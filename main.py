
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def run_module(script_path):
    """Run a project script using the current Python environment."""
    full_path = PROJECT_ROOT / script_path

    if not full_path.is_file():
        print(f"\nError: File not found: {full_path}")
        return

    print(f"\nStarting {script_path}...\n")

    try:
        subprocess.run(
            [sys.executable, str(full_path)],
            cwd=str(PROJECT_ROOT),
            check=False,
        )
    except KeyboardInterrupt:
        print("\nExecution interrupted.")
    except Exception as error:
        print(f"\nCould not run the script: {error}")


def main():
    while True:
        print("\n" + "=" * 52)
        print(" AI-BASED AUTONOMOUS NAVIGATION SYSTEM")
        print("=" * 52)
        print("1. Run Pygame navigation simulation")
        print("2. Open webcam camera feed")
        print("3. Run YOLO object detection")
        print("4. Run path-planning tests")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            run_module("simulation/environment.py")
        elif choice == "2":
            run_module("src/camera_capture.py")
        elif choice == "3":
            run_module("src/object_detection.py")
        elif choice == "4":
            run_module("test_path_planning.py")
        elif choice == "5":
            print("Exiting navigation system.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
