import argparse
import re
arg = argparse.ArgumentParser()
arg.add_argument('--version', type=str)
args = arg.parse_args()
if args.version:
    new = open('setup.py').read().replace(
        '0.1.6',
        re.search(r'\/?([0-9][0-9A-Za-z\.]+)', args.version).group(1)
    )
    with open('setup.py', 'w') as fil:
        print(new)
        fil.write(new)
