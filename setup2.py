import shutil, os
shutil.copy("minige", "/usr/bin/minige")
os.chmod("/usr/bin/minige", 0o755)