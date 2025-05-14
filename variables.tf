variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
}

variable "agent_name" {
  description = "Name of the Bedrock agent"
  type        = string
}

variable "component_id" {
  description = "Component ID for the resources"
  type        = string
}

# Add new variables for environment variables
variable "environment_var_1" {
  description = "First environment variable"
  type        = string
}

variable "environment_var_2" {
  description = "Second environment variable"
  type        = string
}