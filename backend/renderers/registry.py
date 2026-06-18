from renderers.base import Renderer

_registry: dict[str, Renderer] = {}


def register(name: str, renderer: Renderer) -> None:
    _registry[name] = renderer


def get(name: str) -> Renderer:
    if name not in _registry:
        raise ValueError(
            f"No renderer registered for '{name}'. Available: {list(_registry)}"
        )
    return _registry[name]
