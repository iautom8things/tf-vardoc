# Example README.md.js
You should setup your module's readme like you normally would.

## Variables
Variables that do not provide a default value are **required**.

###### "ami_id"
- **description** : _"id of ami to use for swarm"_
###### "env"
- **description** : _"the environment name"_
- **default** : _"test"_
###### "manager_instance_type"
- **description** : _"size of manager nodes"_
- **default** : _"t2.small"_
###### "manager_security_group_ids"
- **type** : _list_
- **description** : _"list of security groups to add to manager nodes"_
###### "manager_subnet_ids"
- **type** : _list_
- **description** : _"list of subnet ids to put manager nodes"_
###### "manager_tags"
- **type** : _map_
- **description** : _"tags to add to manager nodes"_
- **default** : _{}_
###### "manager_volume_size"
- **description** : _"size of manager volumes"_
- **default** : _20_
###### "num_docker_swarm_managers"
- **description** : _"the number of swarm managers to create"_
- **default** : _1_
###### "num_docker_swarm_workers"
- **description** : _"the number of swarm workers to create"_
- **default** : _3_
###### "provision_command"
- **description** : _"command to execute locally to provision nodes (hint: ansible/configuration manager)"_
###### "worker_instance_type"
- **description** : _"size of worker nodes"_
- **default** : _"t2.small"_
###### "worker_security_group_ids"
- **type** : _list_
- **description** : _"list of security groups to add to worker nodes"_
###### "worker_subnet_ids"
- **type** : _list_
- **description** : _"list of subnet ids to put worker nodes"_
###### "worker_tags"
- **type** : _map_
- **description** : _"tags to add to worker nodes"_
- **default** : _{}_
###### "worker_volume_size"
- **description** : _"size of worker volumes"_
- **default** : _20_
