"""
Strict area classifier for WebGPU features.
Implements precise rules to avoid misclassifying non-graphics features as WebGPU.
"""

import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass

@dataclass
class ClassificationResult:
    """Result of WebGPU classification."""
    is_webgpu: bool
    score: int
    reasons: List[str]
    exclusion_reasons: List[str]

class WebGPUClassifier:
    """Strict classifier for WebGPU/graphics features."""
    
    # Strong WebGPU/graphics keywords
    WEBGPU_KEYWORDS = {
        'webgpu', 'gpu', 'dawn', 'texture', 'shader', 'wgsl', 
        'pipeline', 'buffer', 'adapter', 'device', 'compute',
        'rendering', 'graphics', '3d', 'volumetric', 'astc', 
        'compression', 'core-features-and-limits', 'compatibility mode',
        'rasterization', 'fragment', 'vertex', 'tessellation',
        'bindgroup', 'sampler', 'renderbundle', 'querysets'
    }
    
    # Core WebGPU technical terms for content analysis
    CORE_TERMS = {
        'gpu buffer', 'pipeline', 'adapter', 'device', 'compute shader',
        'wgsl', 'render pass', 'command encoder', 'texture format',
        'bindgroup layout', 'gpu queue', 'render bundle', 'query set'
    }
    
    # Generic domains that should NOT be in graphics-webgpu
    GENERIC_DOMAINS = {
        'network', 'security', 'privacy', 'payments', 'navigation',
        'web apis', 'origin trials', 'deprecations', 'media', 
        'ai', 'performance', 'authentication', 'workers', 'web app',
        'service worker', 'fetch', 'cache', 'storage', 'permissions',
        'notifications', 'push', 'background sync', 'web share'
    }
    
    # Non-graphics keywords that strongly indicate misclassification
    EXCLUSION_KEYWORDS = {
        'payment', 'spc', 'csp', 'accept-language', 'tcp', 'port',
        'fingerprint', 'freeze', 'worker', 'rtc', 'audio', 'json',
        'mime', 'authentication', 'prefetch', 'macos', 'iso-2022',
        'crash', 'prompt api', 'speech', 'navigation', 'web app',
        'service worker', 'fetch api', 'cache api', 'notification',
        'permission', 'cookie', 'cors', 'header', 'http', 'https'
    }
    
    # Special WebGPU section identifiers
    WEBGPU_SECTIONS = {
        'detailed webgpu updates',
        'webgpu features',
        'what\'s new in webgpu'
    }
    
    def __init__(self, strict_mode: bool = True):
        """Initialize classifier.
        
        Args:
            strict_mode: If True, apply strict exclusion rules
        """
        self.strict_mode = strict_mode
    
    def is_strong_webgpu(self, feature: Dict) -> ClassificationResult:
        """Determine if a feature is strongly related to WebGPU/graphics.
        
        Args:
            feature: Feature dictionary with title, content, heading_path
            
        Returns:
            ClassificationResult with determination and reasoning
        """
        title = feature.get('title', '').lower()
        content = feature.get('content', '').lower()
        heading_path = [h.lower() for h in feature.get('heading_path', [])]
        
        score = 0
        reasons = []
        exclusion_reasons = []
        
        # Check last two heading levels for WebGPU keywords
        last_two = heading_path[-2:] if len(heading_path) >= 2 else heading_path
        for heading in last_two:
            for keyword in self.WEBGPU_KEYWORDS:
                if keyword in heading:
                    score += 2
                    reasons.append(f"Near heading contains '{keyword}'")
                    break
        
        # Check title for WebGPU keywords
        for keyword in self.WEBGPU_KEYWORDS:
            if keyword in title:
                score += 2
                reasons.append(f"Title contains '{keyword}'")
                break
        
        # Check content for core technical terms
        core_term_count = sum(1 for term in self.CORE_TERMS if term in content)
        if core_term_count >= 2:
            score += 1
            reasons.append(f"Content contains {core_term_count} core WebGPU terms")
        
        # Check if feature is from special WebGPU section
        for section in self.WEBGPU_SECTIONS:
            if any(section in h for h in heading_path):
                # Only add score if not in a generic subdomain
                if not any(domain in h for domain in self.GENERIC_DOMAINS for h in last_two):
                    score += 1
                    reasons.append(f"From WebGPU section: '{section}'")
                break
        
        # Apply exclusions
        if self.strict_mode:
            # Check for generic domains in last two headings
            for heading in last_two:
                for domain in self.GENERIC_DOMAINS:
                    if domain in heading and score < 4:
                        exclusion_reasons.append(f"Generic domain '{domain}' in near heading")
                        return ClassificationResult(False, score, reasons, exclusion_reasons)
            
            # Check for exclusion keywords in title
            for keyword in self.EXCLUSION_KEYWORDS:
                if keyword in title:
                    # Allow if there's overwhelming WebGPU evidence
                    if score < 4:
                        exclusion_reasons.append(f"Exclusion keyword '{keyword}' in title")
                        return ClassificationResult(False, score, reasons, exclusion_reasons)
            
            # Require WebGPU keywords in last two headings or title
            has_near_webgpu = any(
                any(k in h for k in self.WEBGPU_KEYWORDS) 
                for h in last_two
            )
            has_title_webgpu = any(k in title for k in self.WEBGPU_KEYWORDS)
            
            if not (has_near_webgpu or has_title_webgpu):
                exclusion_reasons.append("No WebGPU keywords in title or near headings")
                return ClassificationResult(False, score, reasons, exclusion_reasons)
        
        # Final determination
        is_webgpu = score >= 3
        if not is_webgpu:
            exclusion_reasons.append(f"Score {score} below threshold 3")
        
        return ClassificationResult(is_webgpu, score, reasons, exclusion_reasons)
    
    def classify_feature(self, feature: Dict) -> Dict:
        """Classify a feature and return detailed analysis.
        
        Args:
            feature: Feature dictionary
            
        Returns:
            Dictionary with classification details
        """
        result = self.is_strong_webgpu(feature)
        
        return {
            'title': feature.get('title'),
            'is_webgpu': result.is_webgpu,
            'score': result.score,
            'reasons': result.reasons,
            'exclusion_reasons': result.exclusion_reasons,
            'heading_path': feature.get('heading_path')
        }