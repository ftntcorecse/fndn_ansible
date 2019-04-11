#!/bin/bash
ansible-playbook fmgr_fwobj_ippool6_del.yml -vvvv
ansible-playbook fmgr_fwobj_ippool6_add.yml -vvvv
