# How to Contribute to This Free Open-Source Project

Welcome! We're excited you want to contribute. This guide will help you get started.

## Quick Links

- 📖 [Main README](README.md)
- 📝 [Contributing Guidelines](CONTRIBUTING.md)
- 💻 [Installation Guide](INSTALL.md)
- 🚀 [Deployment Guide](DEPLOYMENT.md)
- 📋 [Code of Conduct](CODE_OF_CONDUCT.md)

---

## For Everyone

### Just Using the Project?

1. ⭐ **Star the repository** on GitHub to show support
2. 💬 **Share feedback** - Open an issue to report bugs or suggest features
3. 🐛 **Report bugs** - Help us find and fix issues
4. 📣 **Tell others** - Share the project with friends and colleagues

### Have a Question?

1. Check [README.md](README.md) and [INSTALL.md](INSTALL.md)
2. Search [existing issues](https://github.com/yourusername/traffic-violation-detection/issues)
3. Start a [discussion](https://github.com/yourusername/traffic-violation-detection/discussions)
4. Open a new issue with `[QUESTION]` prefix

---

## For Developers

### Getting Started (5 minutes)

1. **Fork the repo**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/traffic-violation-detection.git
   cd traffic-violation-detection
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

4. **Install development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Make your changes**
   - Edit files
   - Test locally
   - Commit changes

6. **Push and create PR**
   ```bash
   git push origin feature/my-awesome-feature
   # Open PR on GitHub
   ```

---

## Types of Contributions We Need

### 🐛 Bug Fixes
- Report bugs with clear reproduction steps
- Fix confirmed bugs
- Add regression tests

**Example PR**:
```
Fix: Camera initialization fails on port 8001 (#123)

- Changed port selection logic
- Added fallback port
- Tested on Windows 10 & Ubuntu
- Fixes #120
```

### ✨ New Features
- Real YOLOv8 helmet detection
- Real EasyOCR plate recognition
- Multi-camera support
- Advanced analytics dashboard
- Mobile app integration

**Checklist**:
- [ ] Feature is useful and well-scoped
- [ ] Implementation is clean and documented
- [ ] Tests are added
- [ ] Documentation is updated

### 📚 Documentation
- Improve README
- Add tutorials
- Fix typos
- Clarify confusing sections
- Add examples

### 🧪 Tests
- Unit tests for core modules
- Integration tests
- End-to-end tests
- Performance tests

### ♻️ Code Quality
- Refactor complex code
- Improve performance
- Add type hints
- Improve error handling
- Better logging

---

## Contribution Workflow

### Step 1: Find an Issue to Work On

**Good First Issues** (for beginners):
- Issues labeled `good-first-issue`
- Issues labeled `help-wanted`
- Typos and documentation fixes
- Adding tests

**Browse Issues**:
```bash
# https://github.com/yourusername/traffic-violation-detection/issues
```

**Create Your Own Issue**:
If you have an idea, open an issue first to discuss it!

### Step 2: Fork & Clone

```bash
# Fork on GitHub (click the Fork button)

# Clone your fork
git clone https://github.com/YOUR-USERNAME/traffic-violation-detection.git
cd traffic-violation-detection

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-AUTHOR/traffic-violation-detection.git
```

### Step 3: Create a Feature Branch

```bash
# Update main branch
git fetch upstream
git checkout main
git rebase upstream/main

# Create feature branch
git checkout -b feature/my-feature

# Branch naming conventions:
# feature/helmet-detection
# fix/camera-port-issue
# docs/installation-guide
# test/camera-service
```

### Step 4: Make Your Changes

```bash
# Edit files
# Test locally
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001

# Run tests
pytest tests/

# Check code style
flake8 backend/
black backend/
```

### Step 5: Commit Your Changes

```bash
# Add files
git add .

# Commit with clear message
git commit -m "feature: add helmet detection support

- Implement YOLOv8 helmet detection
- Add detection confidence threshold
- Update API endpoints
- Add tests for detection module"

# Commit emoji guide:
# 🎨 :art: - Improve structure
# 🐛 :bug: - Bug fix
# ✨ :sparkles: - New feature
# 📚 :books: - Documentation
# 🧪 :test_tube: - Add tests
# ⚡ :zap: - Performance
# 🔒 :lock: - Security
```

### Step 6: Push to Your Fork

```bash
git push origin feature/my-feature
```

### Step 7: Create Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill in the PR template
4. Submit!

### Step 8: Respond to Review

- Address comments
- Update code if requested
- Re-push changes
- PR will auto-update

### Step 9: Merge

Once approved, maintainers will merge your PR. Congratulations! 🎉

---

## Code Style Guide

### Python (PEP 8)

```python
# Good
def detect_helmet_violation(frame: np.ndarray) -> Dict[str, Any]:
    """
    Detect helmet violations in a video frame.
    
    Args:
        frame: Input video frame as numpy array
        
    Returns:
        Dictionary containing detection results
        
    Raises:
        ValueError: If frame is invalid
    """
    if not isinstance(frame, np.ndarray):
        raise ValueError("Frame must be numpy array")
    
    violations = []
    # Implementation
    return {"violations": violations}

# Bad
def detectHelmetViolation(f):
    v = []
    # Implementation
    return v
```

### Key Rules
- Use type hints
- Add docstrings
- Max line length: 100
- 4 spaces indentation
- CamelCase for classes, snake_case for functions

### Tools

```bash
# Format code
black backend/

# Check style
flake8 backend/

# Type check
mypy backend/
```

---

## Testing

### Writing Tests

```python
# tests/test_camera_service.py
import pytest
from backend.app.services.camera_service import CameraCapture

def test_camera_capture_initialization():
    """Test camera capture initialization."""
    camera = CameraCapture(camera_index=0)
    assert camera is not None
    camera.stop()

def test_invalid_camera_index():
    """Test invalid camera index handling."""
    with pytest.raises(ValueError):
        camera = CameraCapture(camera_index=999)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test
pytest tests/test_camera_service.py -v
```

---

## Documentation

### Adding Documentation

1. **Update README** if adding major features
2. **Add docstrings** to all functions
3. **Create examples** for complex features
4. **Update INSTALL.md** if changing setup

### Example Docstring

```python
def process_frame(
    frame: np.ndarray,
    confidence_threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Process video frame for violation detection.
    
    Args:
        frame: Input video frame (1280x720 or similar)
        confidence_threshold: Detection confidence (0-1)
        
    Returns:
        {
            "violations": List of violations detected,
            "timestamp": When frame was processed,
            "confidence": Average confidence score
        }
        
    Raises:
        ValueError: If frame is invalid
        RuntimeError: If detection model fails
        
    Example:
        >>> frame = cv2.imread("test.jpg")
        >>> result = process_frame(frame)
        >>> print(result["violations"])
    """
    pass
```

---

## Git Tips & Tricks

### Keeping Your Fork Updated

```bash
# Fetch latest changes
git fetch upstream

# Rebase your branch
git rebase upstream/main

# Or merge (creates merge commit)
git merge upstream/main
```

### Squashing Commits

```bash
# Before: 5 commits, After: 1 clean commit
git rebase -i HEAD~5
# Mark commits as 'squash' (s) to combine
```

### Fixing a Mistake

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Fix last commit message
git commit --amend
```

---

## CI/CD Pipeline

All PRs run automated checks:

- ✅ **Tests** - pytest suite
- ✅ **Linting** - flake8 & black
- ✅ **Type checking** - mypy
- ✅ **Security** - bandit & safety
- ✅ **Docker build** - container builds successfully

Your PR must pass all checks to be merged!

---

## Recognition

Contributors are recognized in:

1. GitHub Contributors page
2. CONTRIBUTORS.md file
3. Commit history (forever on GitHub)

Thank you for your contribution! 🌟

---

## Common Contribution Scenarios

### Scenario 1: Fix a Typo

1. Find typo in README
2. Fork repo
3. Fix typo on main branch
4. Submit PR with title: "docs: fix typo in README"

### Scenario 2: Add a New Feature

1. Open issue: "Add real YOLOv8 helmet detection"
2. Discuss approach with maintainers
3. Fork repo, create feature branch
4. Implement feature with tests
5. Update docs
6. Submit PR

### Scenario 3: Improve Performance

1. Profile code to find bottleneck
2. Open issue: "Optimize frame processing"
3. Fork repo, create optimization branch
4. Implement optimization
5. Add benchmarks showing improvement
6. Submit PR

---

## Need Help?

- 📖 **Documentation**: Check README.md
- 💬 **Discussion**: Open a GitHub Discussion
- 🐛 **Bugs**: Report on Issues page
- ❓ **Questions**: Ask in Discussions or Issues

---

## Final Checklist Before Submitting PR

- [ ] Code follows style guide (black, flake8)
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No unnecessary commits (squash if needed)
- [ ] Branch is rebased on latest main
- [ ] PR title is clear and descriptive
- [ ] PR description explains what and why
- [ ] No sensitive data (keys, passwords)
- [ ] Issue reference included (#123)

---

**Thank you for making this project better! Your contributions matter! 🚀**

If you have questions, ask in the discussions or issues. We're here to help!

Happy coding! ❤️
