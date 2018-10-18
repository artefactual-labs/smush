from __future__ import print_function
from builtins import input
import argparse
import os
import sys
import yaml


def arg_parser():
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
        abort('Unable to load ~/{}: does it exist?'.format(config_filename))

    # Verify QA branch has been set in the config file
    if 'base branch' not in config:
        abort('Please set "base branch" in {}.'.format(config_filename))

    return config


def abort(error_message):
    print(error_message)
    sys.exit(1)


def get_confirmation(prompt):
    confirm = input('{} [y/n] '.format(prompt))
    return len(confirm) and confirm[0].lower() == 'y'
