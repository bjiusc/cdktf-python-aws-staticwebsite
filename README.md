# cdktf-static-s3-website
This repo contains sample code in Python using CDK for Terraform (cdktf) for deploying a static website utilizing a CloudFront distribution, ACM certificate for SSL, Route53 hosted zone and records for DNS resolution for a subdomain. The domain name is pre-registered in AWS using Route53 and already has a hosted zone configured for DNS for the root domain. This repo was created as a learning journey due to the lack of public examples of cdktf in Python, and lack of public examples of linking together various resources in general.

The main manner in which this example code was developed was by referencing the __init__.py source in the imports/aws directory for class names and argument structure when `cdktf get` is ran when the `hashicorp/aws@~> 3.61` dependency is noted in the `terraformProviders` configuration item within `cdktf.json`

## Useful Resources and Links:

1: Getting started with cdktf in Python https://learn.hashicorp.com/tutorials/terraform/cdktf-build-python?in=terraform/cdktf

2: Introduction to cdktf including a live demo in Typescript - great introduction to where cdk fits a gap in IaC, how it was developed, and what it's capabilities are https://www.youtube.com/watch?v=ny2vdjsSiQM

3: Live code example of cdktf using Python https://www.youtube.com/watch?v=Ee2qh-pEC5k&t=1415s 

3: Another live code example of cdktf using Typescript https://www.youtube.com/watch?v=Cf3yJv3klsg

3: Setting up a S3 static website using cdktf (Typescript) https://dev.to/thakkaryash94/host-static-website-using-aws-cdk-for-terraform-part-1-57ki

4: A repository containing some cdktf examples (Typescript) https://github.com/skorfmann/awesome-terraform-cdk

## Usage Guide:

In general, ensure cdktf is installed with dependencies by following the guide at https://learn.hashicorp.com/tutorials/terraform/cdktf-build-python?in=terraform/cdktf. A brief summary of the steps noted in the guide is also provided below once cdktf and it's dependencies are installed.

1: run a `cdktf init` in the directory you want your project to be in. Select `python` from the templates, and use the `--local` flag if you don't want to use Terraform Cloud (I used Terraform Cloud in my example and created a test organization and workspace)

2: Add the `hashicorp/aws@~> 3.61` dependency within the `terraformProviders` configuration item within `cdktf.json` when the project is initialized

3: run `cdktf get` to install the AWS provider dependency

4: ensure you have local AWS credentials setup (alongside the AWS CLI v2 package) by running `aws configure`

5: Copy and paste the code contained in `main.py` into your `main.py` for the new cdktf Python project. Adjust the `RemoteBackend` to match the parameters of your project if you are using Terraform Cloud, otherwise remove that code block if using cdktf locally.

6: Test that the code is valid by running `cdktf synth` - if successful, deploy the code using `cdktf deploy`
