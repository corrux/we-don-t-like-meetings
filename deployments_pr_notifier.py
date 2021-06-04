from github import Github
import yaml
import sys
import requests
import json


def post_message_to_slack(slack_webhook_url, text, blocks = None):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return requests.post(slack_webhook_url, data=json.dumps({"text": text}), headers=headers)


# using an access token
with open(sys.argv[1], "r") as f:
    config = yaml.safe_load(f)
gh = Github(config["github_access_token"])
slack_webhook_url = config["slack_webhook_url"]
release_pr_author = config["release_pr_author"]

# Pull Requests on GitHub have to include certain keywords in title for this to work
issues = gh.search_issues('', state='open', author=release_pr_author, type='pr')
release_pr = [pr for pr in issues if 'Release' or 'release' in pr.title]
staging_release_pr = [pr for pr in release_pr if 'Staging' in pr.title or 'staging' in pr.title]
prod_release_pr = [pr for pr in release_pr if 'Production' in pr.title or 'production' in pr.title]

if no_of_prs == 0:
    sys.exit()

post_message_to_slack(slack_webhook_url,
                      f'{len(release_pr)} deployment(s) for today (as per GitHub):'
                      f' {len(staging_release_pr)} for staging, {len(prod_release_pr)} for production!')