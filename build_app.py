import os
import subprocess
import sys
from pathlib import Path


APP_NAME = "RemoveBG"
ENTRYPOINT = "main.py"
ICON_PATH = Path("assets") / "RB.png"
MODEL_NAME = "u2net.onnx"
MODEL_DIR_IN_BUNDLE = "models"
RUNTIME_HOOK = Path("_pyinstaller_runtime_hook.py")
SPEC_DIR = Path("_pyinstaller_spec")
WORK_DIR = Path("_pyinstaller_build")


def project_root() -> Path:
    return Path(__file__).resolve().parent


def u2net_home() -> Path:
    configured_home = os.environ.get("U2NET_HOME")
    if configured_home:
        return Path(configured_home).expanduser().resolve()
    return (Path(os.environ.get("XDG_DATA_HOME", "~")).expanduser() / ".u2net").resolve()


def ensure_model_file() -> Path:
    model_path = u2net_home() / MODEL_NAME
    if model_path.exists():
        return model_path

    print(f"{MODEL_NAME} was not found at {model_path}. Downloading it with rembg...")
    from rembg.sessions.u2net import U2netSession

    downloaded_path = Path(U2netSession.download_models()).resolve()
    if not downloaded_path.exists():
        raise FileNotFoundError(f"rembg did not create the expected model file: {downloaded_path}")

    return downloaded_path


def write_runtime_hook(root: Path) -> Path:
    hook_path = root / RUNTIME_HOOK
    hook_path.write_text(
        "\n".join(
            [
                "import os",
                "import sys",
                "",
                "if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):",
                "    os.environ['U2NET_HOME'] = os.path.join(sys._MEIPASS, 'models')",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return hook_path


def pyinstaller_add_data_arg(source: Path, destination: str) -> str:
    return f"{source}{os.pathsep}{destination}"


def build() -> None:
    root = project_root()
    os.chdir(root)

    icon_path = (root / ICON_PATH).resolve()
    entrypoint_path = (root / ENTRYPOINT).resolve()

    if not icon_path.exists():
        raise FileNotFoundError(f"Icon file not found: {icon_path}")
    if not entrypoint_path.exists():
        raise FileNotFoundError(f"Entrypoint not found: {entrypoint_path}")

    model_path = ensure_model_file()
    runtime_hook = write_runtime_hook(root)
    SPEC_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--specpath",
        str(SPEC_DIR),
        "--workpath",
        str(WORK_DIR),
        "--name",
        APP_NAME,
        "--icon",
        str(icon_path),
        "--onefile",
        "--console",
        "-y",
        "--runtime-hook",
        str(runtime_hook),
        "--add-data",
        pyinstaller_add_data_arg(model_path, MODEL_DIR_IN_BUNDLE),
        "--copy-metadata",
        "rembg",
        "--copy-metadata",
        "pymatting",
        "--copy-metadata",
        "onnxruntime",
        "--collect-data",
        "skimage",
        "--hidden-import",
        "rembg",
        "--hidden-import",
        "rembg.bg",
        "--hidden-import",
        "rembg.sessions.u2net",
        "--hidden-import",
        "pymatting",
        "--hidden-import",
        "onnxruntime",
        "--hidden-import",
        "scipy._cyutility",
        "--hidden-import",
        "skimage.morphology._skeletonize",
        str(entrypoint_path),
    ]

    print(f"Using Python: {sys.executable}")
    print(f"Bundling model: {model_path}")
    print(f"Running command: {' '.join(command)}\n")

    try:
        subprocess.run(command, check=True)
        print(f"\nBuild successful: {root / 'dist' / f'{APP_NAME}.exe'}")
    except subprocess.CalledProcessError as exc:
        print(f"\nBuild failed with exit code {exc.returncode}")
        raise


if __name__ == "__main__":
    build()
