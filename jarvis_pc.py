#!/usr/bin/env python3
"""Jarvis avanzado modular para Windows 10/11."""

from __future__ import annotations

import argparse
import platform
import sys

from jarvis_core import JarvisAssistant
from jarvis_core.config import JarvisConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Jarvis avanzado para Windows 10/11")
    parser.add_argument("--wake-word", default="jarvis", help="Palabra de activación")
    parser.add_argument("--text-mode", action="store_true", help="Usar texto en vez de micrófono")
    parser.add_argument("--allow-unsafe", action="store_true", help="Sin confirmaciones de seguridad")
    parser.add_argument("--admin-mode", action="store_true", help="Permite acciones avanzadas")
    parser.add_argument("--locale", default="es-ES", help="Locale para reconocimiento de voz")
    parser.add_argument("--openai-api-key", default="", help="Clave para integraciones LLM futuras")
    return parser


def environment_checks() -> None:
    target = (3, 10, 11)
    if sys.version_info[:3] != target:
        print(
            "[WARN] Recomendado Python 3.10.11 para compatibilidad exacta. "
            f"Actual: {platform.python_version()}"
        )

    if platform.system() != "Windows":
        print("[WARN] Este asistente está optimizado para Windows 10/11.")


def main() -> int:
    environment_checks()
    args = build_parser().parse_args()
    config = JarvisConfig.from_args(args)
    assistant = JarvisAssistant(config)
    return assistant.run()


if __name__ == "__main__":
    raise SystemExit(main())
