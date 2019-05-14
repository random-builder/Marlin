#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--disk-label', dest="disk_label", default="MKS-BASE")

args = parser.parse_args()

print(f"disk_label={args.disk_label}")

