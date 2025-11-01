import unittest
from capsule_video import render_video

class TestRender(unittest.TestCase):
    def test_render_video_config(self):
        scene = {"scene": "default", "config": {}, "status": "created"}
        output_path = "output.mp4"
        result = render_video(scene, output_path)
        self.assertEqual(result, output_path)

    def test_render_video_args(self):
        scenes = [{"title": "T", "script": "S", "visuals": [], "mythic": True}]
        result = render_video(scenes)
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b"FAKE_VIDEO_DATA")

if __name__ == "__main__":
    unittest.main()
