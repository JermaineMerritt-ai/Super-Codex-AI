import unittest
from capsule_video import create_scene

class TestScene(unittest.TestCase):
    def test_create_scene_config(self):
        config = {"title": "T", "script": "S", "visuals": ["img.png"]}
        scene = create_scene(config)
        self.assertEqual(scene["scene"], "default")
        self.assertEqual(scene["config"], config)
        self.assertEqual(scene["status"], "created")

    def test_create_scene_args(self):
        scene = create_scene("T", "S", ["img.png"])
        self.assertEqual(scene["title"], "T")
        self.assertEqual(scene["script"], "S")
        self.assertEqual(scene["visuals"], ["img.png"])
        self.assertTrue(scene["mythic"])

if __name__ == "__main__":
    unittest.main()
