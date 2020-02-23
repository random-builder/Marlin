#
# shared build functions
#

import os
import time
import subprocess

# user settings
environment = "<board-hardware>"
printer_name = "USER_<vendor-name>_<printer-name>"

# script location
this_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(this_dir)
root_dir = os.path.dirname(base_dir)


def platformio_run():

    user_stamp = time.strftime("%Y-%m-%d")
    # user_stamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    build_dir = os.path.join(root_dir, ".pioenvs", printer_name)
    build_flags = f"-D{printer_name} -DUSER_STAMP={user_stamp}"

    script_setup = os.path.join(this_dir, "setup.py")

    print(f"environment={environment}")
    print(f"printer_name={printer_name}")
    print(f"build_dir={build_dir}")
    print(f"build_flags={build_flags}")
    print(f"user_stamp={user_stamp}")

    # use per-printer build location
    os.environ['PLATFORMIO_BUILD_DIR'] = build_dir

    # activate configuration override
    os.environ['PLATFORMIO_BUILD_FLAGS'] = build_flags

    # expose for scripts
    os.environ['PLATFORMIO_ENVIRONMENT'] = f"{environment}"

    # provide custom scripts
    os.environ['PLATFORMIO_EXTRA_SCRIPTS'] = f"{script_setup}"

    # invoke build
    platformio = f"{root_dir}/.env/bin/platformio"
    command_build = [platformio, "run", "--environment", environment, "--project-dir", root_dir, "--target", "setup"]
    subprocess.run(command_build)
