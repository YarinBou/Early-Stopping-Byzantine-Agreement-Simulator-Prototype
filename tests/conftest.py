"""
Shared pytest fixtures and configuration for Byzantine Agreement Simulator tests.

This module provides common fixtures used across unit, integration, and property tests.
"""

import sys
from pathlib import Path
import pytest
import asyncio
from typing import Generator

# Add src directory to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an event loop for async tests.

    This fixture ensures each test gets a fresh event loop.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# Additional fixtures will be added as the project develops
