import argparse
import re
arg=argparse.ArgumentParser()
arg.add_argument('--version',type=str)
args=arg.parse_args()
if args.version:
    print(open('setup.py').read().replace('0.1.6',re.search(r'\/?([0-9\.]+)',args.version).group(1)))