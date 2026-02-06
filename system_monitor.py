from __future__ import annotations

from dataclasses import dataclass
import psutil

try:
    import GPUtil
except ImportError:  # optional
    GPUtil = None


@dataclass(slots=True)
class SystemSnapshot:
    cpu_percent: float
    ram_percent: float
    net_sent_mb: float
    net_recv_mb: float
    process_count: int
    gpu_load: str


class SystemMonitor:
    def snapshot(self) -> SystemSnapshot:
        vm = psutil.virtual_memory()
        net = psutil.net_io_counters()
        gpu_load = "N/A"
        if GPUtil:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_load = ", ".join(f"{g.name}:{g.load * 100:.0f}%" for g in gpus)

        return SystemSnapshot(
            cpu_percent=psutil.cpu_percent(interval=0.4),
            ram_percent=vm.percent,
            net_sent_mb=net.bytes_sent / (1024 * 1024),
            net_recv_mb=net.bytes_recv / (1024 * 1024),
            process_count=len(psutil.pids()),
            gpu_load=gpu_load,
        )

    def format_snapshot(self, snap: SystemSnapshot) -> str:
        return (
            f"CPU {snap.cpu_percent:.1f}% | RAM {snap.ram_percent:.1f}% | "
            f"GPU {snap.gpu_load} | Red TX {snap.net_sent_mb:.1f}MB RX {snap.net_recv_mb:.1f}MB | "
            f"Procesos {snap.process_count}"
        )
