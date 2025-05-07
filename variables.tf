variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "us-east-1"
}

variable "agent_name" {
  description = "Name of the Bedrock agent"
  type        = string
  default     = "my-bedrock-agent1"
}

variable "component_id" {
  description = "Component ID for the resources"
  type        = string
  default     = "skylense"
}