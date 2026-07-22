"""Portable paths for repo samples and assets."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the repository root (parent of the photoshop_scripting package)."""
    return Path(__file__).resolve().parent.parent


def sample_scripts_dir() -> Path:
    """Directory containing learning samples and shared demo assets."""
    return repo_root() / "sample_scripts"


def samples_dir() -> Path:
    """Directory containing PS_Samples_Files (alongside script samples)."""
    return sample_scripts_dir() / "PS_Samples_Files"


def sample_path(*parts: str) -> Path:
    """
    Build an absolute path under sample_scripts/PS_Samples_Files.

    Example:
        sample_path("Layer Comps.psd")
        sample_path("Photomerge", "photo1.jpg")
    """
    return samples_dir().joinpath(*parts)


def ensure_sample(*parts: str) -> Path:
    """Like sample_path, but raise FileNotFoundError with a clear message."""
    path = sample_path(*parts)
    if not path.is_file():
        raise FileNotFoundError(
            f"Sample file not found: {path}\n"
            f"Expected under {samples_dir()}. "
            "Clone the full repository or restore sample_scripts/PS_Samples_Files."
        )
    return path


def as_ps_path(path: Path | str) -> str:
    """String path suitable for Photoshop Open/Save APIs."""
    return str(Path(path).resolve())
