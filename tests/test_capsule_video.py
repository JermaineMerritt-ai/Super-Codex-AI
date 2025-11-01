import unittest
from codex_project.capsule_video import create_scene, render_video, publish_video

class TestCapsuleVideo(unittest.TestCase):
    def test_create_scene(self):
        scene = create_scene("Test Title", "Test Script", ["img1.png"])
        self.assertEqual(scene["title"], "Test Title")
        self.assertEqual(scene["script"], "Test Script")
        self.assertEqual(scene["visuals"], ["img1.png"])
        self.assertTrue(scene["mythic"])

    def test_render_video(self):
        video = render_video([{"title": "T", "script": "S", "visuals": [], "mythic": True}])
        self.assertIsInstance(video, bytes)
        self.assertEqual(video, b"FAKE_VIDEO_DATA")

    def test_publish_video(self):
        result = publish_video(b"FAKE_VIDEO_DATA", "CapsuleX")
        self.assertEqual(result["capsule_name"], "CapsuleX")
        self.assertEqual(result["video_size"], len(b"FAKE_VIDEO_DATA"))
        self.assertIn("timestamp", result)
        self.assertEqual(result["lineage"], ["capsule"])

if __name__ == "__main__":
    unittest.main()
