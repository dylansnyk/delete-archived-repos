![snyk-oss-category](https://github.com/snyk-labs/oss-images/blob/main/oss-example.jpg)

# Delete Archived Repos in Snyk

Clone and install dependencies:
```
git clone https://github.com/dylansnyk/delete-archived-repos
cd delete-archived-repos
pip install requests
```

Dry run to review the archived repos in Snyk (no delete):
```
python3 main.py \
  --github-org your_github_org_name \
  --github-pat your_github_pat \
  --snyk-token your_snyk_token \
  --snyk-org your_snyk_org 
```

After reviewing the repos to be deleted in the previous step, add the `--delete` argument to delete the archived repos in Snyk:
```
python3 main.py \
  --github-org your_github_org_name \
  --github-pat your_github_pat \
  --snyk-token your_snyk_token \
  --snyk-org your_snyk_org \
  --delete
```

Help:
```
python3 main.py --help
usage: main.py [-h] [-d] [--github-org GITHUB_ORG] [--github-pat GITHUB_PAT] [--snyk-token SNYK_TOKEN] [--snyk-org SNYK_ORG]

Delete all archived GitHub repos in Snyk

options:
  -h, --help            show this help message and exit
  -d, --delete          Delete repos in Snyk (a dry run is run by default)
  --github-org GITHUB_ORG
                        GitHub org name, as seen in the GitHub repo URL
  --github-pat GITHUB_PAT
                        GitHub classic PAT with "Metadata" repository permissions (read) scope
  --snyk-token SNYK_TOKEN
                        Snyk API token or service account
  --snyk-org SNYK_ORG   Snyk Org ID, e.g. 1aaaaaaa-2bbb-3ccc-4ddd-5eeeeeeeeeee
```
