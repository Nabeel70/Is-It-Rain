# Contributing to "Will It Rain On My Parade?"

Thank you for your interest in contributing to this NASA Space Apps Challenge 2025 project! We welcome contributions of all kinds.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the [NASA Space Apps Challenge Code of Conduct](https://www.spaceappschallenge.org/code-of-conduct/). By participating, you are expected to uphold this code.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Poetry (Python package manager)
- npm (Node package manager)
- Git

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Is-It-Rain.git
   cd Is-It-Rain
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install poetry
   poetry install
   cp .env.example .env
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run Tests**
   ```bash
   # Backend
   cd backend
   poetry run pytest
   
   # Frontend
   cd frontend
   npm run lint
   ```

5. **Start Development Servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   poetry run uvicorn app.main:app --reload
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

## How to Contribute

### Types of Contributions

We welcome:

- 🐛 **Bug fixes**: Fix issues or improve error handling
- ✨ **New features**: Add functionality (coordinate with maintainers first)
- 📝 **Documentation**: Improve or add documentation
- 🎨 **UI/UX improvements**: Enhance the user interface
- 🧪 **Tests**: Add or improve test coverage
- 🔧 **Refactoring**: Improve code quality or performance
- 🌍 **Translations**: Add internationalization support

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Use the latest version of the code
3. Verify the bug is reproducible

**Good Bug Report Includes**:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, Node version)
- Error messages or logs

**Example**:
```markdown
**Title**: Forecast fails for coordinates near poles

**Description**: 
When requesting a forecast for coordinates above 80° latitude, 
the API returns a 500 error.

**Steps to Reproduce**:
1. Send POST to /api/forecast with latitude=85, longitude=0
2. Observe 500 Internal Server Error

**Expected**: Valid forecast or meaningful error message
**Actual**: Internal server error

**Environment**: 
- OS: Ubuntu 22.04
- Python: 3.11.5
- API URL: http://localhost:8000
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:
- Clear description of the feature
- Rationale: Why is this useful?
- Use case: How would it be used?
- Implementation ideas (optional)

## Development Guidelines

### Code Style

#### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for all functions
- Use docstrings for classes and public methods
- Run `ruff` for linting: `poetry run ruff check .`

**Example**:
```python
async def get_forecast(location: Location, date: date) -> ForecastResponse:
    """
    Retrieve precipitation forecast for a location and date.
    
    Args:
        location: Geographic location coordinates
        date: Date for forecast
        
    Returns:
        ForecastResponse with precipitation data
        
    Raises:
        HTTPException: If location invalid or data unavailable
    """
    # Implementation
```

#### TypeScript (Frontend)

- Use TypeScript strict mode
- Use functional components with hooks
- Follow Airbnb style guide
- Run ESLint: `npm run lint`

**Example**:
```typescript
interface ForecastProps {
  forecast: ForecastResponse;
  onRefresh?: () => void;
}

export const ForecastDisplay: React.FC<ForecastProps> = ({ 
  forecast, 
  onRefresh 
}) => {
  // Component implementation
};
```

### Git Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

   Branch naming:
   - `feature/` for new features
   - `fix/` for bug fixes
   - `docs/` for documentation
   - `refactor/` for code refactoring
   - `test/` for adding tests

2. **Make Changes**
   - Write clear, focused commits
   - One logical change per commit
   - Test your changes

3. **Commit Messages**
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   
   ```
   type(scope): brief description
   
   Longer explanation if needed.
   
   Fixes #123
   ```
   
   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   
   **Examples**:
   ```
   feat(api): add retry logic for NASA API calls
   
   Implement exponential backoff retry mechanism for NASA POWER API
   requests to improve reliability.
   
   Fixes #42
   ```
   
   ```
   fix(frontend): correct date picker validation
   
   Date picker was allowing invalid dates to be submitted.
   Added validation to ensure date is valid before submission.
   
   Fixes #38
   ```

4. **Push Changes**
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing

### Backend Tests

- Use pytest for testing
- Aim for >80% code coverage
- Test both success and error cases
- Mock external API calls

**Example Test**:
```python
import pytest
from app.services.nasa_power import NasaPowerClient

