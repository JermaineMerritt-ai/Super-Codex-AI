import pytest
from capsule_video import render_video, create_scene

def test_render_video_returns_path(tmp_path):
    scene = create_scene({"title": "Render Test"})
    output_path = tmp_path / "output.mp4"
    result = render_video(scene, str(output_path))
    assert result == str(output_path)
