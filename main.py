import requests
import argparse

# Initialize parser
parser = argparse.ArgumentParser(description = "Delete all archived GitHub repos in Snyk")

# Adding optional argument
parser.add_argument("-d", "--delete", action = 'store_true', help = "Delete repos in Snyk (a dry run is run by default)")
parser.add_argument("--github-org", help = 'GitHub org name, as seen in the GitHub repo URL')
parser.add_argument("--github-pat", help = 'GitHub classic PAT with "Metadata" repository permissions (read) scope')
parser.add_argument("--snyk-token", help = 'Snyk API token or service account')
parser.add_argument("--snyk-org", help = 'Snyk Org ID, e.g. 1aaaaaaa-2bbb-3ccc-4ddd-5eeeeeeeeeee')
parser.add_argument("-s", "--bypass-ssl", action = 'store_true', help = "Bypass SSL verification (not recommended)")

args = parser.parse_args()

GITHUB_ORG = args.github_org
GITHUB_PAT = args.github_pat
SNYK_TOKEN = args.snyk_token
SNYK_ORG = args.snyk_org
VERIFY_SSL = not args.bypass_ssl

def get_github_repos():
    url = f'https://api.github.com/orgs/{GITHUB_ORG}/repos?per_page=100'

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {GITHUB_PAT}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    return requests.request("GET", url, headers=headers, data={}, verify=VERIFY_SSL)

def get_targets_page(next_url):
    headers = {  'Authorization': f'token {SNYK_TOKEN}' }

    return requests.request("GET", f'https://api.snyk.io{next_url}', headers=headers, data={}, verify=VERIFY_SSL)

def get_all_targets():
    all_targets = []
    next_url = f'/rest/orgs/{SNYK_ORG}/targets?version=2024-09-04&limit=100'
    while next_url:
        res_body = get_targets_page(next_url).json()
        next_url = res_body.get('links').get('next')
        all_targets = all_targets + res_body['data']

    return all_targets

def delete_target(target_id):
    headers = {  'Authorization': f'token {SNYK_TOKEN}' }

    return requests.request("DELETE", f'https://api.snyk.io/rest/orgs/{SNYK_ORG}/targets/{target_id}?version=2024-09-04', headers=headers, data={}, verify=VERIFY_SSL)

repos = get_github_repos().json()
snyk_targets = get_all_targets()

print("All archived repos:")
archived_repos = set()
for repo in repos:
    if repo['archived']:
        archived_repos.add(repo['full_name'])
        print('    ', repo['full_name'])

print("\nArchived repos in Snyk:")
archived_repos_in_snyk = []
for target in snyk_targets:
    target_name = target['attributes']['display_name']
    if target_name in archived_repos:
        archived_repos_in_snyk.append(target)
        print('    ', target_name)

if args.delete:
    print('\nDeleting repos in Snyk:')
    for target in archived_repos_in_snyk:
        print('    Deleting', target['attributes']['display_name'], '...')
        res = delete_target(target['id'])
        print('   ', res.status_code)

