"""
Domain models used by the Chrome update digest pipelines.
"""

from .feature_tagging import (
    FeatureTag,
    HeadingBasedTagger,
    TagPriority,
    TaggedFeature,
)

__all__ = [
    "FeatureTag",
    "HeadingBasedTagger",
    "TagPriority",
    "TaggedFeature",
]
