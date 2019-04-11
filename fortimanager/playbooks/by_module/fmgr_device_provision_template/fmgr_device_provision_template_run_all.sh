#!/bin/bash
ansible-playbook fmgr_device_provision_template_remove_scope.yml -vvvv
ansible-playbook fmgr_device_proftemplate_faz_assign.yml -vvvv
ansible-playbook fmgr_device_provision_template_delete.yml -vvvv
ansible-playbook fmgr_device_provision_template.yml -vvvv
ansible-playbook fmgr_device_provision_template_run_all.sh -vvvv
ansible-playbook fmgr_device_provision_template_absent.yml -vvvv
