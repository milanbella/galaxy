set -x
mkdir -p ${HOME}/module_utils/ansible_collections/onestopsoft/idempiere/plugins/
if [ ! -d ${HOME}/module_utils/ansible_collections/onestopsoft/idempiere/plugins/module_utils ]; then
	ln -s `pwd`/module_utils ${HOME}/module_utils/ansible_collections/onestopsoft/idempiere/plugins/module_utils
	touch ${HOME}/module_utils/ansible_collections/__init__.py
	touch ${HOME}/module_utils/ansible_collections/onestopsoft/__init__.py
	touch ${HOME}/module_utils/ansible_collections/onestopsoft/idempiere/__init__.py
	touch ${HOME}/module_utils/ansible_collections/onestopsoft/idempiere/plugins/__init__.py
fi
export PYTHONPATH=${HOME}/module_utils
export MYPYPATH=${HOME}/module_utils
mypy --ignore-missing-imports module_utils/ modules/
