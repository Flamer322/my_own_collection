#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Creates a text file

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description:
    - Creates a text file on the target host
    - The file path and content are specified through parameters

options:
    path:
        description: Absolute path to the file that should be created
        required: true
        type: str

    content:
        description: Content that should be written into the file
        required: true
        type: str

author:
    - Boris Bartenev (@flamer322)
'''

EXAMPLES = r'''
- name: Create a text file
  my_own_module:
    path: /tmp/test.txt
    content: test

- name: Change file content
  my_own_module:
    path: /tmp/test.txt
    content: new test
'''

RETURN = r'''
path:
    description: Path to the created file.
    type: str
    returned: always
    sample: /tmp/test.txt

content:
    description: Content written to the file.
    type: str
    returned: always
    sample: test
'''

import os

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        path='',
        content=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    # Check whether the target path is a directory.
    if os.path.isdir(path):
        module.fail_json(
            msg=f'{path} is a directory, not a file',
            **result
        )

    # Read existing file content.
    try:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as file:
                current_content = file.read()
        else:
            current_content = None

    except (OSError, UnicodeError) as error:
        module.fail_json(
            msg=f'Unable to read file: {error}',
            **result
        )

    # Determine whether anything needs to be changed.
    changed = current_content != content

    result['changed'] = changed

    # Provide diff information when requested.
    if module._diff:
        result['diff'] = {
            'before': current_content if current_content is not None else '',
            'after': content
        }

    # Check mode: report what would change without modifying anything.
    if module.check_mode:
        module.exit_json(**result)

    # Write the file only when its content differs.
    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

        except OSError as error:
            module.fail_json(
                msg=f'Unable to write file: {error}',
                **result
            )

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()