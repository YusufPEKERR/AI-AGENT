#!/usr/bin/env python3
\"\"\"Self-test script for AI Agent toolkit verification\"\"\"
import sys
import json
import subprocess
import platform

def test_python():
    print(f"✓ Python {sys.version}")
    return True

def test_tools():
    for tool in ['git', 'docker', 'kubectl']:
        try:
            result = subprocess.run([tool, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✓ {tool}: {result.stdout.strip()}")
            else:
                print(f"✗ {tool}: not found")
        except:
            print(f"✗ {tool}: not found")
    return True

def test_platform():
    print(f"✓ Platform: {platform.system()} {platform.release()}")
    print(f"✓ Architecture: {platform.machine()}")
    return True

if __name__ == "__main__":
    print("=== SELF-TEST RESULTS ===")
    test_python()
    test_platform()
    test_tools()
    print("=== SELF-TEST COMPLETE ===")
