from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable


@dataclass
class RenderResult:
    success: bool
    output_path: Path | None = None
    error: str | None = None


@runtime_checkable
class Renderer(Protocol):
    def render(
        self,
        renderer_config: dict,
        design_path: Path,
        output_path: Path | None = None,
    ) -> RenderResult:
        ...
