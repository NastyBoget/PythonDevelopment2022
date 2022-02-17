import os
import subprocess
import sys
import tempfile
import venv

if __name__ == "__main__":
    args = sys.argv[1:]
    with tempfile.TemporaryDirectory() as tmpdir:
        venv.create(tmpdir, with_pip=True)
        env_path = os.path.join(tmpdir, "bin")
        pip_path = os.path.join(env_path, "pip")
        python_path = os.path.join(env_path, "python3")
        subprocess.run([pip_path, "install", "pyfiglet"], capture_output=True)
        args = [python_path, "-m", "figdate"] + args
        subprocess.run(args)
