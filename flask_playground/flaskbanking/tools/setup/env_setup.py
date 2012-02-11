import sys
import os.path
import traceback
import subprocess

__author__ = 'Michael Lossos'
'''
Setup script (the python part) for creating pip install'ing eggs into the current interpreter.
'''

def main():
    if len(sys.argv) < 3:
        raise Exception('usage: {} path/to/virtualenv/activate_this.py path/to/virtualenv/Scripts/pip'.format(sys.argv[0]))
    activate_path = sys.argv[1]
    pip_path = sys.argv[2]
    
    # Activate virtualenv for the current interpreter.
    execfile(activate_path, dict(__file__=activate_path))
    
    requirements_txt = '{}/requirements.txt'.format(os.path.dirname(__file__))
    print 'Using requirements: {}'.format(requirements_txt)
    
    # pip install -U -r requirements.txt
    subprocess.check_call([pip_path, 'install', '--upgrade', '--requirement', requirements_txt])
    
    # TODO Additional python scripted setup goes here.
    
    print 'pip install complete.'

if __name__ == '__main__':
    main()

