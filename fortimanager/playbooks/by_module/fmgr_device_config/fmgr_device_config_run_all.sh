#!/bin/bash
ansible-playbook fmgr_device_exec_config.yml -vvvv
ansible-playbook fgt01_config.yml -vvvv
ansible-playbook fgt03_config.yml -vvvv
ansible-playbook fmgr_device_config.yml -vvvv
ansible-playbook fgt02_config.yml -vvvv
