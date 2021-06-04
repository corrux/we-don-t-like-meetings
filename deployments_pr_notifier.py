import os
import yaml
import sys

from github import Github
import requests
import json


def post_message_to_slack(slack_webhook_url, text, blocks = None):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return requests.post(slack_webhook_url, data=json.dumps({"text": text}), headers=headers)


# using an access token
gh = Github(os.getenv("GH_ACCESS_TOKEN"))
slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
release_pr_author = os.getenv("RELEASE_PR_AUTHOR")

# Pull Requests on GitHub have to include certain keywords in title for this to work
issues = gh.search_issues('', state='open', author=release_pr_author, type='pr')
release_pr = [pr for pr in issues if 'Release' or 'release' in pr.title]
staging_release_pr = [pr for pr in release_pr if 'Staging' in pr.title or 'staging' in pr.title]
prod_release_pr = [pr for pr in release_pr if 'Production' in pr.title or 'production' in pr.title]

no_of_prs = len(release_pr)

post_message_to_slack(slack_webhook_url,
                      f'{no_of_prs} deployment(s) for today (as per GitHub):'
                      f' {len(staging_release_pr)} for staging, {len(prod_release_pr)} for production!')