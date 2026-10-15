
import cv2
from ultralytics import YOLO


def run_object_detection():
    """Detect objects in live webcam frames using pretrained YOLO."""

    print("Loading pretrained YOLO model...")
    model = YOLO("yolo11n.pt")

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Object detection started. Press Q to exit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read a camera frame.")
                break

            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()

            cv2.imshow(
                "AI Autonomous Navigation - YOLO Detection",
                annotated_frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as error:
        print("Object detection error:", error)

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("Object detection stopped.")


if __name__ == "__main__":
    run_object_detection()
