import subprocess
import os

def run_dashboard():
    port = os.environ.get("DASHBOARD_PORT", "8501")
    print(f"🚀 Launching Streamlit dashboard on port {port}...")
    subprocess.Popen(["streamlit", "run", "dashboard_ui.py", "--server.port", port])
