from __future__ import print_function
from builtins import input
import argparse
import os
import subprocess
import sys
import github
import yaml
from git_log_style_checker import GitLogStyleChecker


def arg_parser():
    """Return ArgumentParser for this application."""
    parser = argparse.ArgumentParser(
        description='Automate merging of feature branches.')

    parser.add_argument('topic_branch', metavar='topic_branch', type=str,
                        help='feature branch to merge')
    parser.add_argument('--check', action='store_true', default=False)
    parser.add_argument('--skip-style-check', action='store_true')
    parser.add_argument('--skip-pr-check', action='store_true')
    parser.add_argument('--delete-local', action='store_true', default=False)
    parser.add_argument('--profile')

    return parser


def load_config(profile):
    """Return configuration, from YAML file, for this application.

    Args:
        profile (str, optional): name for profile (allows multiple configurations).

    Raises:
        Exception: If not able to read or parse the configuration file for any
                   reason or if "base branch" isn't set in the configuration
                   file.

    Returns:
        dict: Configuration information.
    """
    # Assemble configuration file name
    config_filename = '.smush'
    if profile:
        config_filename += '-' + profile
    config_filename += '.yml'

    # Attempt to load configuration file from user's home directory
    config_path = os.path.join(os.path.expanduser('~'), config_filename)

    try:
        config = yaml.safe_load(open(config_path))
    except:
        raise Exception('Unable to load ~/{}: does it exist?'.format(config_filename))

    # Verify base branch has been set in the config file
    if 'base branch' not in config:
        raise Exception('Please set "base branch" in {}.'.format(config_filename))

    return config


def check_topic_branch_commits(merge, skip_style_check=False):
    """Check topic branch commit(s) for issues.

    Args:
        merge (TopicMerge): Abstraction to make it easier to work with topic branch.
        skip_style_check (bool, optional): Whether to skip style check.

    Raises:
        Exception if not unmerged commits are found.
    """
    starting_branch = merge.active_branch()

    # Determine number of new commits and offer to rebase if greater than one
    if merge.unmerged_total() > 1:
        display_unmerged_commits(merge)

        print('There is more than one new commit present in dev branch.')
        if get_confirmation('Would you like to interactively rebase?'):
            merge.git.checkout(merge.topic_branch)
            subprocess.call(['git', 'rebase', '-i', 'HEAD~' + str(merge.unmerged_total())])
            print('Updating dev branch...')
            merge.git.push('--force')
            merge.git.checkout(starting_branch)
    elif merge.unmerged_total() == 0:
        raise Exception('No unmerged commits found.')

    # Display unmerged commits in dev branch
    display_unmerged_commits(merge)

    # Show commit style errors
    if not skip_style_check:
        checker = GitLogStyleChecker(merge.unmerged_log())
        print(checker.summarize_style_errors())


def check_for_pull_request(config, topic_branch):
    """ Check to make sure pull request for topic branch exists on Github.

    Uses Github owner/repository information and base branch from the
    application configuration to check Github to make sure an open pull
    request exists for the topic branch against the appropriate base branch.

    Args:
        config (dict): Application configuration.
        topic_branch (str): Topic branch.

    Raises:
        Exception: if the Github repository can't be found, a pull request
                   can't be found, or the pull request's base branch isn't
                   correct.
    """
    # Prepare to access Github repository
    try:
        repo = github.Github().get_repo("{}/{}".format(config['github owner'], config['github repo']))
    except github.UnknownObjectException:
        raise Exception('Github repository not found.')

    # Cycle through pulls request to find the first one for the topic branch
    pr = None
    for pull in repo.get_pulls(state='open'):
        if pull.head.ref == topic_branch:
            pr = pull

    # Report an error finding an appropriate pull request
    if not pr:
        raise Exception('Could not find pull request for this topic branch. Use --skip-pr-check option to skip.')
    elif pr.base.ref != config['base branch']:
        error_message = "The pull request's base is {}, not {}.".format(pr.base.ref, config['base branch'])
        raise Exception(error_message)


def display_unmerged_commits(merge):
    """Print unmerged commits with a blank line above and below."""
    print()
    print(merge.unmerged_log())
    print()


def get_confirmation(prompt):
    """Ask use to confirm an action."""
    confirm = input('{} [y/n] '.format(prompt))
    return len(confirm) and confirm[0].lower() == 'y'
