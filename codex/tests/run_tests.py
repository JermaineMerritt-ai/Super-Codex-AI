#!/usr/bin/env python3
"""
Test runner script for Super-Codex-AI
Provides various options for running different test suites.
"""

import argparse
import sys
import subprocess
from pathlib import Path
from typing import List, Optional


def run_command(cmd: List[str], description: str) -> int:
    """Run a command and return the exit code."""
    print(f"\n🔄 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
        else:
            print(f"❌ {description} failed with exit code {result.returncode}")
        return result.returncode
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return 1


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Run Super-Codex-AI test suites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py --unit             # Run only unit tests
  python run_tests.py --integration      # Run only integration tests
  python run_tests.py --performance      # Run performance tests
  python run_tests.py --fast             # Run fast tests only
  python run_tests.py --verbose          # Run with verbose output
  python run_tests.py --coverage         # Run with coverage report
  python run_tests.py --file test_rag.py # Run specific test file
        """
    )
    
    # Test selection options
    parser.add_argument(
        "--unit", 
        action="store_true",
        help="Run unit tests only"
    )
    parser.add_argument(
        "--integration", 
        action="store_true",
        help="Run integration tests only"
    )
    parser.add_argument(
        "--performance", 
        action="store_true",
        help="Run performance tests only"
    )
    parser.add_argument(
        "--fast", 
        action="store_true",
        help="Run fast tests only (exclude slow tests)"
    )
    parser.add_argument(
        "--file", 
        type=str,
        help="Run specific test file"
    )
    parser.add_argument(
        "--function", 
        type=str,
        help="Run specific test function (use with --file)"
    )
    
    # Output options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet output"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Run with coverage report"
    )
    parser.add_argument(
        "--html-coverage", 
        action="store_true",
        help="Generate HTML coverage report"
    )
    
    # Execution options
    parser.add_argument(
        "--parallel", "-n",
        type=int,
        help="Run tests in parallel (requires pytest-xdist)"
    )
    parser.add_argument(
        "--failfast", "-x",
        action="store_true",
        help="Stop on first failure"
    )
    parser.add_argument(
        "--pdb",
        action="store_true",
        help="Drop into debugger on failures"
    )
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test directory
    test_dir = Path(__file__).parent
    
    # Test selection
    if args.unit:
        cmd.extend(["-m", "not integration and not performance"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.performance:
        cmd.extend(["-m", "performance"])
    elif args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Specific file or function
    if args.file:
        file_path = test_dir / args.file
        if not file_path.exists():
            print(f"❌ Test file not found: {file_path}")
            return 1
        
        if args.function:
            cmd.append(f"{file_path}::{args.function}")
        else:
            cmd.append(str(file_path))
    else:
        cmd.append(str(test_dir))
    
    # Output options
    if args.verbose:
        cmd.append("-v")
    elif args.quiet:
        cmd.append("-q")
    
    # Coverage options
    if args.coverage or args.html_coverage:
        cmd.extend(["--cov=engine", "--cov=scrolls", "--cov-report=term"])
        if args.html_coverage:
            cmd.append("--cov-report=html")
    
    # Execution options
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    if args.failfast:
        cmd.append("-x")
    
    if args.pdb:
        cmd.append("--pdb")
    
    # Additional pytest options
    cmd.extend([
        "--tb=short",
        "--color=yes"
    ])
    
    # Print summary
    print("🧪 Super-Codex-AI Test Runner")
    print("=" * 60)
    
    if args.unit:
        test_type = "Unit Tests"
    elif args.integration:
        test_type = "Integration Tests"
    elif args.performance:
        test_type = "Performance Tests"
    elif args.fast:
        test_type = "Fast Tests"
    elif args.file:
        test_type = f"Specific File: {args.file}"
    else:
        test_type = "All Tests"
    
    print(f"Test Type: {test_type}")
    print(f"Test Directory: {test_dir}")
    
    if args.coverage:
        print("Coverage: Enabled")
    
    if args.parallel:
        print(f"Parallel Workers: {args.parallel}")
    
    # Run the tests
    exit_code = run_command(cmd, f"Running {test_type}")
    
    # Summary
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("🎉 All tests passed!")
    else:
        print(f"💥 Tests failed with exit code {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())