@pytest.mark.asyncio
async def test_precipitation_forecast_success():
    """Test successful forecast retrieval."""
    client = NasaPowerClient()
    location = Location(latitude=40.7128, longitude=-74.0060)
    forecast = await client.precipitation_forecast(location, date(2025, 10, 5))
    
    assert forecast.location.latitude == 40.7128
    assert forecast.precipitation_probability >= 0
    assert forecast.precipitation_probability <= 1
    assert forecast.summary is not None
```

**Running Tests**:
```bash
cd backend
poetry run pytest                 # Run all tests
poetry run pytest -v              # Verbose output
poetry run pytest --cov=app       # With coverage
poetry run pytest tests/test_api.py  # Specific file
```

### Frontend Tests

- Use React Testing Library (to be added)
- Test user interactions
- Test component rendering

### Integration Tests

Test complete workflows:
```bash
# Start both services
cd backend && poetry run uvicorn app.main:app &
cd frontend && npm run dev &

# Run integration tests
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-10-05", "query": "New York City"}'
```

## Documentation

### Code Documentation

- Add docstrings to all public functions/classes
- Include type hints
- Document parameters and return values
- Add usage examples for complex functions

### README Updates

Update README.md if:
- Adding new features
- Changing setup process
- Modifying dependencies
- Changing API

### API Documentation

Update `docs/API.md` if:
- Adding/modifying endpoints
- Changing request/response schemas
- Adding new error codes

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass: `poetry run pytest` and `npm run lint`
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with main branch

### Submitting a Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   Describe how you tested the changes
   
   ## Checklist
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Code follows style guide
   - [ ] No breaking changes (or documented)
   
   ## Related Issues
   Fixes #123
   ```

4. **Code Review**
   - Respond to feedback promptly
   - Make requested changes
   - Push updates to the same branch
   - Request re-review when ready

5. **After Approval**
   - Maintainers will merge your PR
   - Delete your feature branch
   - Pull latest main branch

### Review Criteria

PRs are reviewed for:
- **Functionality**: Does it work as intended?
- **Tests**: Are there adequate tests?
- **Code Quality**: Is it readable and maintainable?
- **Documentation**: Is it documented?
- **Performance**: Are there performance concerns?
- **Security**: Are there security implications?

## Common Tasks

### Adding a New API Endpoint

1. **Define Model** (`backend/app/models/`)
   ```python
   class NewRequest(BaseModel):
       field: str
   ```

2. **Add Route** (`backend/app/api/routes.py`)
   ```python
   @router.post("/new-endpoint")
   async def new_endpoint(request: NewRequest):
       # Implementation
   ```

3. **Add Tests** (`backend/tests/`)
   ```python
   def test_new_endpoint():
       # Test implementation
   ```

4. **Update Docs** (`docs/API.md`)

### Adding a Frontend Component

1. **Create Component** (`frontend/src/components/`)
   ```typescript
   export const NewComponent: React.FC<Props> = ({ prop }) => {
     // Component implementation
   };
   ```

2. **Add Types** (`frontend/src/types/`)
   ```typescript
   export interface NewComponentProps {
     prop: string;
   }
   ```

3. **Import and Use**
   ```typescript
   import { NewComponent } from './components/NewComponent';
   ```

### Adding a New Dataset

1. **Create Service** (`backend/app/services/`)
2. **Add Configuration** (`backend/app/core/config.py`)
3. **Update Documentation** (`docs/DATASETS.md`)
4. **Add Tests**

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: File an issue
- **Feature Requests**: Open an issue with "enhancement" label
- **Security Issues**: Email maintainers directly (don't create public issue)

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Project documentation
- Release notes

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [NASA POWER API](https://power.larc.nasa.gov/docs/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

---

Thank you for contributing to this NASA Space Apps Challenge project! 🚀

**Questions?** Open an issue or discussion on GitHub.
