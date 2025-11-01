__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .capsule_video import create_scene, render_video, publish_video

# Example integration usage
if __name__ == "__main__":
    scene = create_scene(
        title="Genesis Capsule",
        script="In the beginning, the mythos was inscribed.",
        visuals=["sunrise.png", "origin.png"]
    )
    video_data = render_video([scene])
    result = publish_video(video_data, capsule_name="Genesis Capsule")
    print(result)
