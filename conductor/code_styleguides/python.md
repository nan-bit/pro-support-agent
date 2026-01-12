# Python Style Guide

## General Principles
- **PEP 8 Adherence:** Follow PEP 8 for code style, including 4-space indentation and appropriate variable naming.
- **Type Hinting:** Use Python type hints (PEP 484) for all function arguments and return types to improve code clarity and tool support.
- **Docstrings:** Use Google-style docstrings for all modules, classes, and functions.

## Project Specifics
- **Asynchronous Code:** Prefer `asyncio` for I/O-bound tasks, especially when interacting with APIs like Shopify.
- **Environment Variables:** Use `python-dotenv` and access credentials via `os.getenv`. Never hardcode secrets.
- **Logging:** Use the standard `logging` module for tracking events and errors. Avoid `print` statements in production code.
- **Dependency Management:** Maintain a clean `requirements.txt` and use virtual environments.

## Testing
- **Framework:** Use `pytest` for unit and integration testing.
- **Coverage:** Aim for high test coverage, particularly for critical tool logic in `tools.py`.
