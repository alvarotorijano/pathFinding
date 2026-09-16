"""
Entry point for the maze search framework CLI.

Usage:
    python -m labyrinth generate --help
    python -m labyrinth run --help
    python -m labyrinth list --help
"""

import sys
from labyrinth.cli.runner import main

if __name__ == "__main__":
    main()
