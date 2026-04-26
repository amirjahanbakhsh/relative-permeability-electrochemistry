"""Model package exports for convenience."""
from .solver import solve  # noqa: F401
from .physics import krg, effective_diffusivity  # noqa: F401

__all__ = ["solve", "krg", "effective_diffusivity"]
