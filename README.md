# EzyBGRemover

<p align="center">
  <a href="https://www.python.org/"><img alt="Python 3.13+" src="https://img.shields.io/badge/Python-3.13%2B-3776AB.svg?logo=python&logoColor=white"></a>
  <a href="https://pypi.org/project/rembg/"><img alt="rembg on PyPI" src="https://img.shields.io/pypi/v/rembg.svg?label=rembg&logo=pypi&logoColor=white"></a>
  <a href="https://pypi.org/project/pyinstaller/"><img alt="PyInstaller on PyPI" src="https://img.shields.io/pypi/v/pyinstaller.svg?label=PyInstaller&logo=pypi&logoColor=white"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-2ea44f.svg"></a>
</p>

EzyBGRemover is a small local background-removal utility for images. It accepts an image file or a folder, removes backgrounds with `rembg`, and writes transparent PNG outputs without uploading files to an external service.

The repository contains a Python command-line script and a PyInstaller build path for a Windows console executable named `RemoveBG.exe`.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Install From Source](#install-from-source)
- [Use The Windows EXE](#use-the-windows-exe)
- [Use From Source](#use-from-source)
- [Supported Inputs](#supported-inputs)
- [Build The EXE](#build-the-exe)
- [Release The EXE](#release-the-exe)
- [Technical Notes](#technical-notes)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Removes image backgrounds locally with `rembg`.
- Processes one image file or a folder of images.
- Recurses through nested folders.
- Saves every result as a transparent PNG.
- Uses predictable output names ending in `_no_bg.png`.
- Includes a PyInstaller build script for `dist/RemoveBG.exe`.
- Bundles `u2net.onnx` into the packaged Windows executable.

The project depends on `rembg[cpu]`. GPU acceleration is not configured in `pyproject.toml` or `build_app.py`.

## Requirements

| Requirement | Version / notes |
| --- | --- |
| Python | `>=3.13` |
| Package manager | `uv`, installed with `pip` by default or the standalone installer as a fallback |
| Background removal backend | `rembg[cpu] >= 2.0.75` |
| Build tool | `pyinstaller >= 6.20.0` |
| License | MIT, see [LICENSE](LICENSE) |

The Python version is declared in both `pyproject.toml` and `.python-version`.

## Install From Source

Clone the repository:

```bash
git clone https://github.com/Sakth1/EzyBGRemover.git
cd EzyBGRemover
```

### Install uv

Install `uv` with `pip` first.

```
pip install uv
```

If `pip` is unavailable or the install fails in your environment, use the official standalone installer as the fallback.

| Platform | Suggested pip install | Standalone fallback |
| --- | --- | --- |
| Windows PowerShell | `python -m pip install --user uv` | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Linux | `python3 -m pip install --user uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| macOS | `python3 -m pip install --user uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

Restart the terminal if `uv` is not found immediately after installation.

### Create The Environment

Windows PowerShell:

```powershell
uv venv --python 3.13
.\.venv\Scripts\Activate.ps1
uv sync
```

Linux and macOS:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv sync
```

## Use The Windows EXE

If a release build is published, download `RemoveBG.exe` from:

```text
https://github.com/Sakth1/EzyBGRemover/releases
```

The preferred Windows workflow is drag-and-drop:

1. Open the folder that contains `RemoveBG.exe`.
2. Drag one image or one folder of images onto `RemoveBG.exe`.
3. Release the item on the executable.

Windows launches the executable with the dropped item path as an argument, so this works the same as passing the path from a terminal.

`RemoveBG.exe` is still a console application. Use PowerShell or Command Prompt when you want to see progress, errors, or the saved output path:

```powershell
.\RemoveBG.exe "C:\path\to\image.png"
.\RemoveBG.exe "C:\path\to\folder-with-images"
```

Current limitations:

- The app reads only the first command-line argument, `sys.argv[1]`.
- Dropping multiple files or folders may pass multiple paths to the process, but only the first path is processed.
- If you launch by double-clicking or drag-and-drop, the console window may close after the run finishes. Use PowerShell when you want to see progress, errors, or the saved output path.

### Drag And Drop On Other Operating Systems

| Platform | Current repository behavior |
| --- | --- |
| Windows | Supported for one dropped image or one dropped folder when using `RemoveBG.exe`. |
| Linux | No Linux desktop launcher is included. Desktop drag-and-drop requires packaging with a `.desktop` file whose `Exec` entry includes a file field code such as `%f` or `%F`. Use the terminal for this repository as-is. |
| macOS | No `.app` bundle is included. Finder/Dock drag-and-drop onto an app requires a macOS app bundle that declares supported document types and handles opened documents. Use the terminal for this repository as-is. |

On Linux or macOS, you can still drag a file or folder into many terminal windows to paste its path, then run the Python command normally.

## Use From Source

EzyBGRemover accepts one positional argument: a file path or a folder path.

Windows PowerShell:

```powershell
python main.py "C:\path\to\image.png"
python main.py "C:\path\to\folder-with-images"
```

Linux and macOS:

```bash
python main.py "/path/to/image.png"
python main.py "/path/to/folder-with-images"
```

There are no CLI flags, configuration files, or interactive prompts in the current implementation.

## Supported Inputs

The current validation logic supports lowercase `.jpg` and `.png` extensions.

| Extension | Status |
| --- | --- |
| `.jpg` | Supported |
| `.png` | Supported |
| `.jpeg` | Not supported |
| `.webp` | Not supported |
| `.bmp` | Not supported |
| `.JPG`, `.PNG` | Not supported by the current case-sensitive check |

### Single Image Output

Command:

```powershell
python main.py "C:\Images\portrait.jpg"
```

Output:

```text
portrait_no_bg.png
```

For single-file processing, the output is saved in the current working directory.

### Folder Output

Command:

```powershell
python main.py "C:\Images\ProductShots"
```

For folder input, the script creates a sibling output folder with `_no_bg` appended and processes supported images recursively.

Example input:

```text
ProductShots/
|-- shoe.jpg
|-- bag.png
`-- nested/
    `-- watch.jpg
```

Example output:

```text
ProductShots_no_bg/
|-- shoe_no_bg.png
|-- bag_no_bg.png
`-- nested_no_bg/
    `-- watch_no_bg.png
```

Existing files with the same output name are overwritten when Pillow saves the result.

## Build The EXE

The Windows build path is `build_app.py`.

### Build Requirements

| Requirement | Notes |
| --- | --- |
| Windows | The script is configured to produce `RemoveBG.exe` |
| Python `>=3.13` | Required by `pyproject.toml` |
| `uv` | Used to create and sync the environment |
| Internet access | Required if `u2net.onnx` is not already cached |
| `assets/RB.png` | Required executable icon |

### Build Steps

Windows PowerShell:

```powershell
git clone https://github.com/Sakth1/EzyBGRemover.git
cd EzyBGRemover
uv venv --python 3.13
.\.venv\Scripts\Activate.ps1
uv sync
python build_app.py
```

On success, the executable is written to:

```text
dist/RemoveBG.exe
```

PyInstaller working files are written to:

```text
_pyinstaller_build/
_pyinstaller_spec/
```

### What The Build Script Does

`build_app.py`:

1. Uses `main.py` as the entry point.
2. Uses `assets/RB.png` as the executable icon.
3. Locates `u2net.onnx` from `U2NET_HOME` or the default rembg model directory.
4. Downloads the model through rembg if it is missing.
5. Writes `_pyinstaller_runtime_hook.py`.
6. Runs PyInstaller with `--onefile` and `--console`.
7. Adds the model to the bundled executable under `models/`.
8. Includes package metadata and hidden imports required by the rembg stack.

The runtime hook sets `U2NET_HOME` to the bundled model directory when the executable runs from a PyInstaller bundle.

### Build Troubleshooting

| Problem | Check |
| --- | --- |
| `assets/RB.png` not found | Ensure the icon file exists before building. |
| Model download fails | Check internet access or set `U2NET_HOME` to a directory containing `u2net.onnx`. |
| Missing dependency in the executable | Rebuild with `python build_app.py`; it includes project-specific hidden imports and metadata options. |
| Window closes immediately | Run `RemoveBG.exe` from PowerShell to keep output visible. |

## Technical Notes

### Runtime Flow

```text
Path argument
  -> Path resolution
  -> Single image or folder dispatch
  -> Pillow image load
  -> rembg background removal
  -> PNG output
```

### Background Removal Backend

The project delegates segmentation and background removal to `rembg`. The declared dependency is `rembg[cpu]`, so the configured runtime path is CPU-based.

### Configuration

There is no application configuration file.

The build script recognizes `U2NET_HOME`:

- If set, `build_app.py` looks for `u2net.onnx` in that directory.
- If unset, it uses the default rembg model location.
- In the packaged executable, `_pyinstaller_runtime_hook.py` points `U2NET_HOME` to the bundled `models` directory.

### Logging

The application uses terminal `print(...)` statements for progress and status output. No structured logging framework is configured.

## Project Structure

```text
EzyBGRemover/
|-- .github/
|   `-- workflows/
|       `-- release-exe.yml
|-- assets/
|   `-- RB.png
|-- build_app.py
|-- main.py
|-- pyproject.toml
|-- uv.lock
|-- LICENSE
|-- _pyinstaller_runtime_hook.py
|-- RemoveBG.spec
|-- wewe.spec
`-- README.md
```

| Path | Purpose |
| --- | --- |
| `.github/workflows/release-exe.yml` | Manual GitHub Actions workflow that builds and publishes `RemoveBG.exe` for a release tag. |
| `main.py` | Command-line entry point and image/folder processing logic. |
| `build_app.py` | Primary PyInstaller build script for `RemoveBG.exe`. |
| `pyproject.toml` | Project metadata and dependency declarations. |
| `uv.lock` | Locked dependency resolution generated by `uv`. |
| `LICENSE` | MIT license for the project. |
| `assets/RB.png` | Icon used by the Windows executable build. |
| `_pyinstaller_runtime_hook.py` | Runtime hook that points bundled builds to the included model directory. |
| `RemoveBG.spec` | PyInstaller spec file present in the repository. |
| `wewe.spec` | Older PyInstaller spec file present in the repository. |

Generated and local-only directories such as `build/`, `dist/`, `_pyinstaller_build/`, `_pyinstaller_spec/`, `.venv/`, `.ruff_cache/`, and `__pycache__/` are ignored by the repository configuration.

## Contributing

1. Fork the repository.
2. Create a focused branch:

```bash
git checkout -b feature/your-change
```

3. Make the change.
4. Test with a small image and a folder.
5. Commit with a clear message:

```bash
git commit -m "Add support for jpeg images"
```

6. Push the branch and open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
