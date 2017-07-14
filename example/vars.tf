variable "num_docker_swarm_workers" {
  description = "the number of swarm workers to create"
  default = 3
}

variable "num_docker_swarm_managers" {
  description = "the number of swarm managers to create"
  default = 1
}

variable "ami_id" {
  description = "id of ami to use for swarm"
}

variable "worker_instance_type" {
  description = "size of worker nodes"
  default = "t2.small"
}

variable "manager_instance_type" {
  description = "size of manager nodes"
  default = "t2.small"
}

variable "worker_volume_size" {
  description = "size of worker volumes"
  default = 20
}

variable "manager_volume_size" {
  description = "size of manager volumes"
  default = 20
}

variable "worker_subnet_ids" {
  type = "list"
  description = "list of subnet ids to put worker nodes"
}

variable "manager_subnet_ids" {
  type = "list"
  description = "list of subnet ids to put manager nodes"
}

variable "worker_security_group_ids" {
  type = "list"
  description = "list of security groups to add to worker nodes"
}

variable "manager_security_group_ids" {
  type = "list"
  description = "list of security groups to add to manager nodes"
}

variable "worker_tags" {
  type = "map"
  description = "tags to add to worker nodes"
  default = {}
}

variable "manager_tags" {
  type = "map"
  description = "tags to add to manager nodes"
  default = {}
}

variable "env" {
  description = "the environment name"
  default = "test"
}

variable "provision_command" {
  description = "command to execute locally to provision nodes (hint: ansible/configuration manager)"
}

