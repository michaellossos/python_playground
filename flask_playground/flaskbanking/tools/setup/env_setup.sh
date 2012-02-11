#!/bin/bash
#
# Setup script for creating a virtualenv and pip install'ing eggs.
# @Author Michael Lossos
#


#set -x

##########################################################
# Shared env vars
# TODO Move to shared env include
# 
export DEPLOY_TYPE=dev
export TOOLS_REL_PATH=flaskbanking/tools/setup

##########################################################
# Shared functions
# TODO Move to shared env include
#

exit_on_error() {
    error_message="$1"     
    echo "FATAL ERROR. Aborting. Cause: ${error_message}"
    exit 1
}


# Run via exec to grab echo output
echo_norm_path() {
    pdir="$1"
    has_cygpath=`which cygpath`
    if [ -n "${has_cygpath}" ]; then
        pdir=`cygpath --mixed ${pdir}`
    fi
    # TODO Other path normalization
    
    echo "${pdir}"
    return 0
}

##########################################################
# Functions for this script
#

# Infer top level projet dir relative from where this current script is run.
infer_project_dir() {
    attempt_dirs="./flaskbanking ../../../flaskbanking"
    for pdir in ${attempt_dirs}; do
        if [ -d ${pdir} ]; then
            # TODO Convert path to absolute
            export PROJECT_BASE_DIR="${pdir}/.."
            break
        fi
    done
}

echo_activate() {
    _norm_scripts_dir=`echo_norm_path "${VIRTUALENV_TARGET_DIR}/Scripts"`
    echo "Activate scripts in ${_norm_scripts_dir}"
    ls "${_norm_scripts_dir}"/activate*
}

prepare_dirs() {
    # TODO Set PROJECT_BASE_DIR from a top level shell script
    if [ -z "${PROJECT_BASE_DIR}" ]; then
        infer_project_dir
    fi
    echo "PROJECT_BASE_DIR=${PROJECT_BASE_DIR}"
    
    if [ ! -d "${PROJECT_BASE_DIR}" ]; then
        echo "ERROR: the env var PROJECT_BASE_DIR must be a valid directory. export PROJECT_BASE_DIR=\`pwd\`  from the top of the repo. Current PROJECT_BASE_DIR= ${PROJECT_BASE_DIR}"
    fi
    
    TOOLS_DIR="${PROJECT_BASE_DIR}/${TOOLS_REL_PATH}"
    VIRTUALENV_BASE_DIR="${PROJECT_BASE_DIR}/env"
    if [ ! -d ${VIRTUALENV_BASE_DIR} ]; then
        mkdir ${VIRTUALENV_BASE_DIR}
    fi
    if [ ! -d ${VIRTUALENV_BASE_DIR} ]; then
        exit_on_error "Failed to create ${VIRTUALENV_BASE_DIR}"
    fi
    
    VIRTUALENV_TARGET_DIR="${VIRTUALENV_BASE_DIR}/${DEPLOY_TYPE}"
    if [ -d ${VIRTUALENV_TARGET_DIR} ]; then
        exit_on_error "ERROR: virtualenv target ${VIRTUALENV_TARGET_DIR} already exists. Remove it first:  rm -fr ${VIRTUALENV_TARGET_DIR}"
    fi
}

create_virtualenv() {
    PYTHON_EXE=`which python`
    if [ -z "${PYTHON_EXE}" ]; then
        exit_on_error "ERROR: Failed to find a python 2.7 executable on the PATH."
    fi    
    
    # TODO Prefer using virtualenv --no-site-packages 
    virtualenv --no-site-packages ${VIRTUALENV_TARGET_DIR}
    if [ $? -ne 0 ]; then
        exit_on_error "Failed to install virtualenv to ${VIRTUALENV_TARGET_DIR}"
    fi
    
    echo_activate
}

launch_env_setup_python() {
    _activate_this=`ls "${VIRTUALENV_TARGET_DIR}/Scripts"/activate_this.py`
    _env_setup_py=`echo_norm_path "${TOOLS_DIR}/env_setup.py"`
    _pip=`echo_norm_path "${VIRTUALENV_TARGET_DIR}/Scripts"/pip`

    # Activate virtualenv using python since we can't source the activate.bat within cygwin.
    echo "Launching: python \"${_env_setup_py}\" \"${_activate_this}\" \"${_pip}\""
    python "${_env_setup_py}" "${_activate_this}" "${_pip}"
    if [ $? -ne 0 ]; then
        exit_on_error "Failed to pip install via ${_env_setup_py}"
    fi
}

main() {
    prepare_dirs    
    create_virtualenv
    launch_env_setup_python
    echo_activate
}

main

