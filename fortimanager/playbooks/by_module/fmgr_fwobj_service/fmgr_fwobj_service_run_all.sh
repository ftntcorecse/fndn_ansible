#!/bin/bash
ansible-playbook fmgr_fwobj_service_delete_group.yml -vvvv
ansible-playbook fmgr_fwobj_service_add_group.yml -vvvv
ansible-playbook fmgr_fwobj_service_delete_custom.yml -vvvv
ansible-playbook fmgr_fwobj_service_delete_category.yml -vvvv
ansible-playbook fmgr_fwobj_service_add_custom.yml -vvvv
ansible-playbook fmgr_fwobj_service_add_category.yml -vvvv
