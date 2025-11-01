import pytest
from capsule_video import create_scene

def test_create_scene_returns_dict():
    config = {"title": "Test Scene"}
    scene = create_scene(config)
    assert isinstance(scene, dict)
    assert scene["status"] == "created"
    assert scene["config"] == config
