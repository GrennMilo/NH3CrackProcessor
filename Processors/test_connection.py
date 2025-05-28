import time
import requests
import sys

def test_connection(url, max_attempts=5, delay=2):
    """Test connection to a URL with multiple attempts"""
    print(f"Testing connection to {url}...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Attempt {attempt}/{max_attempts}...")
            response = requests.get(url, timeout=5)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Content: {response.text}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            if attempt < max_attempts:
                print(f"Waiting {delay} seconds before next attempt...")
                time.sleep(delay)
    
    return False

if __name__ == "__main__":
    # Test connection to the basic app
    basic_app_url = "http://localhost:8081/ping"
    print("\n=== Testing connection to basic app ===")
    success = test_connection(basic_app_url)
    
    # Try the original app as well
    orig_app_url = "http://localhost:8080/"
    print("\n=== Testing connection to original app ===")
    success_orig = test_connection(orig_app_url)
    
    if not success and not success_orig:
        print("\nBoth apps appear to be unavailable.")
        sys.exit(1)
    elif success and not success_orig:
        print("\nBasic app is running, but original app is not.")
    elif not success and success_orig:
        print("\nOriginal app is running, but basic app is not.")
    else:
        print("\nBoth apps are running.") 