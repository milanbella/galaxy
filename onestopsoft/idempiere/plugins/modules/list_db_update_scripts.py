from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

#ansible_collections.onestopsoft.idempiere.plugins.module_utils.qradar
from ansible_collections.onestopsoft.idempiere.plugins.module_utils.idempiere import Idempiere

DOCUMENTATION = r'''
---
module: idempiere.modules.list_db_update_scripts

short_description: List db update scripts to be exceuted.
description: List db update scripts to be exceuted when upgrading idempiere to next verstion.

options:
    idempiere_path:
        description: Idempiere installation path. Defaults to '/home/idempiere/idempiere-server'.
        required: false
        type: str
    db_adempiere_user_password:
        description: 'adempiere' db user password. Defaults to 'adempiere'.
        required: false
        type: str
    db_host:
        description: Idempiere db host. Defaults to 'localhost'.
        required: false
        type: str
    db_port:
        description: Idempiere db port. Defaults to 5432.
        required: false
        type: int

author:
    - milanbella  (@milanbella)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  idempiere.list_db_update_scripts:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
sql_scripts_to_be_executed:
    description: List sql scripts to be executed in that order for upgrade.
    type: dict
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule # type: ignore


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        idempiere_path=dict(type='str', required=False, default='/home/idempiere/idempiere-server'),
        db_adempiere_user_password=dict(type='str', required=False, default='adempiere'),
        db_host=dict(type='str', required=False, default='localhost'),
        db_port=dict(type='int', required=False, default=5432)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    idempiere = Idempiere(module.params['idempiere_path'], module.params['db_adempiere_user_password'], module.params['db_host'], module.params['db_port'])
    sqlsList = idempiere.getNotExecutedSqlsDict()
    result['sql_scripts_to_be_executed'] = sqlsList 

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = False

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
