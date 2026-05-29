# EzyBGRemover


[![Python](https://img.shields.io/badge/python-%3E%3D3.13-blue)](https://www.python.org/)  [![rembg](https://img.shields.io/pypi/v/rembg?label=rembg)](https://pypi.org/project/rembg/)  [![pyinstaller](https://img.shields.io/pypi/v/pyinstaller?label=pyinstaller)](https://pypi.org/project/pyinstaller/)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

EzyBGRemover is a small local background-removal utility for images. It runs on your machine, processes files without uploading them to an external service, and keeps the workflow simple: provide an image or folder path, then receive transparent PNG outputs.

The project is built around a Python command-line script and a reproducible PyInstaller build for a Windows console executable.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Build From Source](#build-from-source)
- [Technical Notes](#technical-notes)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Removes image backgrounds locally with `rembg`.
- Supports single-file processing for `.jpg` and `.png` files.
- Supports folder processing with recursive traversal.
- Saves processed images as transparent PNG files.
- Uses predictable output names ending in `_no_bg.png`.
- Provides a PyInstaller build script for `dist/RemoveBG.exe`.
- Bundles `u2net.onnx` into the packaged Windows executable.

> [!NOTE]
> The project depends on `rembg[cpu]`. GPU acceleration is not configured in `pyproject.toml` or the build script.

## Requirements

| Requirement | Version / Notes |
| --- | --- |
| Python | `>=3.13` |
| Package manager | `uv` |
| Background removal backend | `rembg[cpu] >= 2.0.75` |
| Build tool | `pyinstaller >= 6.20.0` |

The Python version is declared in both `pyproject.toml` and `.python-version`.

## Installation

### Windows Executable

If a release build is published, download `RemoveBG.exe` from the repository releases page:

https://github.com/Sakth1/EzyBGRemover/releases

Run the executable from PowerShell or Command Prompt:

```powershell
.\RemoveBG.exe "C:\path\to\image.png"
.\RemoveBG.exe "C:\path\to\folder"
```

`RemoveBG.exe` is a console application. Launching it from a terminal keeps progress messages and errors visible.

### From Source

Clone the repository first:

```bash
git clone https://github.com/Sakth1/EzyBGRemover.git
cd EzyBGRemover
```

Install `uv`, create a virtual environment, install dependencies, and run the script.

#### Install uv

The official standalone installer is preferred. Use the `pip` fallback only when the standalone installer is blocked by your environment or you already manage Python tooling through `pip`.

| Platform | Preferred installer | pip fallback |
| --- | --- | --- |
| Windows PowerShell | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `python -m pip install --user uv` |
| Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `python3 -m pip install --user uv` |
| macOS | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `python3 -m pip install --user uv` |

Restart the terminal if `uv` is not found immediately after installation.

#### Create the Environment

Windows PowerShell:

```powershell
uv venv --python 3.13
.\.venv\Scripts\Activate.ps1
uv sync
```

Linux:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv sync
```

macOS:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv sync
```

#### Run the Script

Windows PowerShell:

```powershell
python main.py "C:\path\to\image.png"
```

Linux / macOS:

```bash
python main.py "/path/to/image.png"
```

## Usage

EzyBGRemover accepts one positional argument: a file path or a folder path.

```bash
python main.py "<file-or-folder-path>"
```

With the Windows executable:

```powershell
.\RemoveBG.exe "<file-or-folder-path>"
```

There are no CLI flags, configuration files, or interactive prompts in the current implementation.

### Single Image

```powershell
python main.py "C:\Images\portrait.jpg"
```

For an input file named:

```text
portrait.jpg
```

The output is:

```text
portrait_no_bg.png
```

For single-file processing, the output is saved in the current working directory.

### Folder

```powershell
python main.py "C:\Images\ProductShots"
```

For folder input, the script:

1. Creates a new output folder using the `_no_bg` suffix.
2. Processes supported images inside the folder.
3. Recurses into nested folders.
4. Saves each result as a PNG file.

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

### Supported File Types

The current validation logic supports lowercase `.jpg` and `.png` extensions.

| Extension | Status |
| --- | --- |
| `.jpg` | Supported |
| `.png` | Supported |
| `.jpeg` | Not supported |
| `.webp` | Not supported |
| `.bmp` | Not supported |
| `.JPG`, `.PNG` | Not supported by the current case-sensitive check |

### Output Behavior

| Input | Output location | Naming |
| --- | --- | --- |
| Single image | Current working directory | `<name>_no_bg.png` |
| Folder | New `<folder>_no_bg` directory | `<name>_no_bg.png` |
| Nested folder | New nested directory with `_no_bg` suffix | `<name>_no_bg.png` |

Existing files with the same output name are overwritten when Pillow saves the result.

### Executable Drag-and-Drop

The application does not implement a graphical drag-and-drop interface. Any drag-and-drop behavior comes from the operating system launching the executable with dropped item paths as command-line arguments.

The current code reads only `sys.argv[1]`. That means only the first supplied path is processed.

| Platform | Behavior |
| --- | --- |
| Windows | Dropping one image or one folder onto `RemoveBG.exe` can launch the executable with that item as the first argument. The app processes that one path. |
| Windows, multiple items | Not supported by the current app logic. If the shell passes multiple paths, only the first path is processed. |
| Linux | No `.desktop` launcher or file association is included. Use the terminal command instead. Desktop drag-and-drop would require packaging and an `Exec` entry with file field codes. |
| macOS | No `.app` bundle is included. Use the terminal command instead. Finder items can be dragged into Terminal to insert their paths, then the command can be run normally. |

Recommended terminal usage remains:

```powershell
.\RemoveBG.exe "C:\path\to\image-or-folder"
```

or:

```bash
python main.py "/path/to/image-or-folder"
```

### Runtime Notes

- Images are opened with Pillow.
- Background removal is performed by `rembg.remove(...)`.
- Progress and output locations are printed to the terminal.
- Unsupported files are skipped during folder traversal.
- The first source run may download the `u2net.onnx` model if it is not already present in the rembg model cache.
- Invalid paths, unreadable images, or model/runtime failures may raise Python exceptions.

## Build From Source

The reproducible Windows build path is `build_app.py`.

### Build Requirements

| Requirement | Notes |
| --- | --- |
| Windows | The script is configured to produce `RemoveBG.exe` |
| Python `>=3.13` | Required by `pyproject.toml` |
| `uv` | Recommended dependency manager |
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

### What the Build Script Does

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
|-- assets/
|   `-- RB.png
|-- build_app.py
|-- main.py
|-- pyproject.toml
|-- uv.lock
|-- _pyinstaller_runtime_hook.py
|-- RemoveBG.spec
|-- wewe.spec
`-- README.md
```

| Path | Purpose |
| --- | --- |
| `main.py` | Command-line entry point and image/folder processing logic. |
| `build_app.py` | Primary PyInstaller build script for `RemoveBG.exe`. |
| `pyproject.toml` | Project metadata and dependency declarations. |
| `uv.lock` | Locked dependency resolution generated by `uv`. |
| `assets/RB.png` | Icon used by the Windows executable build. |
| `_pyinstaller_runtime_hook.py` | Runtime hook that points bundled builds to the included model directory. |
| `RemoveBG.spec` | PyInstaller spec file present in the repository. |
| `wewe.spec` | Older PyInstaller spec file present in the repository. |

Generated and local-only directories such as `build/`, `dist/`, `_pyinstaller_build/`, `_pyinstaller_spec/`, `.venv/`, and `__pycache__/` are ignored by the repository configuration.

## Contributing

1. Fork the repository.
2. Create a focused branch:

```bash
git checkout -b feature/your-change
```

3. Make the change.
4. Test with a small image or folder.
5. Commit with a clear message:

```bash
git commit -m "Add support for jpeg images"
```

6. Push the branch and open a pull request.

## License

No license file is currently present in this repository.

Without an explicit license, the project is not currently distributed under an open-source license. Add a license file before redistributing, modifying, or using this project beyond personal evaluation.
