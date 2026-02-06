from __future__ import annotations

from .actions import ActionEngine
from .config import JarvisConfig
from .decision import DecisionEngine
from .hud import HudWindow
from .logger import setup_logger
from .memory import MemoryStore
from .nlp import IntentRouter
from .speech import SpeechIO
from .system_monitor import SystemMonitor


class JarvisAssistant:
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.logger = setup_logger(str(config.logs_path))
        self.memory = MemoryStore(config.db_path)
        self.speech = SpeechIO(config.locale, config.text_mode)
        self.intent_router = IntentRouter()
        self.decision = DecisionEngine()
        self.monitor = SystemMonitor()
        self.hud = HudWindow(self.monitor)
        self.actions = ActionEngine(config)

    def _confirm(self, prompt: str) -> bool:
        self.speech.speak(f"Confirma: {prompt}. Responde sí o no.")
        answer = self.speech.listen().lower()
        return answer in {"sí", "si", "confirmo", "ok", "vale"}

    def _context_reply(self, text: str) -> str:
        latest = list(self.memory.latest(limit=4))
        if latest:
            return "He tomado nota. Contexto reciente actualizado."
        return f"Recibido: {text}"

    def _execute_intent(self, action: str, value: str | None) -> str:
        if action == "help":
            return (
                "Puedo abrir/cerrar apps, ejecutar comandos, monitorear sistema, "
                "gestionar archivos, llamar APIs y mostrar HUD."
            )
        if action == "system_status":
            return self.monitor.format_snapshot(self.monitor.snapshot())
        if action == "show_hud":
            self.hud.open_async()
            return "HUD iniciado en una ventana separada."
        if action == "open" and value:
            return self.actions.open_target(value)
        if action == "close" and value:
            return self.actions.close_target(value)
        if action == "type" and value:
            return self.actions.type_text(value)
        if action == "move_mouse" and value:
            return self.actions.move_mouse(value)
        if action == "click":
            return self.actions.click()
        if action == "run_shell" and value:
            return self.actions.run_shell(value)
        if action == "generate_script" and value:
            return self.actions.generate_script(value)
        if action == "api_call" and value:
            return self.actions.call_api(value)
        if action == "chat" and value:
            return self._context_reply(value)
        return "Comando no implementado todavía."

    def run(self) -> int:
        self.speech.speak("Núcleo Jarvis inicializado. Esperando instrucciones.")
        while True:
            text = self.speech.listen()
            if not text:
                continue

            normalized = text.lower().strip()
            if normalized in {"salir", "terminar", "adiós"}:
                self.speech.speak("Cerrando núcleo Jarvis.")
                return 0

            if not self.config.text_mode and self.config.wake_word:
                if not normalized.startswith(self.config.wake_word.lower()):
                    continue
                normalized = normalized[len(self.config.wake_word) :].strip(" ,")

            intent = self.intent_router.parse(normalized)

            if self.decision.requires_admin(intent) and not self.config.admin_mode:
                self.speech.speak("Ese comando requiere modo administrador. Reinicia con --admin-mode.")
                continue

            if self.decision.requires_confirmation(intent, self.config.allow_unsafe):
                if not self._confirm(f"ejecutar {intent.action} {intent.value or ''}"):
                    self.speech.speak("Acción cancelada.")
                    continue

            reply = self._execute_intent(intent.action, intent.value)
            self.memory.add("user", normalized)
            self.memory.add("assistant", reply)
            self.logger.info("intent=%s value=%s reply=%s", intent.action, intent.value, reply)
            self.speech.speak(reply)
