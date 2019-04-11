#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: fmgr_provisioning
version_added: "2.8"
notes:
    - Full Documentation at U(https://ftnt-ansible-docs.readthedocs.io/en/latest/).
author: Andrew Welsh (@Ghilli3)
short_description: Provision devices via FortiMananger
description:
  - Add model devices on the FortiManager using jsonrpc API and have them pre-configured,
    so when central management is configured, the configuration is pushed down to the
    registering devices

options:
  adom:
    description:
      - The administrative domain (admon) the configuration belongs to.
    default: "root"

  vdom:
    description:
      - The virtual domain (vdom) the configuration belongs to.
    default: "root"

  policy_package:
    description:
      - The name of the policy package to be assigned to the device.
    default: "default"

  name:
    description:
      - The name of the device to be provisioned.
    required: True

  group:
    description:
      - The name of the device group the provisioned device can belong to.
    required: False

  serial:
    description:
      - The serial number of the device that will be provisioned.
    required: True

  platform:
    description:
      - The platform of the device, such as model number or VM.
    default: "FortiGate-VM64"

  description:
    description:
      - Description of the device to be provisioned.
    required: False

  os_version:
    description:
      - The Fortinet OS version to be used for the device, such as 5.0 or 6.0.
    required: True

  minor_release:
    description:
      - The minor release number such as 6.X.1, as X being the minor release.
    required: False

  patch_release:
    description:
      - The patch release number such as 6.0.X, as X being the patch release.
    required: False

  os_type:
    description:
      - The Fortinet OS type to be pushed to the device, such as 'FOS' for FortiOS.
    default: "fos"
'''

EXAMPLES = '''
- name: Create FGT1 Model Device
  fmgr_provisioning:
    adom: "root"
    vdom: "root"
    policy_package: "default"
    name: "FGT1"
    group: "Ansible"
    serial: "FGVM000000117994"
    platform: "FortiGate-VM64"
    description: "Provisioned by Ansible"
    os_version: '6.0'
    minor_release: 0
    patch_release: 0
    os_type: 'fos'


- name: Create FGT2 Model Device
  fmgr_provisioning:
    adom: "root"
    vdom: "root"
    policy_package: "test_pp"
    name: "FGT2"
    group: "Ansible"
    serial: "FGVM000000117992"
    platform: "FortiGate-VM64"
    description: "Provisioned by Ansible"
    os_version: '5.0'
    minor_release: 6
    patch_release: 0
    os_type: 'fos'

'''

RETURN = """
api_result:
  description: full API response, includes status code and message
  returned: always
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.network.fortimanager.fortimanager import FortiManagerHandler
from ansible.module_utils.network.fortimanager.common import FMGBaseException
from ansible.module_utils.network.fortimanager.common import FMGRCommon
from ansible.module_utils.network.fortimanager.common import DEFAULT_RESULT_OBJ
from ansible.module_utils.network.fortimanager.common import FAIL_SOCKET_MSG
from ansible.module_utils.network.fortimanager.common import FMGRMethods


def dev_group_exists(fmgr, paramgram):
    datagram = {
        'adom': paramgram["adom"],
        'name': paramgram["dev_grp_name"],
    }

    url = '/dvmdb/adom/{adom}/group/{dev_grp_name}'.format(adom=paramgram["adom"],
                                                           dev_grp_name=paramgram["dev_grp_name"])
    response = fmgr.process_request(url, datagram, FMGRMethods.GET)
    return response


def prov_template_exists(fmgr, paramgram):
    datagram = {
        'name': paramgram["prov_template"],
        'adom': paramgram["adom"],
    }

    url = '/pm/devprof/adom/{adom}/devprof/{name}'.format(adom=paramgram["adom"], name=paramgram["prov_template"])
    response = fmgr.process_request(url, datagram, FMGRMethods.GET)
    return response


def create_model_device(fmgr, paramgram):
    datagram = {
        'adom': paramgram["adom"],
        'flags': ['create_task', 'nonblocking'],
        'groups': [{'name': paramgram["group"], 'vdom': paramgram['vdom']}],
        'device': {
            'mr': paramgram["minor_release"],
            'name': paramgram["name"],
            'sn': paramgram["serial"],
            'mgmt_mode': 'fmg',
            'device action': 'add_model',
            'platform_str': paramgram["platform"],
            'os_ver': paramgram["os_version"],
            'os_type': paramgram["os_type"],
            'patch': paramgram["patch_release"],
            'desc': 'Provisioned by Ansible',
        }
    }

    url = '/dvm/cmd/add/device'
    response = fmgr.process_request(url, datagram, FMGRMethods.EXEC)
    return response


def update_flags(fmgr, paramgram):
    datagram = {
        'flags': ['is_model', 'linked_to_model']
    }

    url = 'dvmdb/device/{name}'.format(name=paramgram["name"])
    response = fmgr.process_request(url, datagram, FMGRMethods.UPDATE)
    return response


def assign_provision_template(fmgr, paramgram):
    datagram = {
        'name': paramgram["template"],
        'type': 'devprof',
        'description': 'Provisioned by Ansible',
        'scope member': [{'name': paramgram["target"]}]
    }

    url = "/pm/devprof/adom/{adom}".format(adom=paramgram["adom"])
    response = fmgr.process_request(url, datagram, FMGRMethods.UPDATE)
    return response
#
#
# def set_devprof_scope(self, provisioning_template, adom, provision_targets):
#     """
#     :param fmgr: The fmgr object instance from fortimanager.py
#     :type fmgr: class object
#     :param paramgram: The formatted dictionary of options to process
#     :type paramgram: dict
#     :return: The response from the FortiManager
#     :rtype: dict
#     """
#     fields = dict()
#     targets = []
#     fields["name"] = provisioning_template
#     fields["type"] = "devprof"
#     fields["description"] = "CreatedByAnsible"
#
#     for target in provision_targets.strip().split(","):
#         # split the host on the space to get the mask out
#         new_target = {"name": target}
#         targets.append(new_target)
#
#     fields["scope member"] = targets
#     url = "/pm/devprof/adom/{adom}".format(adom=paramgram["adom"])
#     body = {"method": "set", "params": [{"url": "/pm/devprof/adom/{adom}".format(adom=paramgram["adom"]),
#                                          "data": fields, "session": self.session}]}
#     response = fmgr.process_request(url, body, FMGRMethods.SET)
#     return response


def assign_dev_grp(fmgr, paramgram):
    datagram = {
        'name': paramgram["device_name"],
        'vdom': paramgram["vdom"],
    }

    url = "/dvmdb/adom/{adom}/group/{grp_name}/object member".format(adom=paramgram["adom"],
                                                                     grp_name=paramgram["grp_name"])
    response = fmgr.process_request(url, datagram, FMGRMethods.SET)
    return response


def update_install_target(fmgr, paramgram):
    datagram = {
        'scope member': [{'name': paramgram["device"], 'vdom': paramgram["vdom"]}],
        'type': 'pkg'
    }

    url = '/pm/pkg/adom/{adom}/{pkg_name}'.format(adom=paramgram["adom"], pkg_name=paramgram["policy_package"])
    response = fmgr.process_request(url, datagram, FMGRMethods.UPDATE)
    return response


def install_pp(fmgr, paramgram):
    datagram = {
        'adom': paramgram["adom"],
        'flags': 'nonblocking',
        'pkg': paramgram["policy_package"],
        'scope': [{'name': paramgram["device"], 'vdom': paramgram["vdom"]}],
    }

    url = 'securityconsole/install/package'
    response = fmgr.process_request(url, datagram, FMGRMethods.EXEC)
    return response


def main():

    argument_spec = dict(
        adom=dict(required=False, type="str", default="root"),
        vdom=dict(required=False, type="str", default="root"),
        policy_package=dict(required=False, type="str", default="default"),
        name=dict(required=True, type="str"),
        group=dict(required=False, type="str"),
        serial=dict(required=True, type="str"),
        platform=dict(required=False, type="str", default="FortiGate-VM64"),
        description=dict(required=False, type="str"),
        os_version=dict(required=True, type="str"),
        minor_release=dict(required=False, type="str"),
        patch_release=dict(required=False, type="str"),
        os_type=dict(required=False, type="str", default="fos"),

    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, )

    paramgram = {
        "adom": module.params["adom"],
        "vdom": module.params["vdom"],
        "policy_package": module.params["policy_package"],
        "name": module.params["name"],
        "group": module.params["group"],
        "serial": module.params["serial"],
        "platform": module.params["platform"],
        "description": module.params["description"],
        "os_version": module.params["os_version"],
        "minor_release": module.params["minor_release"],
        "patch_release": module.params["patch_release"],
        "os_type": module.params["os_type"],
    }

    module.paramgram = paramgram
    fmgr = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        fmgr = FortiManagerHandler(connection, module)
        fmgr.tools = FMGRCommon()
    else:
        module.fail_json(**FAIL_SOCKET_MSG)

    results = DEFAULT_RESULT_OBJ

    try:
        results = create_model_device(fmgr, paramgram)
        if results[0] != 0:
            module.fail_json(msg="Create model failed", **results)

        results = update_flags(fmgr, paramgram)
        if results[0] != 0:
            module.fail_json(msg="Update device flags failed", **results)

        results = update_install_target(fmgr, paramgram)
        if results[0] != 0:
            module.fail_json(msg="Adding device target to package failed", **results)

        results = install_pp(fmgr, paramgram)
        if results[0] != 0:
            module.fail_json(msg="Installing policy package failed", **results)

    except Exception as err:
        raise FMGBaseException(err)

    return module.exit_json(**results[1])


if __name__ == "__main__":
    main()
