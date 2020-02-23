#!/usr/bin/env python

import os
import sys
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
parser.add_argument('--user_name', dest="user_name", default="pi")
parser.add_argument('--host_name', dest="host_name", default="octopi2")
parser.add_argument('--disk_label', dest="disk_label", default="MKS-BASE")
parser.add_argument('--firmware_path', dest="firmware_path", required=True)

params = parser.parse_args()

for key, value in vars(params).items():
    print(f"{key}={value}")


def trace(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_id = func.__name__
        logger = logging.getLogger(func_id)
        try:
            logger.info(f"{func_id}")
            return func(*args, **kwargs)
        except Exception as error:
            logger.exception(error)
            raise error

    return wrapper


@trace
def disk_find(label:str) -> str:
    result = ssh(f"sudo lsblk -n -l -o name,label | grep {label} | head -n 1")
    if result.returncode == 0:
        stdparts = result.stdout.split()
        if len(stdparts) == 2:
            disk_name = stdparts[0].decode('utf-8')
            return disk_name
        else:
            return None
    else:
        return None


@trace
def disk_has_point(disk_point):
    result = ssh(f"cat /proc/mounts | grep {disk_point}")
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
def disk_setup(disk_name, firmware_path):
    disk_path = f"/dev/{disk_name}"
    disk_point = f"/tmp/disk-setup/{disk_name}"
    disk_point_unmount(disk_point)
    disk_point_create(disk_point)
    disk_point_mount(disk_point, disk_path)
    disk_file_copy(firmware_path, disk_point)
    disk_point_unmount(disk_point)
    disk_point_delete(disk_point)


def shell(script):
    result = subprocess.run(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result


def has_host(host_name):
    result = shell(f"ping -c 1 {host_name}")
    return result.returncode == 0


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


def scp(source_path, target_path):
    ftp_client = ssh_client.open_sftp()
    ftp_client.put(source_path, target_path)
    ftp_client.close()

#
#
#


if not has_host(params.host_name):
    print(f"missing host={params.host_name}")
    sys.exit()

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(username=params.user_name, hostname=params.host_name,)

disk_name = disk_find(params.disk_label)

if disk_name is None:
    print(f"missing disk={params.disk_label}")
    sys.exit()

disk_setup(disk_name, params.firmware_path)
