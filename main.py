#!/usr/bin/env python
from constructs import Construct

from cdktf import (
    App,
    TerraformStack,
    TerraformOutput,
    RemoteBackend,
    NamedRemoteWorkspace,
)
from imports.aws import (
    AwsProvider,
    S3Bucket,
    S3BucketWebsite,
    S3BucketObject,
    CloudfrontDistribution,
    CloudfrontDistributionOrigin,
    CloudfrontDistributionDefaultCacheBehavior,
    CloudfrontDistributionRestrictions,
    CloudfrontDistributionRestrictionsGeoRestriction,
    CloudfrontDistributionViewerCertificate,
    CloudfrontDistributionDefaultCacheBehaviorForwardedValues,
    CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies,
    Route53Record,
    Route53RecordAlias
)

import mimetypes

class StaticWebsiteStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str, hosted_zone_id: str):
        super().__init__(scope, ns)

        # define resources here
        AwsProvider(self, "Aws", region="us-west-2")

        # Hardcoded vars here, used later to set up the Route53 record and Cloudfront distribution, could pass these in as args to make this construct more reusable
        var_acl_wildcard_certificate_arn = "WILDCARD_ACM_CERT_ARN_HERE"
        self.hosted_zone_id = hosted_zone_id

        # Define the S3 bucket to be used for static website hosting
        website_bucket = S3Bucket(
            self,
            "s3_bucket_static_website",
            bucket="test-cdktf-bucket",
            acl="public-read",
            website=[
                S3BucketWebsite(
                    error_document="error.html", index_document="index.html"
                )
            ]
        )

        # Define local path to a index.html file to upload - for uploading multiple files we could do a loop through the directory
        s3_file_source = "/Users/local/path/to/website/files/index.html"
        mimetype, _ = mimetypes.guess_type(s3_file_source) # Guess mimetype of the file for S3 upload

        # Upload the index.html file to the S3 bucket with public-read ACL for use in a static website
        bucket_object = S3BucketObject(
            self,
            "s3_bucket_object_indexhtml",
            depends_on=[website_bucket],
            bucket=website_bucket.bucket,
            key="index.html",
            acl="public-read",
            source=s3_file_source,
            content_type=mimetype
        ) # Ref https://dev.to/thakkaryash94/host-static-website-using-aws-cdk-for-terraform-part-1-57ki
        
        # Cloudfront distribution to sit in front of the S3 bucket holding the website contents
        cloudfront_distribution = CloudfrontDistribution(
            self,
            "cloudfront_distribution",
            enabled=True,
            default_root_object="index.html",
            origin=[CloudfrontDistributionOrigin(
                domain_name=website_bucket.bucket_regional_domain_name,
                origin_id="cdks3originid"
            )],
            aliases=["SUBDOMAIN.DOMAIN_NAME.com"],  # Note - we need to configure the ACM wildcard certificate in order to use this alias
            default_cache_behavior=[CloudfrontDistributionDefaultCacheBehavior(
                allowed_methods=["HEAD","GET"],
                cached_methods=["HEAD","GET"],
                target_origin_id="cdks3originid",
                viewer_protocol_policy="redirect-to-https",
                forwarded_values=[CloudfrontDistributionDefaultCacheBehaviorForwardedValues(
                    cookies=[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(
                        forward="none"
                    )],
                    query_string=False
                )]
            )],
            restrictions=[CloudfrontDistributionRestrictions(
                geo_restriction=[CloudfrontDistributionRestrictionsGeoRestriction(
                    restriction_type="whitelist",
                    locations=["US"]
                )]
            )],
            # Define the ACM certificate associated with the previously configured alias
            viewer_certificate=[CloudfrontDistributionViewerCertificate(
                acm_certificate_arn=var_acl_wildcard_certificate_arn,
                ssl_support_method="sni-only",
                minimum_protocol_version="TLSv1"
            )]
        )

        # Define an A record in the route53 hosted zone so that DNS requests to the subdomain will reach the cloudfront distribution
        route_53_a_record = Route53Record(
            self,
            "route53_a_record",
            name="SUBDOMAIN.DOMAIN_NAME.com",
            type="A",
            zone_id=self.hosted_zone_id,
            alias=[Route53RecordAlias(
                name=cloudfront_distribution.domain_name,
                zone_id=cloudfront_distribution.hosted_zone_id,
                evaluate_target_health=False
            )]
        )

        # TerraformOutput(self, "newInstanceIP", value=newInstance.public_ip)
        TerraformOutput(self, "out_s3_bucket_website_url", value=website_bucket.bucket_regional_domain_name)
        TerraformOutput(self, "out_cloudfront_distribution_domain_name", value=cloudfront_distribution.domain_name)


app = App()
stack = StaticWebsiteStack(app, "cdktf_static_website", hosted_zone_id="ROUTE53_HOSTED_ZONE_ID_HERE")

RemoteBackend(
    stack,
    hostname="app.terraform.io",
    organization="TERRAFORM_CLOUD_ORGANIZATION_NAME_HERE",
    workspaces=NamedRemoteWorkspace("TERRAFORM_CLOUD_WORKSPACE_NAME_HERE"),
)

app.synth()
