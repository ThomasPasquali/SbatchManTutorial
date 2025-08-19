# SbatchMan Hands-on Tutorial

Clone this repo on both your local machine and cluster.

First, ensure to have a Python virtual environment to install `SbatchMan`, `Jupiter` and other dependencies like `matplotlib`.

If you don't already have it, run:
```bash
python3 -m venv .venv # Create virtual environment into `.venv` directory
source .venv/bin/activate # If you change terminal, this must be run again 
pip install -r requirements.txt # Install Python packages
pipx install sbatchman # Install SbatchMan CLI 
```

> **! Important !**  
> Run these commands on **both** your **local machine** and **remote cluster**.

*Locally, use VS Code to setup Jupiter Server.*

*If you use fancy VS Code features like `Remote - SSH` this will work on the remote cluster as well.*

### Now, for the tutorial, please refer to [`tutorial.ipynb`](./tutorial.ipynb)