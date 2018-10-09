from __future__ import print_function
import json
import subprocess
import sys
import urllib2


def check_for_valid_pull_request(config, base_branch, dev_branch):
    pr = get_open_pull_request_for_branch(config['github owner'], config['github repo'], dev_branch)
    if not pr:
        app.abort('There is no open pull request for this branch.')
    if pr['base']['ref'] != base_branch:
        app.abort("This pull request's base is {}, not {}.".format(pr['base']['ref'], base_branch))


def get_open_pull_request_for_branch(owner, repo, branch):
    pr_url = 'https://api.github.com/repos/{}/{}/pulls?state=open'.format(owner, repo)
    unparsed_result = urllib2.urlopen(pr_url).read()
    pull_requests = json.loads(unparsed_result)

    for pr in pull_requests:
        if pr['head']['ref'] == branch:
            return pr
