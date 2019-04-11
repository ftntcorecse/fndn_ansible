#!/bin/bash
ansible-playbook fmgr_faz_scripts.yml -vvvv
ansible-playbook fmgr_script_run_all.sh -vvvv
ansible-playbook fmgr_scripts.yml -vvvv
