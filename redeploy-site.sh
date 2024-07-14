#!/bin/bash


PROJECT_DIR="/root/Ahsan-folio"
VENV_ACTIVATE="$PROJECT_DIR/python3-virtualenv/bin/activate"


if ! command -v tmux &> /dev/null; then
    echo "tmux command not found. Installing tmux..."

    sudo yum install tmux   

fi


echo "Navigating to the project directory..."
cd "$PROJECT_DIR" || { echo "Failed to navigate to project directory"; exit 1; }


echo "Fetching the latest changes from the GitHub repository..."
git fetch && git reset origin/main --hard || { echo "Failed to fetch latest changes"; exit 1; }


echo "Activating the Python virtual environment and installing dependencies..."
source "$VENV_ACTIVATE" || { echo "Failed to activate virtual environment"; exit 1; }
pip install -r requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }


echo "Restarting myportfolio service..."
sudo systemctl restart myportfolio.service || { echo "Failed to restart myportfolio service"; exit 1; }

echo "Deployment script executed successfully!"
