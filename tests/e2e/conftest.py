import pytest
import subprocess
import time
import socket
import os

def wait_for_port(port: int, timeout: int = 15):
    """Wait until a port is open to accept connections."""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                return False

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

@pytest.fixture(scope="session")
def rider_server():
    port = 5173
    if is_port_in_use(port):
        yield f"http://localhost:{port}"
        return

    process = subprocess.Popen(
        f"npm run dev -- --port {port} --host 127.0.0.1",
        cwd=os.path.join(os.path.dirname(__file__), "../../apps/valley_rider"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )
    
    if not wait_for_port(port, timeout=60):
        process.terminate()
        pytest.fail("Valley Rider frontend failed to start in time.")
        
    yield f"http://localhost:{port}"
    
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

@pytest.fixture(scope="session")
def business_server():
    port = 5174
    if is_port_in_use(port):
        yield f"http://localhost:{port}"
        return

    process = subprocess.Popen(
        f"npm run dev -- --port {port} --host 127.0.0.1",
        cwd=os.path.join(os.path.dirname(__file__), "../../apps/valley_business"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )
    
    if not wait_for_port(port, timeout=60):
        process.terminate()
        pytest.fail("Valley Business frontend failed to start in time.")
        
    yield f"http://localhost:{port}"
    
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

@pytest.fixture(scope="session")
def superapp_server():
    port = 5175
    if is_port_in_use(port):
        yield f"http://localhost:{port}"
        return

    process = subprocess.Popen(
        f"npm run dev -- --port {port} --host 127.0.0.1",
        cwd=os.path.join(os.path.dirname(__file__), "../../apps/valley"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )
    
    if not wait_for_port(port, timeout=60):
        process.terminate()
        pytest.fail("Valley SuperApp frontend failed to start in time.")
        
    yield f"http://localhost:{port}"
    
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
