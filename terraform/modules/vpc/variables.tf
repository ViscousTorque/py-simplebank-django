variable "project_name" {
  description = "Name for this project"
  type        = string
}

variable "azs" {
  description = "Slice of az strings"
  type        = list(string)
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
}