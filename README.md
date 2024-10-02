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

Delete the archived repos in Snyk:
```
python3 main.py \
  --github-org your_github_org_name \
  --github-pat your_github_pat \
  --snyk-token your_snyk_token \
  --snyk-org your_snyk_org \
  --delete
```
