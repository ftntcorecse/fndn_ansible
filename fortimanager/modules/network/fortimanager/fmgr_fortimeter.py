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

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community"
}

DOCUMENTATION = '''
---
module: fmgr_fortimeter
version_added: "2.8"
notes:
    - Full Documentation at U(https://ftnt-ansible-docs.readthedocs.io/en/latest/).
author: Luke Weighall (@lweighall)
short_description: Sets FortiMeter licensing level
description:
  - Provides MSPs the ability to programmatically change FortiMeter license levels on devices.

options:
  adom:
    description:
      - The ADOM the configuration should belong to.
    required: true
    default: root
  device_unique_name:
    description:
      - The desired "friendly" name of the device you want to query.
    required: true
  fortimeter_utm_level:
    description:
      - Determines which UTM profiles should be allowed for Fortimeter. Multiple comma seperated selections allowed.
    required: true
    default: "all"
    choices: ["fw", "ips", "av", "ac", "wf", "all"]
  foslic_type:
    description:
      - Sets the FortiMeterOS license Type (0 is temporary, 2 is regular, 1 is trial, 3 is expired)
    required: false
    default: 2
'''


EXAMPLES = '''
- name: SET LICENSING MODE ON FORTIMETER DEVICE to ALL
  fmgr_fortimeter:
    object: "device"
    adom: "ansible"
    device_unique_name: "FOSVM1FGPRJ411DD"
    fortimeter_utm_level: "all"

- name: SET LICENSING MODE ON FORTIMETER DEVICE to a COMBO
  fmgr_fortimeter:
    object: "device"
    adom: "ansible"
    device_unique_name: "FOSVM1FGPRJ411DD"
    fortimeter_utm_level: "fw, ips, av"
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
from ansible.module_utils.network.fortimanager.common import FMGRMethods
from ansible.module_utils.network.fortimanager.common import DEFAULT_RESULT_OBJ
from ansible.module_utils.network.fortimanager.common import FAIL_SOCKET_MSG



def fmgr_set_fortimeter_lic(fmgr, paramgram):
    """
    :param fmgr: The fmgr object instance from fortimanager.py
    :type fmgr: class object
    :param paramgram: The formatted dictionary of options to process
    :type paramgram: dict
    :return: The response from the FortiManager
    :rtype: dict
    """
    # FIRST WE NEED TO PARSE THE DESIRED FOSLIC LEVEL ON THESE RULES
    # FW = 1
    # AV = 2
    # IPS = 4
    # AC = 8
    # WF = 16
    # PARSE THE DESIRED OPTIONS, AND THEN ADD THEM UP
    fos_levels = {
        "fw": 1,
        "av": 2,
        "ips": 4,
        "ac": 8,
        "wf": 16
    }

    foslic = 0
    fos_items = paramgram["fortimeter_utm_level"].strip().split(",")

    if "all" in paramgram["fortimeter_utm_level"].lower():
        foslic = 63
    else:
        for item in fos_items:
            if item.strip().lower() == "fw":
                foslic += fos_levels["fw"]
                continue
            if item.strip().lower() == "av":
                foslic += fos_levels["av"]
                continue
            if item.strip().lower() == "ips":
                foslic += fos_levels["ips"]
                continue
            if item.strip().lower() == "ac":
                foslic += fos_levels["ac"]
                continue
            if item.strip().lower() == "wf":
                foslic += fos_levels["wf"]
                continue

    datagram = {
        "foslic_utm": foslic,
        "foslic_type": paramgram["foslic_type"]
    }
    url = "/dvmdb/adom/{adom}/device/{device}".format(adom=paramgram["adom"], device=paramgram["device_unique_name"])
    response = fmgr.process_request(url, datagram, FMGRMethods.SET)

    return response


def main():
    argument_spec = dict(
        adom=dict(required=False, type="str", default="root"),
        device_unique_name=dict(required=True, type="str"),
        fortimeter_utm_level=dict(required=True, type="str"),
        foslic_type=dict(required=False, type="int", default=2)
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, )
    paramgram = {
        "adom": module.params["adom"],
        "device_unique_name": module.params["device_unique_name"],
        "fortimeter_utm_level": module.params["fortimeter_utm_level"],
        "foslic_type": module.params["foslic_type"]
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
        results = fmgr_set_fortimeter_lic(fmgr, paramgram)
        fmgr.govern_response(module=module, results=results,
                             ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))

    except Exception as err:
        raise FMGBaseException(err)

    return module.exit_json(**results[1])


if __name__ == "__main__":
    main()
