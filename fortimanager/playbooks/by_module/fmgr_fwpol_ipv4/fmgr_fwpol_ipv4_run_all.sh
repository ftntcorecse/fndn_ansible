#!/bin/bash
ansible-playbook fmgr_fwpol_ipv4_add_basic.yml -vvvv
ansible-playbook fmgr_fwpol_ipv4_delete_basic.yml -vvvv
