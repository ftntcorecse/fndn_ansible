#!/bin/bash
ansible-playbook fmgr_group_delete.yml -vvvv
ansible-playbook fmgr_group_edit_remove.yml -vvvv
ansible-playbook fmgr_device_groups.yml -vvvv
ansible-playbook fmgr_group_edit_add.yml -vvvv
ansible-playbook fmgr_group_add.yml -vvvv
