#!/usr/bin/env python3
"""
Final test script for Nala-Fedora
Verifies all core functionality before GitHub upload
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(name, command, expected_return_codes=[0]):
    """Run a test command and report results."""
    print(f"🧪 Testing {name}...")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode in expected_return_codes:
            print(f"   ✅ {name}: PASSED")
            return True
        else:
            print(f"   ❌ {name}: FAILED (return code: {result.returncode})")
            if result.stderr:
                print(f"      Error: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"   ❌ {name}: ERROR - {e}")
        return False

def main():
    """Main test function."""
    print("🎯 NALA-FEDORA FINAL VERIFICATION TEST")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Set environment for English output
    env = os.environ.copy()
    env.update({
        "LANG": "en_US.UTF-8",
        "LC_ALL": "en_US.UTF-8",
        "_NALA_COMPLETE": "1"
    })
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Python module imports
    total_tests += 1
    test_cmd = [
        "python3", "-c",
        "import sys; sys.path.insert(0, '.'); "
        "from nala.dnf_interface import DNFCache, run_dnf_command; "
        "from nala.cache import Cache; "
        "print('All imports successful')"
    ]
    if run_test("Python imports", test_cmd):
        tests_passed += 1
    
    # Test 2: DNF command execution
    total_tests += 1
    test_cmd = [
        "python3", "-c",
        "import sys; sys.path.insert(0, '.'); "
        "from nala.dnf_interface import run_dnf_command; "
        "result = run_dnf_command(['--version']); "
        "print(f'DNF version: {result.stdout.split()[2] if result.stdout else \"Unknown\"}')"
    ]
    if run_test("DNF interface", test_cmd):
        tests_passed += 1
    
    # Test 3: English wrapper script
    total_tests += 1
    if run_test("English wrapper help", ["./nala-fedora-en", "help"]):
        tests_passed += 1
    
    # Test 4: System test via wrapper
    total_tests += 1
    if run_test("System functionality test", ["./nala-fedora-en", "test"]):
        tests_passed += 1
    
    # Test 5: Package search
    total_tests += 1
    if run_test("Package search", ["./nala-fedora-en", "search", "curl"], [0, 1]):
        tests_passed += 1
    
    # Test 6: Mirror speed test script
    total_tests += 1
    test_cmd = ["python3", "fedora-fetch-simple.py"]
    # Simulate 'n' input for no repo file creation
    try:
        result = subprocess.run(
            test_cmd,
            input="n\n",
            text=True,
            capture_output=True,
            timeout=60,
            env=env
        )
        if "Nala-Fedora Mirror Speed Test" in result.stdout:
            print("   ✅ Mirror speed test: PASSED")
            tests_passed += 1
        else:
            print("   ❌ Mirror speed test: FAILED")
    except Exception as e:
        print(f"   ❌ Mirror speed test: ERROR - {e}")
    
    total_tests += 1
    
    # Test 7: Check essential files exist
    total_tests += 1
    essential_files = [
        "README.md",
        "CONTRIBUTING.md", 
        "LICENSE",
        "pyproject.toml",
        "nala-fedora-en",
        "nala/dnf_interface.py"
    ]
    
    all_files_exist = True
    for file in essential_files:
        if not Path(file).exists():
            print(f"   ❌ Missing file: {file}")
            all_files_exist = False
    
    if all_files_exist:
        print("   ✅ Essential files check: PASSED")
        tests_passed += 1
    else:
        print("   ❌ Essential files check: FAILED")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Nala-Fedora is ready for GitHub upload!")
        print("\n🚀 Next steps:")
        print("   1. Follow instructions in GITHUB_UPLOAD_INSTRUCTIONS.md")
        print("   2. Upload to GitHub as a fork of volitank/nala")
        print("   3. Set repository description and topics")
        print("   4. Enable Issues and Wiki features")
        return 0
    else:
        print("❌ Some tests failed. Please review before uploading.")
        return 1

if __name__ == "__main__":
    sys.exit(main())