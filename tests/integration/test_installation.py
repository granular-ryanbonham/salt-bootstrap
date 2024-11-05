import json
import logging
import platform
import subprocess

import pytest

## from Demos.win32cred_demo import target

log = logging.getLogger(__name__)


@pytest.fixture
def path():
    if platform.system() == "Windows":
        salt_path = "C:\\Program Files\\Salt Project\\Salt"
        if salt_path not in os.environ["path"]:
            os.environ["path"] = f'{os.environ["path"]};{salt_path}'
    yield os.environ["path"]


def run_salt_call(cmd):
    """
    Runs salt call command and returns a dictionary
    Accepts cmd as a list
    """
    cmd.append("--out=json")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"DGM run_salt_call, cmd '{cmd}', result '{result}'", flush=True)
    if result.stdout:
        json_data = json.loads(result.stdout)
        return json_data["local"]
    return None


def test_ping():
    cmd = ["salt-call", "--local", "test.ping"]
    result = run_salt_call(cmd)
    assert result == True


def test_target_python_version(target_python_version):
    cmd = ["salt-call", "--local", "grains.item", "pythonversion", "--timeout=120"]
    result = run_salt_call(cmd)
    # Returns: {'pythonversion': [3, 10, 11, 'final', 0]}
    py_maj_ver = result["pythonversion"][0]
    assert py_maj_ver == target_python_version


def test_target_salt_version(target_salt_version):
    cmd = ["salt-call", "--local", "grains.item", "saltversion", "--timeout=120"]
    result = run_salt_call(cmd)
    # Returns: {'saltversion': '3006.9+217.g53cfa53040'}
    assert result["saltversion"] == target_salt_version
