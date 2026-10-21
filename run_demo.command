#!/bin/zsh
# Double-click on macOS, or run ./run_demo.command from a terminal.
cd -- "${0:A:h}" || exit 1
if [[ ! -x .venv/bin/python ]]; then
  print 'Create the project environment using the instructions in README.md first.'
  read '?Press Return to close.'
  exit 1
fi
print 'Open http://127.0.0.1:8765 after the server starts. Stop with Ctrl+C.'
exec .venv/bin/python -m intention_grounding.dashboard "$@"
