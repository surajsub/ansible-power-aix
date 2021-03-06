#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright:: 2020- IBM, Inc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
######################################################################

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'IBM, Inc'
}

DOCUMENTATION = r'''
---
author:
- AIX Development Team
module: mktcpip
short_description: Sets the required values for starting TCP/IP on a host
description:
- This module sets the required minimal values required for using TCP/IP on a host machine.
- These values are written to the configuration database.
version_added: '2.9'
requirements: [ AIX ]
options:
  hostname:
    description:
    - Sets the name of the host.
    type: str
    required: true
  address:
    description:
    - Sets the Internet address of the host.
    type: str
    required: true
  interface:
    description:
    - Specifies a particular network interface.
    type: str
    required: true
  netmask:
    description:
    - Specifies the mask the gateway should use in determining the appropriate subnetwork for routing.
    type: str
  gateway:
    description:
    - Adds the default gateway address to the routing table.
    type: str
  nameserver:
    description:
    - Specifies the Internet address of the name server the host uses for name resolution.
    type: str
  domain:
    description:
    - Specifies the domain name of the name server the host should use for name resolution.
    type: str
  start_daemons:
    description:
    - Starts the TCP/IP daemons.
    type: bool
    default: no
'''

EXAMPLES = r'''
- name: Set the required values for starting TCP/IP
  mktcpip:
    hostname: fred.austin.century.com
    address: 192.9.200.4
    interface: en0
    nameserver: 192.9.200.1
    domain: austin.century.com
    start_daemons: yes
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=dict(
            hostname=dict(required=True, type='str'),
            address=dict(required=True, type='str'),
            interface=dict(required=True, type='str'),
            netmask=dict(type='str'),
            gateway=dict(type='str'),
            nameserver=dict(type='str'),
            domain=dict(type='str'),
            start_daemons=dict(type='bool', default=False),
        ),
        required_together=[
            ["nameserver", "domain"],
        ]
    )

    result = dict(
        changed=False,
        msg='',
    )

    hostname = module.params['hostname']
    address = module.params['address']
    interface = module.params['interface']

    cmd = ['mktcpip', '-h', hostname, '-a', address, '-i', interface]
    netmask = module.params['netmask']
    if netmask:
        cmd += ['-m', netmask]
    gateway = module.params['gateway']
    if gateway:
        cmd += ['-g', gateway]
    nameserver = module.params['nameserver']
    if nameserver:
        cmd += ['-n', nameserver]
        domain = module.params['domain']
        if domain:
            cmd += ['-d', domain]
    if module.params['start_daemons']:
        cmd += ['-s']

    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        result['msg'] = stderr
        module.fail_json(**result)

    result['changed'] = True
    result['msg'] = stdout
    module.exit_json(**result)


if __name__ == '__main__':
    main()
