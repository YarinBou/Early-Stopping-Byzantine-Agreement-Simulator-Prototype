"""
Test suite for Story 1.1: Project Structure & Dependencies

This test suite verifies all acceptance criteria for the project setup story.
"""

import subprocess
import sys
from pathlib import Path


# Get project root (parent of tests directory)
PROJECT_ROOT = Path(__file__).parent.parent


class TestProjectStructure:
    """Tests for AC1: Python 3.10+ project structure with standard layout."""

    def test_src_directory_exists(self):
        """Verify src/ directory exists."""
        assert (PROJECT_ROOT / "src").exists()
        assert (PROJECT_ROOT / "src").is_dir()

    def test_ba_simulator_package_exists(self):
        """Verify ba_simulator package exists with __init__.py."""
        ba_sim_path = PROJECT_ROOT / "src" / "ba_simulator"
        assert ba_sim_path.exists()
        assert ba_sim_path.is_dir()
        assert (ba_sim_path / "__init__.py").exists()

    def test_required_modules_exist(self):
        """Verify all required module directories exist."""
        ba_sim_path = PROJECT_ROOT / "src" / "ba_simulator"
        required_modules = [
            "transport",
            "scheduling",
            "protocols",
            "controller",
            "adversaries",
            "validation",
            "baselines",
            "experiments",
        ]
        for module in required_modules:
            module_path = ba_sim_path / module
            assert module_path.exists(), f"Module {module} does not exist"
            assert module_path.is_dir(), f"Module {module} is not a directory"
            assert (module_path / "__init__.py").exists(), f"Module {module} missing __init__.py"

    def test_tests_directory_exists(self):
        """Verify tests/ directory exists with subdirectories."""
        tests_path = PROJECT_ROOT / "tests"
        assert tests_path.exists()
        assert tests_path.is_dir()

        # Check subdirectories
        for subdir in ["unit", "integration", "property"]:
            subdir_path = tests_path / subdir
            assert subdir_path.exists(), f"tests/{subdir} does not exist"
            assert subdir_path.is_dir(), f"tests/{subdir} is not a directory"

    def test_experiments_directory_exists(self):
        """Verify experiments/ directory exists."""
        experiments_path = PROJECT_ROOT / "experiments"
        assert experiments_path.exists()
        assert experiments_path.is_dir()
        assert (experiments_path / "results").exists()

    def test_docs_directory_exists(self):
        """Verify docs/ directory exists."""
        docs_path = PROJECT_ROOT / "docs"
        assert docs_path.exists()
        assert docs_path.is_dir()


class TestDependencies:
    """Tests for AC2: requirements.txt with version-locked dependencies."""

    def test_requirements_file_exists(self):
        """Verify requirements.txt exists."""
        requirements_path = PROJECT_ROOT / "requirements.txt"
        assert requirements_path.exists()
        assert requirements_path.is_file()

    def test_required_packages_present(self):
        """Verify all required packages are in requirements.txt."""
        requirements_path = PROJECT_ROOT / "requirements.txt"
        requirements_content = requirements_path.read_text()

        required_packages = ["PyNaCl", "pytest", "pandas", "matplotlib"]
        for package in required_packages:
            assert (
                package in requirements_content
            ), f"Required package {package} not found in requirements.txt"

    def test_dependencies_are_version_locked(self):
        """Verify dependencies have version pins."""
        requirements_path = PROJECT_ROOT / "requirements.txt"
        requirements_content = requirements_path.read_text()

        # Check that at least major packages have version specifications
        for line in requirements_content.split("\n"):
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # If it's a package line, it should have a version specifier
            if line and not line.startswith("-"):
                assert (
                    "==" in line or ">=" in line or "<=" in line
                ), f"Package '{line}' is not version-locked"


class TestDocumentation:
    """Tests for AC3: README.md with setup instructions."""

    def test_readme_exists(self):
        """Verify README.md exists."""
        readme_path = PROJECT_ROOT / "README.md"
        assert readme_path.exists()
        assert readme_path.is_file()

    def test_readme_contains_setup_instructions(self):
        """Verify README contains key setup instructions."""
        readme_path = PROJECT_ROOT / "README.md"
        readme_content = readme_path.read_text(encoding="utf-8").lower()

        # Check for key sections
        assert "virtual" in readme_content or "venv" in readme_content
        assert "install" in readme_content
        assert "requirements" in readme_content or "dependencies" in readme_content
        assert "pytest" in readme_content or "test" in readme_content


class TestGitignore:
    """Tests for AC4: .gitignore configured for Python projects."""

    def test_gitignore_exists(self):
        """Verify .gitignore exists."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        assert gitignore_path.exists()
        assert gitignore_path.is_file()

    def test_gitignore_contains_python_patterns(self):
        """Verify .gitignore contains essential Python patterns."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        gitignore_content = gitignore_path.read_text()

        # Check for essential patterns (allow for pattern variants like *.py[cod] which includes *.pyc)
        essential_patterns = [
            "__pycache__",
            ".pytest_cache",
            "venv",
            ".coverage",
        ]
        for pattern in essential_patterns:
            assert pattern in gitignore_content, f"Pattern '{pattern}' not found in .gitignore"

        # Check that Python compiled files are covered (*.pyc or *.py[cod])
        assert (
            "*.pyc" in gitignore_content or "*.py[cod]" in gitignore_content
        ), "Python compiled files pattern (*.pyc or *.py[cod]) not found in .gitignore"


class TestPytestConfiguration:
    """Tests for AC5 and AC6: pytest configuration and execution."""

    def test_pytest_ini_exists(self):
        """Verify pytest.ini exists (AC5)."""
        pytest_ini_path = PROJECT_ROOT / "pytest.ini"
        assert pytest_ini_path.exists()
        assert pytest_ini_path.is_file()

    def test_pytest_ini_configuration(self):
        """Verify pytest.ini contains proper configuration."""
        pytest_ini_path = PROJECT_ROOT / "pytest.ini"
        pytest_ini_content = pytest_ini_path.read_text()

        # Check for essential configurations
        assert "[pytest]" in pytest_ini_content
        assert "testpaths" in pytest_ini_content

    def test_conftest_exists(self):
        """Verify conftest.py exists for shared fixtures."""
        conftest_path = PROJECT_ROOT / "tests" / "conftest.py"
        assert conftest_path.exists()
        assert conftest_path.is_file()

    def test_pytest_runs_successfully(self):
        """Verify pytest runs without errors (AC6)."""
        # Run pytest with minimal options
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        # pytest should exit with 0 (tests found) or 5 (no tests, but config OK)
        assert result.returncode in [0, 5], f"pytest failed: {result.stderr}"


class TestCodeFormatting:
    """Tests for AC7: Code formatting tools configured (optional)."""

    def test_black_configuration_exists(self):
        """Verify black configuration exists."""
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml should exist for black config"

        pyproject_content = pyproject_path.read_text()
        assert "[tool.black]" in pyproject_content, "Black configuration not found"

    def test_flake8_configuration_exists(self):
        """Verify flake8 configuration exists."""
        flake8_path = PROJECT_ROOT / ".flake8"
        assert flake8_path.exists(), ".flake8 configuration file should exist"

        flake8_content = flake8_path.read_text()
        assert "[flake8]" in flake8_content, "Flake8 configuration not found"


class TestPythonVersion:
    """Test Python version requirement (AC1)."""

    def test_python_version_is_3_10_or_higher(self):
        """Verify Python version is 3.10 or higher."""
        version_info = sys.version_info
        assert version_info >= (3, 10), f"Python 3.10+ required, got {sys.version}"
