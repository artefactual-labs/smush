from __future__ import print_function
from builtins import input
import argparse
import os
import subprocess
import github
import yaml
from smush import GitLogStyleChecker


def arg_parser():
    """Return ArgumentParser for this application."""
    parser = argparse.ArgumentParser(
        description='Automate merging of feature branches.')

    parser.add_argument('topic_branch', nargs='?', metavar='topic_branch',
                        type=str, help='feature branch to merge')
    parser.add_argument('-n', '--new', action='store_true', default=False)
    parser.add_argument('-c', '--check', action='store_true', default=False)
    parser.add_argument('-d', '--delete-local', action='store_true', default=False)
    parser.add_argument('-p', '--profile')

    # Arguments that can be used instead of, or to override, configuration
    parser.add_argument('-b', '--base-branch', nargs='?', metavar='base branch', type=str)
    parser.add_argument('-o', '--github-owner', nargs='?', metavar='Github owner', type=str)
    parser.add_argument('-r', '--github-repo', nargs='?', metavar='Github repo', type=str)

    parser.add_argument('-v', '--version', action='store_true', help='display version and exit')

    parser.add_argument('--skip-style-check', action='store_true')
    parser.add_argument('--skip-pr-check', action='store_true')

    return parser


def load_config(profile=None, base_branch=None):
    """Return configuration, from YAML file, for this application.

    Args:
        profile (str, optional): name for profile (allows multiple configurations).
        base_branch (str, optional): base branch (supplied outside of configuration).

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
    config = {}

    # Make sure config file exists if needed
    if not os.path.isfile(config_path) and base_branch is None:
        raise Exception('Unable to open ~/{}: does it exist?'.format(config_filename))
    else:
        config = yaml.safe_load(open(config_path))

    # Verify base branch has been set in the config file
    if 'base branch' not in config and base_branch is None:
        raise Exception('Please set "base branch" in {} or specify via --base-branch.'.format(config_filename))

    return config


def check_topic_branch_commits(merge, skip_style_check=False, syntax_check_scripts=None):
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

    # Show files with other errors
    if syntax_check_scripts:
        print('Checking unmerged files...')

        error_messages = []

        for filepath in merge.unmerged_files():
            filename, file_extension = os.path.splitext(filepath)
            file_extension = file_extension[1:]

            if isinstance(syntax_check_scripts, dict) and file_extension in syntax_check_scripts:
                print('Checking ' + filepath + '...')

                check_command = syntax_check_scripts[file_extension].format(filepath)
                process = subprocess.Popen(check_command, shell=True, stdout=subprocess.PIPE)
                process.wait()

                if process.returncode > 0:
                    error_messages.append('Error found in ' + filepath)

        if len(error_messages):
            for error_message in error_messages:
                print(error_message)

        print('Check complete.')


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
