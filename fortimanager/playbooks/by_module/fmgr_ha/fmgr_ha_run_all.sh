#!/bin/bash
ansible-playbook fmgr_ha_run_all.sh -vvvv
ansible-playbook fmgr_ha_standalone.yml -vvvv
ansible-playbook fmgr_ha_enable_peer2.yml -vvvv
ansible-playbook fmgr_ha_slave.yml -vvvv
ansible-playbook fmgr_ha_enable_peer.yml -vvvv
ansible-playbook fmgr_ha_enable_peer_slave.yml -vvvv
ansible-playbook fmgr_ha_master.yml -vvvv
ansible-playbook fmgr_ha_disable_peer2.yml -vvvv
ansible-playbook fmgr_ha_disable_peer.yml -vvvv
