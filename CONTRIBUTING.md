# Contributing to Traffic Violation & Helmet Detection System

Thank you for your interest in contributing! This is a free, open-source project and we welcome contributions from everyone.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing opinions, viewpoints, and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- Harassment or discrimination of any kind
- Insulting/derogatory comments
- Public or private harassment
- Publishing others' private information

## How to Contribute

### Reporting Bugs

Before creating bug reports, check if the issue already exists. When you are creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed**
- **Explain which behavior you expected to see instead**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **A clear and descriptive title**
- **A step-by-step description of the suggested enhancement**
- **Specific examples to demonstrate the steps**
- **A description of the current behavior and expected behavior**
- **Why this enhancement would be useful**

### Pull Requests

- Fill in the pull request template
- Follow the Python style guide (PEP 8)
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/traffic-violation-detection.git
   cd traffic-violation-detection
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

6. Make your changes and test them:
   ```bash
   # Run tests
   pytest
   
   # Check code style
   flake8 backend/
   
   # Format code
   black backend/
   ```

7. Commit your changes:
   ```bash
   git commit -am 'Add feature: description of feature'
   ```

8. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

9. Create a Pull Request on GitHub

## Style Guide

### Python

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use meaningful variable and function names

Example:
```python
def detect_helmet_violation(frame: np.ndarray) -> Dict[str, Any]:
    """
    Detect helmet violations in a video frame.
    
    Args:
        frame: Input video frame as numpy array
        
    Returns:
        Dictionary containing detection results
    """
    # Implementation
    pass
```

### Commits

- Use imperative mood ("add feature" not "added feature")
- Limit first line to 50 characters
- Reference issues and pull requests liberally after the first line
- Consider starting commit message with emoji:
  - 🎨 `:art:` Improve structure/format
  - 🐛 `:bug:` Bug fix
  - ✨ `:sparkles:` New feature
  - 📚 `:books:` Documentation
  - 🧪 `:test_tube:` Add tests
  - ⚡ `:zap:` Performance improvement
  - 🔒 `:lock:` Security fix

### Documentation

- Use clear and concise language
- Include code examples where appropriate
- Update README.md if adding new features
- Add docstrings to all functions
- Keep line length reasonable (80-100 chars)

## Areas for Contribution

### High Priority
- [ ] Real YOLOv8 helmet detection implementation
- [ ] Real EasyOCR plate recognition
- [ ] Unit tests for core modules
- [ ] API documentation improvements
- [ ] Bug fixes

### Medium Priority
- [ ] Performance optimizations
- [ ] Additional database backend support
- [ ] Enhanced error handling
- [ ] Logging improvements
- [ ] Code refactoring

### Low Priority
- [ ] UI/UX enhancements
- [ ] Additional deployment examples
- [ ] Tutorial content
- [ ] Community examples

## Testing

- Write tests for new features
- Run existing tests before submitting PR:
  ```bash
  pytest tests/
  ```
- Aim for >80% code coverage
- Test both happy and error paths

## Documentation

When adding features:

1. Update relevant docstrings
2. Add examples to README if applicable
3. Update API documentation
4. Add inline comments for complex logic
5. Update CHANGELOG.md

## License

By contributing to this project, you agree that your contributions will be licensed under its MIT License.

## Questions?

Feel free to open an issue or discussion for questions. We're here to help!

---

**Thank you for contributing to make this project better! 🎉**
