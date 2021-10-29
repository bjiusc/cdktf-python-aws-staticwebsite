# cdktf-python-aws-staticwebsite
Deploys a S3 backed static website using CDK for Terraform (cdktf) in Python. Utilizes a CloudFront distribution, ACM certificate for SSL, Route53 hosted zone and records for DNS resolution for a subdomain. The domain name is pre-registered in AWS using Route53 and already has a hosted zone configured for DNS for the root domain.
