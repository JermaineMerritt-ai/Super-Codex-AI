

"""
capsule_video package
Provides basic video pipeline functions:
- create_scene
- render_video
- publish_video
"""

from .scene import create_scene
from .render import render_video
from .publish import publish_video

__all__ = ["create_scene", "render_video", "publish_video"]