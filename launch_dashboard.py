"""
MESSAGE-IX Dashboard Launcher
Quick launcher for the Streamlit dashboard
"""

import subprocess
import sys
from pathlib import Path

def launch_dashboard():
    """Launch the MESSAGE-IX Streamlit dashboard"""
    
    print("Launching MESSAGE-IX Energy System Dashboard...")
    print("Starting Streamlit server...")
    
    # Get the dashboard file path
    dashboard_path = Path(__file__).parent / "dashboard.py"
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port", "8501",
            "--server.headless", "false",
            "--server.enableCORS", "false"
        ])
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        print("Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    launch_dashboard()