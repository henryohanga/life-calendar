# Good Dates API

A numerology-based calendar API to find dates that align with your life path number.

## Development Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

3. Run tests:

   ```bash
   pytest
   ```

4. Start the development server:
   ```bash
   uvicorn api.main:app --reload --port 28000
   ```

## Code Quality

This project uses:

- Black for code formatting
- Ruff for linting
- MyPy for type checking
- Pytest for testing
- Pre-commit hooks for automated checks

## API Documentation

Once running, visit:

- http://localhost:28000/docs for Swagger UI
- http://localhost:28000/redoc for ReDoc
