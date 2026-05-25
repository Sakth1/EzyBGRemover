import subprocess
import sys
import os

def build():
    # Define the base command
    # Note: Using --onefile as requested in your current command
    # We use the name and icon you provided.
    
    command = [
        "pyinstaller",
        "--name", "RemoveBG",
        "--icon", "assets/RB.png",
        "--onefile",
        "-y",
        "main.py"
    ]

    # To fix the PackageNotFoundError, we should include the hiddenimports
    # We can add them via command line arguments instead of editing the spec manually
    command.extend(["--hidden-import", "rembg", "--hidden-import", "importlib.metadata"])

    print(f"Running command: {' '.join(command)}")
    
    try:
        subprocess.run(command, check=True)
        print("\nBuild successful!")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
    except FileNotFoundError:
        print("\nError: 'pyinstaller' not found. Please ensure it is installed in your environment.")

if __name__ == "__main__":
    build()
