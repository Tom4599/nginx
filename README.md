```
[masters]
masteropenshift.generac.phosphore.si

[etcd]
masteropenshift.generac.phosphore.si

[nodes]
masteropenshift.generac.phosphore.si openshift_node_labels="{'region': 'infra', 'zone': 'default'}" openshift_schedulable=true
node01openshift.generac.phosphore.si openshift_node_labels="{'region': 'primary', 'zone': 'default'}" openshift_schedulable=true
node02openshift.generac.phosphore.si openshift_node_labels="{'region': 'primary', 'zone': 'default'}" openshift_schedulable=true

[glusterfs]
masteropenshift.generac.phosphore.si glusterfs_devices='["/dev/sdb"]'
node01openshift.generac.phosphore.si glusterfs_devices='["/dev/sdb"]'
node02openshift.generac.phosphore.si glusterfs_devices='["/dev/sdb"]'

[OSEv3:children]
masters
nodes
etcd
glusterfs

[OSEv3:vars]
openshift_storage_glusterfs_wipe=true
openshift_storage_glusterfs_storageclass=true
openshift_storage_glusterfs_storageclass_default=true

ansible_ssh_user=root

openshift_deployment_type=origin

openshift_release=v3.9

debug_level=3

# allow htpasswd
openshift_master_identity_providers=[{'name': 'htpasswd', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider', 'filename': '/root/users.htpasswd'}]
openshift_master_htpasswd_file=/root/users.htpasswd

# default project node selector
osm_default_node_selector='region=primary'

# Default value: 'region=infra'
openshift_hosted_router_selector='region=infra'

template_service_broker_selector={"region": "infra"}

openshift_disable_check=docker_image_availability
```
