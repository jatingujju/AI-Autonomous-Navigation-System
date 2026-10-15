
import cv2


def capture_camera():
    """Capture and display live video from the default camera."""

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Camera started. Press Q to exit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read a camera frame.")
                break

            cv2.imshow(
                "Autonomous Navigation - Camera Feed",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("Camera closed.")


if __name__ == "__main__":
    capture_camera()
