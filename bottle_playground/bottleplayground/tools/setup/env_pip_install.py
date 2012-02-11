"""
Setup script for pip install'ing eggs into the current virtualenv.
This avoids writing a shell/cmd script to activate prior to pip install.
This sources the virtualenv's activate_this.py to ensure pip install into the right env.
"""
__author__ = 'Michael Lossos <mlossos@pobox.com>'

import sys
import os.path
import subprocess


def process_args(args):
    """
    args: like sys.argv, where args[0] is the name of the currently running module.
    """
    if len(args) < 4:
        raise Exception('usage: {} path/to/virtualenv/Scripts/activate_this.py path/to/virtualenv/Scripts/pip path/to/requirements.txt'.format(sys.argv[0]))
    return { 'activate_path': args[1], 'pip_path': args[2], 'requirements_txt': args[3] }

def validate_paths(args):
    for k, v in args.iteritems():
        print 'Using: {}'.format(v)
        if not os.path.exists(v):
            raise Exception('Failed to find file for {}: {}'.format(k, v))

def run_pip_install(sys_argv):
    args = process_args(sys_argv)
    validate_paths(args)

    # Activate virtualenv for the current interpreter.
    execfile(args['activate_path'], dict(__file__=args['activate_path']))

    # pip install -U -r requirements.txt
    subprocess.check_call([args['pip_path'], 'install', '--upgrade', '--requirement', args['requirements_txt']])
    
    # TODO Additional python scripted setup goes here.
    
    print 'SUCCESS: pip install complete.'

if __name__ == '__main__':
    run_pip_install(sys.argv)

