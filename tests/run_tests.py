#!/usr/bin/env python
"""
Convenience script to run the complete test suite.

Usage:
    python tests/run_tests.py                    # Run all tests
    python tests/run_tests.py -v                 # Verbose output
    python tests/run_tests.py --cov              # With coverage
    python tests/run_tests.py tests/test_models.py  # Specific file
"""

import sys
import pytest


def main():
    """Run pytest with sensible defaults."""
    args = sys.argv[1:] if len(sys.argv) > 1 else ["tests", "-v"]
    exit_code = pytest.main(args)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
