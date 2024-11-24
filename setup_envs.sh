#!/bin/bash
set -e

setup_venv() {
    local repo_dir=$1
    echo "setting up virtual environment in $repo_dir..."

    cd "$repo_dir"
    python3 -m venv venv
    source venv/bin/activate

    if [[ -f "setup.py" ]]; then
        echo "installing dependencies using setup.py..."
        pip install --upgrade pip
        pip install -e .
    else
        echo "setup.py not found. skipping installation."
    fi

    deactivate
    cd - > /dev/null
}

# Set up virtual environments for each repository
echo "starting setup for vr_kitchen..."
setup_venv "vr_kitchen"

echo "starting setup for fov_aware_planner..."
setup_venv "fov_aware_planner"

echo "virtual environments setup complete!"