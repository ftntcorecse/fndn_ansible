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
module: fmgr_sys_proxy
version_added: "2.8"
notes:
    - Full Documentation at U(https://ftnt-ansible-docs.readthedocs.io/en/latest/).
author: Andrew Welsh
short_description: Make FortiGate API calls via the FortiMananger
description:
  - The FMG proxies FOS API calls via the FMG.  Review FortiGate API documentation to ensure you are passing correct
    parameters for both the FortiManager and FortiGate

options:
  adom:
    description:
      - The administrative domain (admon) the configuration belongs to
    required: true
  action:
    description:
      - Specify HTTP action for the request. Either 'get' or 'post'
    required: True
  payload:
    description:
      - JSON payload of the request. The payload will be URL-encoded and becomes the "json" field in the query string for both GET and POST request.
    required: False
  resource:
    description:
      - URL on the remote device to be accessed, string
    required: True
  target:
    description:
      - FOS datasource, either device or group object
    required: True

'''

EXAMPLES = '''
- name: Proxy FOS requests via FMG
  hosts: FortiManager
  connection: local
  gather_facts: False

  tasks:

    - name: Get upgrade path for FGT1
      fmgr_provision:
        adom: "root"
        action: "get"
        resource: "/api/v2/monitor/system/firmware/upgrade-paths?vdom=root"
        target: ["/adom/root/device/FGT1"]
    - name: Upgrade firmware of FGT1
      fmgr_provision:
        adom: "root"
        action: "post"
        payload: {source: upload, file_content: b64_encoded_string, file_name: file_name}
        resource: "/api/v2/monitor/system/firmware/upgrade?vdom=vdom"
        target: ["/adom/root/device/FGT1"]

'''

RETURN = """
api_result:
  description: full API response, includes status code and message
  returned: always
  type: string
"""


from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.connection import Connection
from ansible.module_utils.network.fortimanager.fortimanager import FortiManagerHandler
from ansible.module_utils.network.fortimanager.common import FMGBaseException
#from ansible.module_utils.network.fortimanager.common import DEFAULT_RESULT_OBJ
from ansible.module_utils.network.fortimanager.common import FAIL_SOCKET_MSG
from ansible.module_utils.network.fortimanager.common import prepare_dict
from ansible.module_utils.network.fortimanager.common import scrub_dict


def fos_request(fmgr, action, resource, target, payload, adom='root'):

    datagram = {
        "data": {
            # get or post
            "action": action,
            # dictionary of data
            "payload": payload,
            # FOS API URL including vdom params
            "resource": resource,
            # FMG device to make API calls to
            "target": target
        },

    }
    url = "/sys/proxy/json"

    status, response = fmgr.process_request(url, datagram, action)
    return status, response


def main():

    argument_spec = dict(
        adom=dict(required=False, type="str"),
        host=dict(required=True, type="str"),
        password=dict(fallback=(env_fallback, ["ANSIBLE_NET_PASSWORD"]), no_log=True),
        username=dict(fallback=(env_fallback, ["ANSIBLE_NET_USERNAME"]), no_log=True),

        action=dict(required=False, type="str"),
        resource=dict(required=False, type="str"),
        target=dict(required=False, type="str"),
        payload=dict(required=False, type="str"),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, )
    fmgr = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        fmgr = FortiManagerHandler(connection, module.check_mode)
        fmgr.tools = FMGRCommon()
    else:
        module.fail_json(**FAIL_SOCKET_MSG)

    action = module.params["action"]
    resource = module.params["resource"]
    target = module.params["target"]
    payload = module.params["payload"]
    if module.params["adom"] is None:
        module.params["adom"] = 'root'

    # BEGIN MODULE-SPECIFIC LOGIC -- THINGS NEED TO HAPPEN DEPENDING ON THE ENDPOINT AND OPERATION
    results = DEFAULT_RESULT_OBJ
    try:
        status, result = fos_request(fmgr, action, resource, target, payload, module.params["adom"])
        fmgr.govern_response(module=module, results=results,
                             ansible_facts=fmgr.construct_ansible_facts(results, module.params, payload))

    except Exception as err:
        raise FMGBaseException(err)

    return module.exit_json(changed=True, **result)


if __name__ == "__main__":
    main()
