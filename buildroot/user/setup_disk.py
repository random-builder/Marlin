#!/usr/bin/env python

import os
import time
import logging
import paramiko
import argparse
import functools
import subprocess

logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(levelname)-8s %(message)s',
)

parser = argparse.ArgumentParser()
parser.add_argument('--host_uri', dest="host_uri", default="pi@octopi2")
parser.add_argument('--disk_label', dest="disk_label", default="MKS-BASE")
parser.add_argument('--firmware_path', dest="firmware_path", required=True)

params = parser.parse_args()

for key, value in vars(params).items():
    print(f"{key}={value}")


def trace(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        id = func.__name__
        logger = logging.getLogger(id)
        try:
            logger.info(f"{id}")
            return func(*args, *kwargs)
        except Exception as error:
            logger.exception(error)
            raise error

    return wrapper


@trace
def disk_find(label=params.disk_label) -> str:
    result = ssh(f"sudo lsblk -n -l -o name,label | grep {label} | head -n 1")
    if result.returncode == 0:
        stdout = result.stdout
        stdparts = stdout.split()
        if len(stdparts) == 2:
            disk_name = stdparts[0].decode('utf-8')
            return disk_name
        else:
            return None
    else:
        return None


@trace
def disk_has_point(disk_point):
    result = ssh(f"mountpoint {disk_point}")
    return result.returncode == 0


@trace
def disk_point_create(disk_point):
    ssh(f"mkdir -p {disk_point}")


@trace
def disk_point_delete(disk_point):
    ssh(f"rm -rf {disk_point}")


@trace
def disk_file_copy(local_path, remote_dir):
    local_base = os.path.basename(local_path)
    source_path = local_path
    target_path = os.path.join(remote_dir, local_base)
    scp(source_path, target_path)


@trace
def disk_point_mount(disk_point, disk_path):
    if disk_has_point(disk_point) is False:
        ssh(f"sudo mount {disk_path} {disk_point} -o uid=$USER,gid=$USER")


@trace
def disk_point_unmount(disk_point):
    if disk_has_point(disk_point) is True:
        ssh(f"sudo umount {disk_point}")


@trace
def disk_setup(disk_name, firmware_path=params.firmware_path):
    disk_path = f"/dev/{disk_name}"
    disk_point = f"/tmp/disk-setup/{disk_name}"
    disk_point_unmount(disk_point)
    disk_point_create(disk_point)
    disk_point_mount(disk_point, disk_path)
    disk_file_copy(firmware_path, disk_point)
    disk_point_unmount(disk_point)
    disk_point_delete(disk_point)


def ssh_x(script, host_uri=params.host_uri, check=True, stdin=None):
    command = ["ssh", host_uri, script]
    result = subprocess.run(command, check=check,
        shell=False, stdin=stdin,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )    
    return result


class Result() :
    returncode = 0
    stdout = ""
    stderr = ""


def ssh(script):
    stdin, stdout, stderr = ssh_client.exec_command(script)
    stdin.flush()
    result = Result()
    result.returncode = stdout.channel.recv_exit_status()
    result.stdout = stdout.read()
    result.stderr = stderr.read()
    return result


def scp_x(source_path, target_path, host_uri=params.host_uri, check=True, stdin=None):
    source_uri = f"{source_path}"
    target_uri = f"{host_uri}:{target_path}"
    command = ["scp", source_uri, target_uri]
    result = subprocess.run(command, check=check,
        shell=False, stdin=stdin,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )    
    return result


def scp(source_path, target_path):
    ftp_client = ssh_client.open_sftp()
    ftp_client.put(source_path, target_path)
    ftp_client.close()
    

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(username="pi", hostname="octopi2",)

disk_name = disk_find()
print(f"disk_name={disk_name}")

if disk_name is None:
    sys.exit()

disk_setup(disk_name)
