import sys
import time
import urllib.request
import urllib.error

NGINX_HOST = "nginx"

OK_URL = f"http://{NGINX_HOST}:8080/"
ERR_URL = f"http://{NGINX_HOST}:8081/"

def http_get(url, timeout=2):
    """Send a GET request and return (status_code, body_as_text)."""
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as e:
        # HTTPError happens for non-2xx codes 
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body
    except Exception as e:
        # Network errors, DNS errors, connection refused and more...
        return None, str(e)

def wait_until_up(url, attempts=30, delay=1.0):
    """retry until the service is reachable"""
    for _ in range(attempts):
        status, _ = http_get(url)
        if status is not None:
            return True
        time.sleep(delay)
    return False

def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)

def main():
    # Wait for nginx to become reachable
    if not wait_until_up(OK_URL):
        fail(f"Nginx not reachable at {OK_URL}")

    # Test 1: Port 8080 should return 200 and contain expected text
    status, body = http_get(OK_URL)
    if status != 200:
        fail(f"Expected 200 from {OK_URL}, got {status}")
    if "hello from nginx container" not in body.lower():
        fail("Expected HTML content not found on port 8080")

    # Test 2: Port 8081 should return 418 (error)
    status, _ = http_get(ERR_URL)
    if status != 418:
        fail(f"Expected 418 from {ERR_URL}, got {status}")

    print("[PASS] All tests passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
