#!/bin/bash
ansible-playbook fmgr_devices_ansibleAdom.yml -vvvv
ansible-playbook fmgr_devices_plugin_edition_add.yml -vvvv
ansible-playbook fmgr_devices_ansibleAdom_all.yml -vvvv
ansible-playbook fmgr_devices_delete_ansibleAdom.yml -vvvv
ansible-playbook fmgr_devices_plugin_edition_del.yml -vvvv
ansible-playbook fmgr_devices.yml -vvvv
ansible-playbook fmgr_devices_ipv6_add.yml -vvvv
ansible-playbook fmgr_devices_ansibleAdom2.yml -vvvv
