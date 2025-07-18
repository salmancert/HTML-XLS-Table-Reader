# HTML-XLS-Table-Reader

[![KNIME Hub](https://img.shields.io/badge/KNIME-Hub-yellow.svg)](https://hub.knime.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://github.com/yourusername/knime-html-xls-reader/workflows/Build/badge.svg)](https://github.com/yourusername/knime-html-xls-reader/actions)

A KNIME node extension that reads HTML tables from files saved with .xls extension. This node is designed to handle the common scenario where web applications export HTML tables with an .xls extension for Excel compatibility.

![Node Screenshot](docs/images/node-screenshot.png)

## 🚀 Features

- **📁 Smart File Detection**: Automatically detects HTML content in .xls files
- **🔍 Encoding Detection**: Automatic character encoding detection with fallback options
- **📊 Advanced Parsing**: Configure headers, skip rows, date parsing, and more
- **📂 Batch Processing**: Process entire directories with pattern matching
- **🖼️ Table Preview**: Preview tables during configuration
- **🏷️ Metadata Support**: Optional metadata columns for source tracking
- **🔄 Flow Variable Integration**: Full support for dynamic file paths

## 📋 Requirements

- KNIME Analytics Platform 5.5 or higher
- Python 3.11 or higher

## 🛠️ Installation

### Option 1: Install from KNIME Hub
1. Open KNIME Analytics Platform
2. Go to File → Install KNIME Extensions
3. Search for "HTML-XLS Table Reader"
4. Click Install

### Option 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/knime-html-xls-reader.git
cd knime-html-xls-reader

# Install pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | sh

# Install dependencies
pixi install

# Build the extension
pixi run build
```

See [Installation Guide](docs/installation.md) for detailed instructions.

## 📖 Usage

### Quick Start
1. Drag the "HTML-XLS Table Reader" node from the node repository to your workflow
2. Configure the file path in the node settings
3. Adjust parsing options if needed
4. Execute the node

### Batch Processing
Enable batch mode to process multiple files:
```
✓ Batch Processing Mode
Folder Path: /path/to/files/
File Pattern: report_*.xls
✓ Recursive Search
```

See [Usage Guide](docs/usage.md) for more examples.

## 🔧 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| **File Path** | Path to HTML-XLS file | - |
| **Encoding** | Character encoding | auto |
| **Table Index** | Which table to extract (-1 for all) | 0 |
| **Header Rows** | Number of header rows | 1 |
| **Parse Dates** | Auto-detect date columns | True |
| **Include Metadata** | Add source file information | True |

## 🧪 Development

### Setting up Development Environment

```bash
# Clone and setup
git clone https://github.com/yourusername/knime-html-xls-reader.git
cd knime-html-xls-reader

# Install development environment
pixi install

# Create config.yml from example
cp config.yml.example config.yml
# Edit config.yml with your paths

# Run tests
pixi run test
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- KNIME AG for the Python node development framework
- The pandas and BeautifulSoup communities

## 📞 Support

- 📧 [Email Support](mailto:support@example.com)
- 💬 [KNIME Forum](https://forum.knime.com)
- 🐛 [Report Issues](https://github.com/yourusername/knime-html-xls-reader/issues)

## 📊 Project Status

![GitHub release (latest by date)](https://img.shields.io/github/v/release/yourusername/knime-html-xls-reader)
![GitHub issues](https://img.shields.io/github/issues/yourusername/knime-html-xls-reader)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/knim
