"""
Run API server and execute tests
"""
import subprocess
import time
import sys
import requests

# Start the API server
print("Starting API server...")
server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(3)

# Check if server is running
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print("✓ API server is running\n")
except:
    print("✗ Failed to start API server")
    server_process.kill()
    sys.exit(1)

# Run the test script
print("Running tests...\n")
test_process = subprocess.run([sys.executable, "test_all_apis.py"])

# Cleanup
print("\nShutting down API server...")
server_process.kill()
print("Done!")
