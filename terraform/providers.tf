provider "aws" {
  region = "us-west-2"
  profile = "your-aws-profile"
}

terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "path/to/terraform.tfstate"
    region = "us-west-2"
  }
}
