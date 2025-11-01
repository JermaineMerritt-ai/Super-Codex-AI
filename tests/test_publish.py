import unittest
from capsule_video import publish_video
import time

class TestPublish(unittest.TestCase):
    def test_publish_video_config(self):
        video_path = "output.mp4"
        destination = "S3"
        result = publish_video(video_path, destination)
        self.assertEqual(result, f"Video at {video_path} published to {destination}")

    def test_publish_video_args(self):
        video_data = b"FAKE_VIDEO_DATA"
        capsule_name = "CapsuleX"
        result = publish_video(video_data, capsule_name)
        self.assertEqual(result["capsule_name"], capsule_name)
        self.assertEqual(result["video_size"], len(video_data))
        self.assertIn("timestamp", result)
        self.assertEqual(result["lineage"], ["capsule"])

if __name__ == "__main__":
    unittest.main()
