import subprocess, pathlib

def run_command(cmd):
    print("* " + " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        print(out.stderr)
        print(f"'{" ".join(cmd)}' failed with error code {out.returncode}")
        exit(1)
    print(out.stdout, end="")

print("Creating virtual enviornment..")
run_command(["python3", "-m" "venv", ".venv"])
print("Installing dependencies")
run_command([".venv/bin/pip", "install", "-r", "requirements.txt"])
print("Done!")

print("Creating ~/.minige")
with open(pathlib.Path.home().joinpath(".minige").absolute(), "w") as f:
    f.write(str(pathlib.Path(".venv").absolute()))
print("Copying launcher (./minige) to /usr/bin. (root required)")
run_command(["sudo", "python3", "setup2.py"])