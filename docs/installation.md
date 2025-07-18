# Installation Guide

## Prerequisites

- KNIME Analytics Platform 5.5 or higher
- Python 3.11 or higher (handled automatically by KNIME)

## Installation Methods

### Method 1: Install from KNIME Hub (Recommended)

1. Open KNIME Analytics Platform
2. Go to **File → Install KNIME Extensions...**
3. Search for "HTML-XLS Table Reader"
4. Select the extension and click **Next**
5. Follow the installation wizard
6. Restart KNIME when prompted

### Method 2: Install from Local Update Site

1. Download the latest release from [GitHub Releases](https://github.com/yourusername/knime-html-xls-reader/releases)
2. Extract the ZIP file to a local directory
3. In KNIME: **File → Preferences → Install/Update → Available Software Sites**
4. Click **Add...** and add the local directory as an update site
5. Go to **File → Install KNIME Extensions...**
6. Select the local update site and install the extension

### Method 3: Build from Source

#### Prerequisites
- Git
- Pixi package manager

#### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/knime-html-xls-reader.git
cd knime-html-xls-reader
```

2. Install Pixi (if not already installed):
```bash
# Linux/macOS
curl -fsSL https://pixi.sh/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://pixi.sh/install.ps1 | iex"
```

3. Install dependencies:
```bash
pixi install
```

4. Build the extension:
```bash
pixi run build
```

5. The built extension will be in the `build/` directory

## Development Setup

For development, you'll need to configure KNIME to use your local extension:

1. Copy `config.yml.example` to `config.yml`
2. Update the paths in `config.yml` to match your system
3. Add to your `knime.ini`:
```
-Dknime.python.extension.config=/path/to/your/config.yml
```

## Verification

After installation, verify the extension is working:

1. Open KNIME Analytics Platform
2. In the Node Repository, navigate to **Community Nodes → File Readers → HTML-XLS Reader**
3. Drag the node to your workflow
4. The node should appear without errors

## Troubleshooting

### Extension Not Visible
- Restart KNIME after installation
- Check the KNIME console for error messages
- Verify you have KNIME 5.5 or higher

### Python Environment Issues
- The extension manages its own Python environment
- Check the KNIME log for Python-related errors
- Ensure you have sufficient disk space for the Python environment

### Build Failures
- Ensure Pixi is properly installed
- Check that all dependencies are available
- Review the build logs for specific errors

## Uninstallation

1. Go to **Help → About KNIME Analytics Platform → Installation Details**
2. Find "HTML-XLS Table Reader"
3. Click **Uninstall**
4. Restart KNIME
