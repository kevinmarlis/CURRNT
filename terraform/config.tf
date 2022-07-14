# This configuration file will contain the provider configurations and tested versions.
# Specify the Terraform provider version.
# Configure the AWS Provider
provider "aws" {
  region                   = "us-east-1"
  shared_credentials_files = ["~/.aws/credentials"]
}
