import pytest
from capsule_video import publish_video

def test_publish_video_returns_confirmation():
    video_path = "video.mp4"
    destination = "s3://bucket/videos"
    result = publish_video(video_path, destination)
    assert video_path in result
    assert destination in result
