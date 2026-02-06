from __future__ import annotations

import subprocess
import webbrowser
from pathlib import Path

import psutil
import pyautogui
import requests

from .config import JarvisConfig

APP_ALIASES = {
    "navegador": "start msedge",
    "notepad": "start notepad",
    "bloc de notas": "start notepad",
    "powershell": "start powershell",
    "explorador": "start explorer",
}

SITE_ALIASES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
}


class ActionEngine:
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.config.scripts_dir.mkdir(parents=True, exist_ok=True)

    def open_target(self, target: str) -> str:
        if target in SITE_ALIASES:
            webbrowser.open(SITE_ALIASES[target])
            return f"Abriendo {target}."
        if target.startswith(("http://", "https://")):
            webbrowser.open(target)
            return "URL abierta."

        command = APP_ALIASES.get(target)
        if command:
            subprocess.Popen(command, shell=True)
            return f"Aplicación {target} iniciada."

        return f"No tengo un alias para {target}."

    def close_target(self, process_name: str) -> str:
        killed = 0
        normalized = process_name.replace(".exe", "")
        for proc in psutil.process_iter(attrs=["name"]):
            name = (proc.info.get("name") or "").lower().replace(".exe", "")
            if normalized in name:
                proc.terminate()
                killed += 1
        return f"Procesos cerrados: {killed}."

    def move_mouse(self, direction: str) -> str:
        delta = 140
        movement = {
            "arriba": (0, -delta),
            "abajo": (0, delta),
            "izquierda": (-delta, 0),
            "derecha": (delta, 0),
        }
        dx, dy = movement.get(direction, (0, 0))
        pyautogui.moveRel(dx, dy, duration=0.25)
        return f"Mouse movido {direction}."

    def click(self) -> str:
        pyautogui.click()
        return "Click ejecutado."

    def type_text(self, text: str) -> str:
        pyautogui.write(text, interval=0.02)
        return "Texto escrito."

    def run_shell(self, command: str) -> str:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        output = (completed.stdout or completed.stderr or "sin salida").strip()[:500]
        return f"Código {completed.returncode}. Salida: {output}"

    def generate_script(self, request_text: str) -> str:
        safe_name = request_text.replace(" ", "_")[:30]
        script_path = self.config.scripts_dir / f"script_{safe_name}.ps1"
        body = (
            "# Script generado por Jarvis\n"
            f"# Solicitud: {request_text}\n"
            "Get-Date\n"
            'Write-Host "Personaliza este script antes de uso en producción."\n'
        )
        script_path.write_text(body, encoding="utf-8")
        return f"Script generado en {script_path}."

    def call_api(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        snippet = response.text[:250].replace("\n", " ")
        return f"API {response.status_code}: {snippet}"

    def list_files(self, folder: str) -> str:
        path = Path(folder)
        if not path.exists():
            return "La carpeta no existe."
        names = [p.name for p in sorted(path.iterdir())[:20]]
        return "Elementos: " + ", ".join(names)

    def create_folder(self, folder: str) -> str:
        Path(folder).mkdir(parents=True, exist_ok=True)
        return f"Carpeta creada: {folder}"

    def schedule_windows_task_stub(self, name: str, command: str) -> str:
        schtasks_cmd = f'schtasks /Create /SC DAILY /TN "{name}" /TR "{command}" /F'
        return f"Para programarlo en Windows ejecuta: {schtasks_cmd}"
