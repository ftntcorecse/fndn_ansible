#!/bin/bash
ansible-playbook fmgr_secprof_av_add.yml -vvvv
ansible-playbook fmgr_secprof_av_del.yml -vvvv
ansible-playbook av.yml -vvvv
