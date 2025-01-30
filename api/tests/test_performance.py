import pytest
import time
from typing import List, Callable, Any
from statistics import mean, stdev

from fastapi.testclient import TestClient
from api.main import app
from api.numerology import (
    calculate_life_path_number,
    get_date_compatibility,
)


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def benchmark(
    func: Callable[..., Any], iterations: int = 1000, **kwargs: Any
) -> tuple[float, float]:
    """
    Benchmark a function's execution time.
    Returns (mean_time, std_dev) in milliseconds.
    """
    times: List[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        func(**kwargs)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms

    return mean(times), stdev(times)


def test_numerology_calculation_performance() -> None:
    """Test performance of core numerology calculations."""
    mean_time, std_dev = benchmark(
        calculate_life_path_number,
        birth_date="1990-01-01",
        single_digit=True,
    )
    assert mean_time < 0.1  # Should take less than 0.1ms
    print(f"\nLife path calculation: {mean_time:.3f}ms ±{std_dev:.3f}ms")

    mean_time, std_dev = benchmark(
        get_date_compatibility,
        birth_date="1990-01-01",
        target_date="2024-01-01",
        single_digit=True,
    )
    assert mean_time < 0.2  # Should take less than 0.2ms
    print(f"Date compatibility: {mean_time:.3f}ms ±{std_dev:.3f}ms")


def test_api_endpoint_performance(client: TestClient) -> None:
    """Test performance of API endpoints."""

    def call_good_dates() -> None:
        client.post(
            "/good-dates/",
            json={
                "birth_date": "1990-01-01",
                "match_on_single_digit": True,
                "year": 2024,
            },
        )

    mean_time, std_dev = benchmark(call_good_dates, iterations=100)
    assert mean_time < 50  # Should take less than 50ms
    print(f"\nGood dates endpoint: {mean_time:.1f}ms ±{std_dev:.1f}ms")


def test_cache_performance(client: TestClient) -> None:
    """Test performance improvement from caching."""

    def get_good_dates() -> None:
        client.post(
            "/good-dates/",
            json={
                "birth_date": "1990-01-01",
                "match_on_single_digit": True,
                "year": 2024,
            },
        )

    # First call (uncached)
    start = time.perf_counter()
    get_good_dates()
    uncached_time = (time.perf_counter() - start) * 1000

    # Second call (cached)
    start = time.perf_counter()
    get_good_dates()
    cached_time = (time.perf_counter() - start) * 1000

    # Cache should be at least 2x faster
    assert cached_time < uncached_time * 0.5
    print(f"\nUncached: {uncached_time:.1f}ms")
    print(f"Cached: {cached_time:.1f}ms")
    print(f"Cache speedup: {uncached_time/cached_time:.1f}x")
