import logging
import os

import pytest

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def target_python_version():
    return 3


@pytest.fixture(scope="session")
def target_salt_version():
    bootstrap_types = ("git", "stable", "onedir", "onedir_rc")

    # filter out any bootstrap types and then join
    target_salt = ".".join(
        [
            item
            ## DGM for item in os.environ["KITCHEN_SUITE"].split("-")
            for item in os.environ.get("KITCHEN_SUITE", "").split("-")
            if item not in bootstrap_types
        ]
    )

    # target_salt = os.environ["KITCHEN_SUITE"].split("-", 1)[-1].replace("-", ".")

    if target_salt.startswith("v"):
        target_salt = target_salt[1:]
    if target_salt in ("default", "latest", "master", "nightly"):
        pytest.skip("Don't have a specific salt version to test against")
    return target_salt
