# malikhamdane.com

Personal website hosted on AWS.
The site is static and served via the following services:
- S3 for storage
- CloudFront for CDN
- ACM for SSL
- Route 53 for DNS

The infrastructure is managed within a single provider.
Email hosting is external, with MX records managed in Route 53.
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

- A build script (`scripts/build.py`) processes the HTML files before deployment.
    The header and footer are maintained as shared templates in `site/includes/`.
    Each HTML source file contains `{{HEADER}}` and `{{FOOTER}}` placeholders.
    The build script replaces them with the processed templates.
    The active language link in the header is set automatically based on the file path.
    The mentions légales link in the footer is set to the correct language and label.

- Each language directory contains a `mentions-legales/index.html` page.
    This is a legal requirement under the LCEN (Loi pour la Confiance dans l'Économie Numérique).

- Email is hosted on Zoho Mail Lite.
    Route 53 manages the MX records pointing to Zoho Mail servers.
    SPF (Sender Policy Framework) and DKIM (DomainKeys Identified Mail) records are also configured in Route 53.
    They serve for email authentication.
    Both are standard best practice for any custom domain email setup.
    Zoho provides the exact values to add in Route 53 during the configuration process.
    - SPF: A TXT record in Route 53 that declares which mail servers are authorised to send email on behalf of malikhamdane.com.
            Without it, anyone could send an email pretending to be contact@malikhamdane.com.
            Receiving mail servers check the SPF record to verify the sender is legitimate.
    - DKIM: a TXT or CNAME record in Route 53 that publishes a public key.
            Zoho Mail signs every outgoing email with a corresponding private key.
            The receiving mail server uses the public key from the DNS record to verify the signature.
            If the signature does not match, the email is flagged as suspicious or rejected.


## Cost

The estimated annual cost is approximately $32 to $35:
- Route 53 hosted zone: $6.00
- Domain registration: $13.00
- S3 storage: approximately $0.25
- CloudFront: $0.00 (free tier)
- ACM certificate: $0.00
- Zoho Mail Lite: $14.00 (12.96 €)


## Prerequisites

- An AWS account
- Terraform installed
- AWS CLI configured with appropriate credentials
- Python 3 installed (required by the build script)


## Deployment

GitHub Actions runs on every push to `main` that modifies files in `site/`.
The pipeline executes `scripts/build.py` to process the templates, then uploads the contents of `build/` to S3.
Authentication between GitHub Actions and AWS uses OIDC federation.
No IAM access keys are stored.


## Repository structure

See `docs/repository_structure.md`.


## Changelog

See `CHANGELOG.md`.

