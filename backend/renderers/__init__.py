from renderers.registry import register
from renderers.photoshop.renderer import PhotoshopRenderer

register("photoshop", PhotoshopRenderer())
