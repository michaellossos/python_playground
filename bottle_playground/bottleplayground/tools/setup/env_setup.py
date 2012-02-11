"""
"""
import argparse
import subprocess
import os
import sys

__author__ = 'Michael Lossos <mlossos@pobox.com>'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest_env_path', default='env/dev', help='relative or absoluate path to the dest virtualenv dir')
    parser.add_argument('--site-packages', default=False, help='when enabled, do not use --no-site-packages with virtualenv')
    parser.add_argument('--requirements', default='requirements.txt', help='path to requirements.txt for pip')
    return parser.parse_args()

def prepare_env_dir(dest_env_path):
    dest_env_path = os.path.abspath(dest_env_path)
    if os.path.exists(dest_env_path):
        raise Exception('ERROR: virtualenv target path already exists: {}'.format(dest_env_path)
            + '\nDelete it first before running setup.')
    parent_dir = os.path.dirname(dest_env_path)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    return dest_env_path

def create_virtualenv(dest_env_path, site_packages=False):
    args = ['virtualenv', dest_env_path]
    if not site_packages:
        args.insert(1, '--no-site-packages')
    print 'Launching: {}'.format(' '.join(args))
    subprocess.check_call(args)

def get_env_scripts_path(dest_env_path):
    return os.path.abspath(dest_env_path + '/Scripts')

def discover_env_paths(dest_env_path, requirements_txt):
    scripts_path = get_env_scripts_path(dest_env_path)
    activate_this = scripts_path + '/activate_this.py'
    pip = scripts_path + '/pip'
    if not os.path.exists(pip):
        # Windows
        pip = scripts_path + '/pip.exe'
    req = os.path.abspath(requirements_txt)
    if not os.path.exists(req):
        req = '{}/{}'.format(os.path.dirname(__file__), os.path.basename(req))
        print 'Requirements file: {} does not exist. Guessing new path: {}'.format(requirements_txt, req)
    paths = [activate_this, pip, req]
    paths = [os.path.abspath(p) for p in paths]
    for p in paths:
        if not os.path.exists(p):
            raise Exception('Failed to find file: {}'.format(p))
    return paths

def import_env_pip_install():
    print 'Discovering env_pip_install.py'
    try:
        # First try on the current sys.path
        import env_pip_install
    except ImportError:
        # Try again alongside the current script.
        p = os.path.dirname(__file__)
        sys.path.append(p)
        import env_pip_install

def run_pip_install(paths):
    import_env_pip_install()
    import env_pip_install  # Prevent IDE warnings when referencing env_pip_install
    sys_paths = [sys.argv[0]]
    sys_paths.extend(paths)
    env_pip_install.run_pip_install(sys_paths)

def get_activate_path(dest_env_path):
    activate_script = '{}/{}'.format(get_env_scripts_path(dest_env_path), 'activate')
    if not os.path.exists(activate_script):
        # Windows
        activate_script += '.bat'
    if not os.path.exists(activate_script):
        print 'WARNING: Failed to find activate script: {}'.format(activate_script)
    return os.path.abspath(activate_script)

def create_activate_wrapper(dest_env_path):
    activate_script = get_activate_path(dest_env_path)
    print 'Activate script: {}'.format(activate_script)
    output_win_cmd = activate_script.endswith('.bat')

    # If these shell/cmd scripts become larger, move them out to a template file.
    output_filename = 'myenv'
    comment_text = 'Wapper for virtualenv activate'
    script_contents = '#!/bin/bash\r\n# {}\r\nsource {}\n'.format(comment_text, activate_script)
    if output_win_cmd:
        # Windows
        output_filename += '.cmd'
        script_contents = ':: {}\r\ncall {}\r\n'.format(comment_text, activate_script)

    with open(output_filename, 'w') as output_file:
        output_file.write(script_contents)
    print 'Created activate wrapper: {}'.format(output_filename)

def main():
    ARGS = parse_args()

    dest_env_path = prepare_env_dir(ARGS.dest_env_path)
    create_virtualenv(dest_env_path)
    paths = discover_env_paths(dest_env_path, ARGS.requirements)
    run_pip_install(paths)
    create_activate_wrapper(dest_env_path)

if __name__ == '__main__':
    main()