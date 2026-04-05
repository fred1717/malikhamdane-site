# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.0] - 2026-04-05

### Added

- Terraform infrastructure across 5 modules:
    - `s3`: private bucket with versioning
    - `acm`: SSL certificate with DNS validation
    - `cloudfront`: CDN distribution with Origin Access Control
    - `route53`: DNS alias record
    - `cicd`: OIDC provider and IAM role for GitHub Actions
- Root Terraform configuration with S3 bucket policy
  (placed at root level to avoid circular dependency between `s3` and `cloudfront` modules)
- GitHub Actions deployment workflow (`deploy.yml`)
  with OIDC federation (no stored IAM access keys)
- CloudFront Function (`language_redirect.js`)
  for browser language detection and 302 redirect
- Site content in 6 languages:
    - French
    - English
    - German
    - Spanish
    - Portuguese
    - Russian
- Root `index.html` as fallback
- Custom 404 error page
- External stylesheet (`css/style.css`) with brand colours
- Links to 4 LinkedIn articles on each language page
- `README.md` with architecture overview and cost estimate
- `docs/repository_structure.md`
- `.gitignore` excluding Terraform runtime artefacts, `.env`, and `journal.md`
- `.env.example` with placeholder values
- Cost Explorer tagging via Terraform `default_tags`

### Fixed

- CloudFront Function amended to append `index.html` to subdirectory paths
  (initial version only handled the root path)
- CloudFront Function amended to return non-directory requests unchanged
  (prevented incorrect redirect of static assets such as `style.css`)
