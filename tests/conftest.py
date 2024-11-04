import logging
import os

import pytest

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def target_python_version():
    return 3


@pytest.fixture(scope="session")
def target_salt_version():
    target_salt = os.environ.get("SaltVersion", "")

    if target_salt.startswith("v"):
        target_salt = target_salt[1:]
    if target_salt in ("default", "latest", "master", "nightly"):
        pytest.skip("Don't have a specific salt version to test against")
    return target_salt
