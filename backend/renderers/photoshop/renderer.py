from pathlib import Path
from renderers.base import RenderResult
from services.photoshop_service import PhotoshopService


class PhotoshopRenderer:
    """
    Wraps PhotoshopService behind the Renderer protocol.
    renderer_config must contain 'template_path' when using server-side templates,
    or it is omitted when the caller passes the template path directly via design_path
    (current MVP upload flow passes the template path through renderer_config).
    """

    def render(
        self,
        renderer_config: dict,
        design_path: Path,
        output_path: Path | None = None,
    ) -> RenderResult:
        template_path = renderer_config.get("template_path")
        if not template_path:
            return RenderResult(
                success=False,
                error="renderer_config missing required key: 'template_path'",
            )

        try:
            service = PhotoshopService()
            # generate_mockup is async; callers must await via run_in_executor
            # or call from an async context. PhotoshopRenderer.render_async exists
            # for async callers — this sync wrapper is kept for future sync renderers.
            raise RuntimeError(
                "PhotoshopRenderer.render() cannot be called synchronously. "
                "Use PhotoshopRenderer.render_async() from an async context."
            )
        except Exception as e:
            return RenderResult(success=False, error=str(e))

    async def render_async(
        self,
        renderer_config: dict,
        design_path: Path,
        output_path: Path | None = None,
    ) -> RenderResult:
        template_path = renderer_config.get("template_path")
        if not template_path:
            return RenderResult(
                success=False,
                error="renderer_config missing required key: 'template_path'",
            )

        try:
            service = PhotoshopService()
            result_path = await service.generate_mockup(
                str(design_path),
                str(template_path),
            )
            return RenderResult(success=True, output_path=Path(result_path))
        except Exception as e:
            return RenderResult(success=False, error=str(e))
