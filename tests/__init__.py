"""Test configuration and shared fixtures for CWM-Sci."""

import pytest
import asyncio
from typing import AsyncGenerator

import pytest_asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def event_loop_async() -> AsyncGenerator[asyncio.AbstractEventLoop, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()