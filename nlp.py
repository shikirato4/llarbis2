from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Intent:
    action: str
    value: Optional[str] = None


class IntentRouter:
    """Rule-based NLU router, easy to replace with LLM later."""

    def parse(self, text: str) -> Intent:
        command = text.lower().strip()

        if command in {"salir", "adiós", "apagar"}:
            return Intent("exit")
        if command in {"ayuda", "qué puedes hacer", "comandos"}:
            return Intent("help")
        if command in {"estado", "sistema", "resumen del sistema"}:
            return Intent("system_status")
        if command in {"hud", "mostrar hud"}:
            return Intent("show_hud")

        if m := re.match(r"(?:abre|abrir) (.+)", command):
            return Intent("open", m.group(1))
        if m := re.match(r"(?:cierra|cerrar) (.+)", command):
            return Intent("close", m.group(1))
        if m := re.match(r"(?:escribe|escribir) (.+)", command):
            return Intent("type", m.group(1))
        if m := re.match(r"mueve mouse (arriba|abajo|izquierda|derecha)", command):
            return Intent("move_mouse", m.group(1))
        if m := re.match(r"(?:ejecuta|ejecutar) comando (.+)", command):
            return Intent("run_shell", m.group(1))
        if m := re.match(r"(?:crear|genera) script (.+)", command):
            return Intent("generate_script", m.group(1))
        if m := re.match(r"consulta api (https?://\S+)", command):
            return Intent("api_call", m.group(1))

        if command in {"clic", "click", "haz clic"}:
            return Intent("click")

        return Intent("chat", text)
