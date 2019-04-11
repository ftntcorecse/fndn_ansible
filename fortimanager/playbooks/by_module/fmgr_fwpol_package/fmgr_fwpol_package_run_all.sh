#!/bin/bash
ansible-playbook fmgr_fwpol_plugin_install.yml -vvvv
ansible-playbook fmgr_fwpol_package_add.yml -vvvv
ansible-playbook fmgr_fwpol_package_delete.yml -vvvv
ansible-playbook fmgr_fwpol_package_add_with_rules_install.yml -vvvv
ansible-playbook fmgr_fwpol_plugin_del.yml -vvvv
ansible-playbook fmgr_fwpol_package_install2vdom.yml -vvvv
ansible-playbook fmgr_fwpol_package_install.yml -vvvv
ansible-playbook fmgr_fwpol_package_assign2vdom.yml -vvvv
ansible-playbook fmgr_fwpol_plugin_add.yml -vvvv
