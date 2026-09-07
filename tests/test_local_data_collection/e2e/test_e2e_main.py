import os

import pytest
from dotenv import find_dotenv, load_dotenv

pytest.importorskip("clr")

load_dotenv(find_dotenv())

REQUIRED_TEST_ENV_VARS = (
    "AZURE_CLIENT_ID",
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_SECRET",
    "TEST_LANDING_CONTAINER",
    "TEST_AZURE_STORAGE_URL",
)


def require_test_environment():
    missing = [var for var in REQUIRED_TEST_ENV_VARS if not os.getenv(var)]
    if missing:
        raise AssertionError(
            f"Missing test-environment variables (expected in .env or shell): {', '.join(missing)}"
        )


def test_main_when_full_pipeline_runs_completes_without_raising(monkeypatch):
    require_test_environment()
    monkeypatch.setenv("ENVIRONMENT", "test")

    from local_data_collection.main import main

    main()