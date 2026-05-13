from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
from typing import List
import aiofiles
from pathlib import Path
import renderers  # noqa: F401 — triggers renderer registration
import renderers.registry as renderer_registry
from pydantic import BaseModel
from enum import Enum

router = APIRouter()

# Create necessary directories
UPLOAD_DIR = Path("uploads")
TEMP_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_TEMPLATE_EXTENSIONS = {".psd"}

def validate_file(filename: str, allowed_extensions: set) -> bool:
    """Validate if the file extension is allowed."""
    return Path(filename).suffix.lower() in allowed_extensions

@router.post("/upload")
async def upload_files(
    design: UploadFile = File(...),
    template: UploadFile = File(...),
):
    """
    Upload both a design file and a mockup template file.
    Args:
        design: The image file to place in the mockup (PNG or JPEG)
        template: The PSD template file
    Returns:
        The generated mockup image
    """
    design_path = None
    template_path = None
    
    try:
        # Validate design file
        if not validate_file(design.filename, ALLOWED_IMAGE_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail=f"Design file type not allowed. Please upload {', '.join(ALLOWED_IMAGE_EXTENSIONS)} files"
            )
        
        # Validate template file
        if not validate_file(template.filename, ALLOWED_TEMPLATE_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail="Template must be a PSD file"
            )
        
        # Validate file sizes
        design_content = await design.read()
        if len(design_content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=400,
                detail="Design file size too large. Maximum size is 10MB"
            )
            
        template_content = await template.read()
        if len(template_content) > 20 * 1024 * 1024:  # 20MB
            raise HTTPException(
                status_code=400,
                detail="Template file size too large. Maximum size is 20MB"
            )
        
        # Save the design file
        design_path = UPLOAD_DIR / design.filename
        async with aiofiles.open(design_path, 'wb') as out_file:
            await out_file.write(design_content)
            
        # Save the template file
        template_path = TEMP_DIR / template.filename
        async with aiofiles.open(template_path, 'wb') as out_file:
            await out_file.write(template_content)

        try:
            renderer = renderer_registry.get("photoshop")
            result = await renderer.render_async(
                renderer_config={"template_path": str(template_path)},
                design_path=design_path,
            )

            if not result.success:
                raise Exception(result.error)

            return FileResponse(
                str(result.output_path),
                media_type="image/png",
                filename=result.output_path.name,
            )

        finally:
            # Clean up the uploaded files
            for path in [design_path, template_path]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

    except Exception as e:
        # Clean up any uploaded files on error
        for path in [design_path, template_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing files: {str(e)}"
        )

@router.get("/templates")
async def list_templates():
    """Get list of available mockup templates."""
    templates_dir = Path("templates")
    if not templates_dir.exists():
        return {"templates": []}
        
    templates = []
    for template in templates_dir.glob("*.psd"):
        template_id = template.stem
        templates.append({
            "id": template_id,
            "name": template_id.title().replace("_", " "),
            "description": f"Generate a {template_id.lower().replace('_', ' ')} mockup",
        })
    
    return {"templates": templates} 