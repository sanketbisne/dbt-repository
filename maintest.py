import os
import subprocess

# Get the script name from environment variable
script_name = os.getenv("PROJECT_RUN")
if not script_name:
    print("❌ PROJECT_RUN environment variable is not set.")
    exit(1)

script_path = f"agg_data_storage_dbt/project_run_scripts/{script_name}.sh"

print(f"▶️ Running script: {script_path}")

try:
    proc = subprocess.run(
        ["bash", script_path],
        capture_output=True,
        text=True
    )
    print("=== STDOUT ===")
    print(proc.stdout)
    print("=== STDERR ===")
    print(proc.stderr)
    if proc.returncode == 0:
        print("✅ Script executed successfully.")
    else:
        print(f"❌ Script failed with exit code {proc.returncode}")
        exit(proc.returncode)
except FileNotFoundError:
    print(f"❌ Script not found: {script_path}")
    exit(1)
except Exception as e:
    print("❌ Unexpected error:", str(e))
    exit(1)
