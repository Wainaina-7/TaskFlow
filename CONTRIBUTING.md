# Contributing to TaskFlow

Thank you for your interest in contributing to TaskFlow! This document provides guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

- Be respectful and inclusive
- Foster a welcoming environment
- Provide constructive feedback
- Respect others' time and effort

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/Taskflow.git
   cd Taskflow
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   # Backend
   source venv/bin/activate
   pip install -r server/requirements.txt

   # Frontend
   cd frontend
   npm install
   ```

## 📝 Development Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Maximum line length: 100 characters

**JavaScript/React (Frontend)**
- Use consistent formatting (ESLint recommended)
- Use camelCase for variables and functions
- Use PascalCase for components
- Add JSDoc comments for complex functions

### Git Workflow

1. Create a descriptive branch name:
   - `feature/add-login` for new features
   - `fix/button-click-issue` for bug fixes
   - `docs/update-readme` for documentation

2. Commit messages:
   - Use clear, concise commit messages
   - Start with a verb: "Add", "Fix", "Update", "Refactor"
   - Example: `Add user authentication endpoint`

3. Before pushing:
   ```bash
   # Ensure your changes don't break existing functionality
   # Run tests if available
   # Check code formatting
   ```

## 🧪 Testing

- Write tests for new features
- Ensure existing tests pass
- Test on multiple browsers (frontend)
- Test with different database configurations (backend)

## 📦 Making Changes

### Adding a New Feature

1. **Discuss first** - Open an issue to discuss your idea
2. **Implement** - Create your feature with tests
3. **Document** - Update README and comments for major changes
4. **Submit PR** - Create a pull request with clear description

### Bug Fixes

1. **Report** - Open an issue describing the bug
2. **Locate** - Find the root cause
3. **Fix** - Implement the fix with tests
4. **Document** - Add comment explaining the fix if non-obvious
5. **Submit PR** - Reference the issue in your PR

## 📋 Pull Request Process

1. **Describe your changes** clearly in the PR description
2. **Reference related issues** (e.g., "Fixes #123")
3. **Keep PR focused** - One feature/fix per PR
4. **Update documentation** if needed
5. **Ensure CI passes** - All tests and checks must pass
6. **Ask for review** - Tag maintainers for feedback

### PR Title Format
- `feat: Add task filtering`
- `fix: Correct user email validation`
- `docs: Update API documentation`
- `style: Format code with Prettier`
- `refactor: Improve task query performance`

## 🔍 Code Review

When reviewing code:
- Check for code quality and style
- Ensure tests are present and passing
- Verify documentation is updated
- Test the changes locally
- Provide constructive feedback

## 📚 Documentation

- Keep README updated with major changes
- Document new API endpoints
- Add inline comments for complex logic
- Update .env.example for new environment variables
- Create/update guides for significant features

## 🐛 Reporting Issues

**Before reporting:**
- Check existing issues
- Try to reproduce the issue
- Gather relevant information

**When reporting:**
- Use a clear, descriptive title
- Describe the exact steps to reproduce
- Include expected vs actual behavior
- Add screenshots if applicable
- Include system information

## 💡 Feature Requests

- Explain the use case
- Describe the feature clearly
- Suggest implementation if possible
- Keep scope reasonable

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Tailwind CSS**: https://tailwindcss.com/
- **Git**: https://git-scm.com/doc

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make TaskFlow better for everyone. We appreciate your time and effort!

---

**Questions?** Open an issue or discussion on GitHub.
