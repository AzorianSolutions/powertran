#!/usr/bin/env bash

# Add sudo to elevated commands when not running as root already
CMD_PREFIX=
if [ ! "$EUID" -eq 0 ]; then
  CMD_PREFIX=sudo
fi

# Move to the project's root directory if not already there
CURRENT_PATH=$(dirname "$(readlink -f "$0")")
PARENT_DIRECTORY=$(basename $CURRENT_PATH)

if [ "$PARENT_DIRECTORY" == 'bin' ]; then
  cd "$CURRENT_PATH/.."
fi

# Install Python3 if not already installed
if [ "$(dpkg -l | awk '/python3/ {print }'|wc -l)" -lt 1 ]; then
  $CMD_PREFIX apt update && $CMD_PREFIX apt install -y python3
else
  echo "Skipping Python3 installation, already installed."
fi

# Install Python3 venv package if not already installed
if [ "$(dpkg -l | awk '/python3-venv/ {print }'|wc -l)" -lt 1 ]; then
  $CMD_PREFIX apt update && $CMD_PREFIX apt install -y python3-venv
else
  echo "Skipping Python3 venv installation, already installed."
fi

# Load the environment configuration
source .env

# Setup the Python virtual environment
/usr/bin/env python3 -m venv ./venv

# Load the Python virtual environment
source venv/bin/activate

# Install the required pip modules based on the configuration in setup.py
pip install --editable .

echo ""
echo "The environment is ready to run the application!"
echo ""
echo "Please run the \"powertran\" command to get started."
echo ""