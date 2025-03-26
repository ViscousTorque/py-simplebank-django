
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = var.project_name
  cidr = var.vpc_cidr

  azs = var.azs

  public_subnets  = [for k, v in var.azs : cidrsubnet(var.vpc_cidr, 8, k)]
  private_subnets = [for k, v in var.azs : cidrsubnet(var.vpc_cidr, 8, k + 3)]

  enable_dns_support   = true
  enable_dns_hostnames = true
  enable_nat_gateway   = true
  single_nat_gateway   = true

  map_public_ip_on_launch = true

    public_subnet_tags = {
    # TODO: use a variable here for the eks cluster name
    "kubernetes.io/cluster/simple-bank-cluster" = "shared"
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    # TODO: use a variable here for the eks cluster name
    "kubernetes.io/cluster/simple-bank-cluster" = "shared"
    "kubernetes.io/role/internal-elb" = "1"
  }

  tags = {
    Project = var.project_name
  }
}

// TODO - this resource is against best practices, only good for quick demo, fix later for best practices
resource "aws_db_subnet_group" "public" {
  name        = "public-db-subnet-group"
  description = "DB Subnet Group for Public Subnets"
  subnet_ids  = module.vpc.public_subnets

  tags = {
    Name = "Public DB Subnet Group"
  }
}


