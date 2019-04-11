#!/bin/bash
ansible-playbook fmgr_fwobj_ippool_del.yml -vvvv
ansible-playbook fmgr_fwobj_ippool_add.yml -vvvv
