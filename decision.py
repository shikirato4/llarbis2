from __future__ import annotations

from .nlp import Intent


class DecisionEngine:
    """Policy layer for confirmations and admin-only commands."""

    ADMIN_ACTIONS = {"run_shell", "generate_script"}

    def requires_admin(self, intent: Intent) -> bool:
        return intent.action in self.ADMIN_ACTIONS

    def requires_confirmation(self, intent: Intent, allow_unsafe: bool) -> bool:
        if allow_unsafe:
            return False
        return intent.action in {"run_shell", "close", "generate_script"}
