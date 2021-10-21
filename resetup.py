import argparse
arg=argparse.ArgumentParser()
arg.add_argument('--version',type=str)
args=arg.parse_args()
if args.version:
    print(open('setup.py').read().replace('0.1.6',args.version))