import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--dir", type=str)
parser.add_argument("--args", type=str)

args = parser.parse_args()

subprocess.run(f'COMMANDLINE_ARGS="{args.args}" {sys.executable} launch.py', shell=True, cwd=args.dir)
