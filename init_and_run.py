import os
import secrets
import subprocess
import sys
import signal
import time

def create_env_file():
    if not os.path.exists(".env"):
        print("--- Environment Setup ---")
        groq_key = input("Enter your GROQ_API_KEY: ")
        secret_key = secrets.token_hex(32)
        with open(".env", "w") as f:
            f.write(f"GROQ_API_KEY={groq_key}\n")
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write("DATABASE_URL=sqlite:///./database.db\n")
        print(".env file created.")
    else:
        print(".env file already exists.")

def run_uv_sync():
    print("--- Syncing Dependencies ---")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("Dependencies synced successfully.")
    except FileNotFoundError:
        print("Error: 'uv' not found. Please install it first.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: 'uv sync' failed.")
        sys.exit(1)

def main():
    create_env_file()
    run_uv_sync()

    print("--- Starting PracticeAI ---")
    
    # Start Backend
    backend_proc = subprocess.Popen(
        ["uv", "run", "uvicorn", "backend.app.main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Start Frontend
    frontend_proc = subprocess.Popen(
        ["uv", "run", "streamlit", "run", "frontend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    def signal_handler(sig, frame):
        print("\nStopping PracticeAI...")
        backend_proc.terminate()
        frontend_proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("Backend running at http://localhost:8000")
    print("Frontend running at http://localhost:8501")
    print("Press Ctrl+C to stop.")

    # Simple loop to keep main thread alive and print outputs
    while True:
        # We could print output from subprocesses here if desired, 
        # but it might be messy with two processes.
        # Let's just wait.
        time.sleep(1)

if __name__ == "__main__":
    main()
