#!/usr/bin/env python3
"""
Test runner script for the Content Creator API.

This script provides a convenient way to run tests with different configurations
and generate reports.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for Content Creator API")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--html", action="store_true", help="Generate HTML test report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fast", action="store_true", help="Skip slow tests")
    parser.add_argument("--file", help="Run tests from specific file")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    
    args = parser.parse_args()
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        if not run_command("pip install -r requirements-test.txt", "Installing test dependencies"):
            sys.exit(1)
    
    # Build pytest command
    pytest_cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        pytest_cmd.append("-v")
    else:
        pytest_cmd.append("-q")
    
    # Add coverage if requested
    if args.coverage:
        pytest_cmd.extend(["--cov=.", "--cov-report=term-missing", "--cov-report=html"])
    
    # Add HTML report if requested
    if args.html:
        pytest_cmd.extend(["--html=test_report.html", "--self-contained-html"])
    
    # Add test markers
    if args.unit:
        pytest_cmd.extend(["-m", "unit"])
    elif args.integration:
        pytest_cmd.extend(["-m", "integration"])
    
    # Skip slow tests if requested
    if args.fast:
        pytest_cmd.extend(["-m", "not slow"])
    
    # Add specific file if requested
    if args.file:
        pytest_cmd.append(args.file)
    else:
        pytest_cmd.extend(["test_main.py", "test_agent.py"])
    
    # Run the tests
    command = " ".join(pytest_cmd)
    success = run_command(command, "Running tests")
    
    if success:
        print("\n🎉 All tests completed successfully!")
        
        # Show coverage report if generated
        if args.coverage and os.path.exists("htmlcov/index.html"):
            print("\n📊 Coverage report generated: htmlcov/index.html")
        
        # Show HTML report if generated
        if args.html and os.path.exists("test_report.html"):
            print("📋 HTML test report generated: test_report.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
