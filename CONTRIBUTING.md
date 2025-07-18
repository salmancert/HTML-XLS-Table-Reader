# Contributing to KNIME HTML-XLS Table Reader

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Your environment details (KNIME version, OS, Python version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Why this enhancement would be useful
- Possible implementation approach

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Issue that pull request!

## Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/knime-html-xls-reader.git
cd knime-html-xls-reader

# Install pixi
curl -fsSL https://pixi.sh/install.sh | sh

# Install dependencies
pixi install

# Run tests
python -m pytest tests/
```

## Style Guide

### Python Style
- Follow PEP 8
- Use type hints where possible
- Document all public functions and classes
- Keep line length under 100 characters

### Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add batch processing for multiple files

- Implement recursive directory scanning
- Add file pattern matching
- Update documentation

Fixes #123
```

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update CHANGELOG.md for notable changes

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.

Thank you for contributing! 🙏
