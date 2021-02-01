set -xe
rm -rf /root/.ansible/collections/ansible_collections/onestopsoft
rm -f onestopsoft-idempiere-1.0.0.tar.gz
ansible-galaxy collection build
ansible-galaxy collection install onestopsoft-idempiere-1.0.0.tar.gz
