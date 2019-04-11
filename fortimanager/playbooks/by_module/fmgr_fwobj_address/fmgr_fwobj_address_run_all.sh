#!/bin/bash
ansible-playbook fmgr_fwobj_ipv6_add_iprange.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_fqdn.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_del_all.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_broadcast_subnet.yml -vvvv
ansible-playbook fmgr_fwobj_ipv6_add_ip.yml -vvvv
ansible-playbook fmgr_fwobj_ipv6_add_z_group.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_geo.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_ipmask.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_z_group.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_ipsubnet.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_multicast_range.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_iprange.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_wildcard_fqdn.yml -vvvv
ansible-playbook fmgr_fwobj_ipv4_add_wildcard.yml -vvvv
