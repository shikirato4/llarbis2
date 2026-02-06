from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class JarvisConfig:
    """Runtime configuration for the assistant."""

    wake_word: str = "jarvis"
    text_mode: bool = False
    allow_unsafe: bool = False
    admin_mode: bool = False
    locale: str = "es-ES"
    openai_api_key: str = ""
    db_path: Path = Path("jarvis_memory.db")
    logs_path: Path = Path("jarvis_actions.log")
    scripts_dir: Path = Path("generated_scripts")

    @classmethod
    def from_args(cls, args: object) -> "JarvisConfig":
        return cls(
            wake_word=getattr(args, "wake_word", "jarvis"),
            text_mode=getattr(args, "text_mode", False),
            allow_unsafe=getattr(args, "allow_unsafe", False),
            admin_mode=getattr(args, "admin_mode", False),
            locale=getattr(args, "locale", "es-ES"),
            openai_api_key=getattr(args, "openai_api_key", ""),
        )
