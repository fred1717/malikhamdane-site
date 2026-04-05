# malikhamdane.com

Personal website hosted on AWS.
The site is static and served via the following services:
- S3 for storage
- CloudFront for CDN
- ACM for SSL
- Route 53 for DNS

The entire stack is managed within a single provider.
Infrastructure is defined in Terraform.
Deployment is handled by GitHub Actions.


## Architecture

- The static files are stored in a private S3 bucket.

- CloudFront serves them from edge locations using an Origin Access Control.
    Origin Access Control (OAC) is the mechanism that allows CloudFront to read objects from a private S3 bucket.
    Without it, the S3 bucket would need to be public.
    With it, only CloudFront can access the bucket content.
    Direct access to the S3 URL is denied.
    This is the current recommended method.
    The older method was called Origin Access Identity (OAI), which AWS considers legacy.

- The ACM certificate is provisioned in `us-east-1` (required by CloudFront).

- Route 53 manages the DNS records, including the CNAME for certificate validation.

- The site supports 6 languages:
    - French
    - English
    - German
    - Spanish
    - Portuguese
    - Russian

- A CloudFront Function inspects the browser `Accept-Language` header and redirects to the corresponding language subdirectory.

- A custom 404 error page is served for invalid paths.


## Cost

The estimated annual cost is approximately $19 to $22:
- Route 53 hosted zone: $6.00
- Domain registration: $13.00
- S3 storage: approximately $0.25
- CloudFront: $0.00 (free tier)
- ACM certificate: $0.00


## Prerequisites

- An AWS account
- Terraform installed
- AWS CLI configured with appropriate credentials


## Deployment

GitHub Actions deploys the site content to S3 on every push to `main` that modifies files in `site/`.
Authentication between GitHub Actions and AWS uses OIDC federation.
No IAM access keys are stored.


## Repository structure

See `docs/repository_structure.md`.



