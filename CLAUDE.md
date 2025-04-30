# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Test Commands
- Install: `pip install -e .` or `pip install -r requirements.txt`
- Run tests: `pytest tests/`
- Run single test: `pytest tests/test_file.py::TestClass::test_function`
- Skip API tests: `pytest tests/ -k "not api"`
- Format code: `black .`
- Lint code: `ruff .`

## Code Style
- **Formatting**: Black with 88 character line length
- **Linting**: Ruff with E, F, W, I, N, UP, S, B, A rule sets
- **Imports**: Standard library first, third-party second, project imports last
- **Naming**: snake_case for functions/variables, PascalCase for classes, CAPS for constants
- **Types**: Use Python type hints throughout
- **Errors**: Use custom error types from errors.py when appropriate
- **Documentation**: Google-style docstrings with Args/Returns sections

## Workflow Rules
Follow the assistant execution flow in .cursorrules:
1. Understand scope before implementation
2. Maintain core_docs (projectRoadmap.md, currentTask.md, techStack.md)
3. Get explicit approval on docs before proceeding
4. Keep tech references updated
5. Self-audit against acceptance criteria before completion