"""Background workers so the UI stays responsive during COM automation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from PySide6.QtCore import QThread, Signal


class BatchWorker(QThread):
    progress = Signal(int, int, str)  # current, total, message
    log = Signal(str)
    finished_ok = Signal(list)
    failed = Signal(str)

    def __init__(self, job: str, params: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.job = job
        self.params = params
        self._cancel = False

    def cancel(self) -> None:
        self._cancel = True

    def _should_cancel(self) -> bool:
        return self._cancel

    def _on_progress(self, current: int, total: int, message: str) -> None:
        self.progress.emit(current, total, message)
        self.log.emit(f"[{current}/{total}] {message}")

    def run(self) -> None:
        try:
            from photoshop_scripting import batch as batch_ops

            results: List[str] = []
            job = self.job
            p = self.params

            if job == "resize":
                results = batch_ops.batch_resize(
                    p["files"],
                    width=p["width"],
                    height=p.get("height"),
                    resolution=p.get("resolution"),
                    resample=p.get("resample", 8),
                    save_as_copy_dir=p.get("output_dir"),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "export_jpeg":
                results = batch_ops.batch_export_jpeg(
                    p["files"],
                    p["output_dir"],
                    quality=p.get("quality", 10),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "export_png":
                results = batch_ops.batch_export_png(
                    p["files"],
                    p["output_dir"],
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "layer_comps":
                results = batch_ops.export_layer_comps(
                    p["psd_path"],
                    p["output_dir"],
                    format=p.get("format", "png"),
                    sleep_between=p.get("sleep", 0.2),
                    on_progress=self._on_progress,
                )
            elif job == "run_action":
                results = batch_ops.run_action_on_files(
                    p["files"],
                    p["action_name"],
                    p["action_set"],
                    save=p.get("save", True),
                    sleep_between=p.get("sleep", 0.2),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "export_layers":
                results = batch_ops.export_layers_to_files(
                    p["psd_path"],
                    p["output_dir"],
                    format=p.get("format", "png"),
                    quality=p.get("quality", 10),
                    visible_only=p.get("visible_only", False),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "watermark":
                results = batch_ops.batch_watermark_text(
                    p["files"],
                    p["output_dir"],
                    text=p.get("text", "© Copyright"),
                    opacity=p.get("opacity", 40.0),
                    font_size=p.get("font_size", 24.0),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "srgb":
                results = batch_ops.batch_convert_srgb(
                    p["files"],
                    p["output_dir"],
                    format=p.get("format", "jpg"),
                    quality=p.get("quality", 10),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "border":
                results = batch_ops.batch_add_canvas_border(
                    p["files"],
                    p["output_dir"],
                    padding_px=p.get("padding_px", 40),
                    format=p.get("format", "png"),
                    quality=p.get("quality", 10),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            elif job == "text_replace":
                results = batch_ops.batch_replace_text(
                    p["files"],
                    p["find"],
                    p["replace"],
                    save=p.get("save", True),
                    output_dir=p.get("output_dir"),
                    sleep_between=p.get("sleep", 0.15),
                    on_progress=self._on_progress,
                    should_cancel=self._should_cancel,
                )
            else:
                raise ValueError(f"Unknown job: {job}")

            if self._cancel:
                self.log.emit("Cancelled by user.")
            self.finished_ok.emit(results)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


def collect_images(folder: str, recursive: bool = False) -> List[Path]:
    from photoshop_scripting.batch import iter_images

    return iter_images(folder, recursive=recursive)
