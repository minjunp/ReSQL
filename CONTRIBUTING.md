# Contributing to ReSQL

Thank you for your interest in contributing to ReSQL! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the issue tracker
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - System information (OS, Python version, GPU)
   - Relevant code snippets or error messages

### Suggesting Enhancements

We welcome suggestions for:
- New model support
- Performance improvements
- Additional error analysis features
- Documentation improvements

## Development Process

### Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/ReSQL.git
cd ReSQL
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes:
   - Follow existing code style
   - Add docstrings to functions
   - Update documentation as needed

3. Test your changes:
   - Run on small dataset first
   - Verify no regressions
   - Check that examples still work

4. Commit your changes:
```bash
git add .
git commit -m "Add: brief description of changes"
```

### Code Style Guidelines

#### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add type hints where appropriate
- Keep functions focused and small
- Add docstrings for all functions

Example:
```python
def analyze_error(query: str, error_msg: str) -> dict:
    """
    Analyze SQL query error and categorize it.

    Args:
        query (str): The SQL query that failed
        error_msg (str): The error message from execution

    Returns:
        dict: Analysis result with error type and explanation
    """
    # Implementation
    pass
```

#### Documentation
- Use clear, concise language
- Include code examples
- Keep formatting consistent
- Update README if adding features

### Adding New Model Support

To add support for a new model:

1. Create initialization function in `Analysis/Inference_template_qwen_7b.py`:
```python
def new_model_initialize(model_name):
    """Initialize new model."""
    # Your implementation
    return model, tokenizer
```

2. Create generation function:
```python
def new_model_generate_result(prompt, model, tokenizer):
    """Generate using new model."""
    # Your implementation
    return response
```

3. Update main() function to include your model
4. Test with small dataset
5. Document in Analysis/README.md

### Submitting Pull Requests

1. Push to your fork:
```bash
git push origin feature/your-feature-name
```

2. Create pull request from your fork to main repository

3. In the PR description:
   - Explain what changes were made
   - Reference any related issues
   - Describe how you tested the changes
   - Include example output if applicable

4. Wait for review and address any feedback

## Testing Guidelines

### Before Submitting

- [ ] Code runs without errors
- [ ] Tested on small dataset (10-20 examples)
- [ ] No breaking changes to existing functionality
- [ ] Documentation updated
- [ ] Examples still work
- [ ] No sensitive data (tokens, credentials) in commits

### Testing Checklist

```python
# Test on small sample
data = data[:10]  # Small subset for testing

# Verify output format
assert 'Analysis_inference' in result
assert 'Error Type' in result['Analysis_inference']

# Check all supported models still work
for model in supported_models:
    test_model(model)
```

## Documentation Contributions

Documentation improvements are always welcome!

### Areas to Contribute

- Fix typos or unclear explanations
- Add more examples
- Improve code comments
- Create tutorials
- Translate documentation

### Documentation Structure

```
README.md           - Main project overview
QUICKSTART.md       - 5-minute getting started
Data/README.md      - Dataset documentation
Result/README.md    - Results documentation
Analysis/README.md  - Code documentation
examples/README.md  - Example usage
```

## Adding New Datasets

To contribute new reasoning datasets:

1. Generate using the framework
2. Verify quality on sample
3. Document model and settings used
4. Create PR with:
   - Dataset files in appropriate folder
   - Update to Result/README.md
   - Statistics about the dataset

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

### Communication

- Use clear, professional language
- Ask questions when unclear
- Provide context in discussions
- Share knowledge and resources

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing:

- Check existing issues and discussions
- Read the documentation
- Open an issue with the question label
- Contact the maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in academic citations (for significant contributions)

## Versioning

We follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Release Process

1. Update version number
2. Update CHANGELOG.md
3. Create release tag
4. Update documentation
5. Announce release

---

Thank you for contributing to ReSQL! Your efforts help advance Text-to-SQL research.

For questions: [your-email@example.com]
