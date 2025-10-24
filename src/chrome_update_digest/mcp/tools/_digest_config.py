from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


ModelPreferences = Optional[Union[Dict[str, Any], List[Any]]]


@dataclass
class DigestRunConfig:
    """Run-scoped configuration payload for digest generation.

    This encapsulates mutable run state (model preferences, resolved languages, etc.)
    so the EnhancedWebplatformDigestTool instance does not leak configuration
    across multiple invocations.
    """

    version: str
    channel: str
    language: Optional[str]
    split_by_area: bool
    target_area: Optional[str]
    model_preferences: ModelPreferences = None
    explicit_model: Optional[str] = None

    def resolved_languages(self) -> List[str]:
        """Return the list of languages that should be produced for this run."""
        if self.language in (None, "bilingual"):
            return ["en", "zh"]
        return [self.language]

    def language_mode(self) -> str:
        """Return the display language identifier used in responses."""
        return self.language or "bilingual"

