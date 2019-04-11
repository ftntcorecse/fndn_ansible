#!/bin/bash
ansible-playbook fmgr_fwobj_vip_add_pnat.yml -vvvv
ansible-playbook fmgr_fwobj_vip_add_dnst.yml -vvvv
ansible-playbook fmgr_fwobj_vip_add_fqdn.yml -vvvv
ansible-playbook fmgr_fwobj_vip_add_snat.yml -vvvv
ansible-playbook fmgr_fwobj_vip_TEMPLATE.yml -vvvv
ansible-playbook fmgr_fwobj_vip_del_all.yml -vvvv
