**Get the repository structure as a tree**
From the parent folder of the project folder:
```bash
tree -I '.git' malikhamdane-site
```

The problem with that command is that it mixes files and directories in alphabetical order.
Better is to sort directories first, thus following the established convention:
```bash
tree -a --dirsfirst -I '.git|.idea|.terraform|*.tfstate|*.tfstate.backup|terraform.tfvars|tfplan' malikhamdane-site
```

This also excludes the contents of '.git' and '.idea' directories.
`-I`: ignore
`.git|.idea`: exclude any file or directory whose name matches `.git` or `.idea`.
    The pipe `|` separates multiple patterns.

malikhamdane-site
├── .github
│   └── workflows
│       └── deploy.yml
├── docs
│   └── repository_structure.md
├── site
│   ├── assets
│   ├── css
│   │   └── style.css
│   ├── de
│   │   └── index.html
│   ├── en
│   │   └── index.html
│   ├── es
│   │   └── index.html
│   ├── fr
│   │   └── index.html
│   ├── pt
│   │   └── index.html
│   ├── ru
│   │   └── index.html
│   ├── 404.html
│   └── index.html
├── terraform
│   ├── modules
│   │   ├── acm
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── cicd
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── cloudfront
│   │   │   ├── functions
│   │   │   │   └── language_redirect.js
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── route53
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   └── s3
│   │       ├── main.tf
│   │       ├── outputs.tf
│   │       └── variables.tf
│   ├── .terraform.lock.hcl
│   ├── main.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── variables.tf
├── .env
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── README.md
└── journal.md

21 directories, 38 files
