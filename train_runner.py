import sys
import subprocess
import os

print(f"Python executable: {sys.executable}")
print(f"Working Directory: {os.getcwd()}")

try:
    result = subprocess.run([r"myvenv\Scripts\python.exe", "model_training.py"], capture_output=True, text=True)
    with open("runner_output.txt", "w", encoding="utf-8") as f:
        f.write(f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nEXIT:\n{result.returncode}")
    print("Runner completed successfully.")
except Exception as e:
    with open("runner_output.txt", "w", encoding="utf-8") as f:
        f.write(str(e))
    print(f"Runner failed: {e}")
