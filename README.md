smush
=====

Script to automate merging of feature branches

Usage: `smush <dev branch>`

Does the following:

1. Optionally shows text reminders (from configuration file) before merge
2. Verifies that an open pull request exists for the dev branch (aborting if one doesn't exist)
3. Updates QA branch
4. Rebases dev branch using QA
5. Force pushes dev branch
6. Allows optional interactive rebasing if more than one commit is to be merged
7. Displays unmerged commits
8. Asks confirmation to go ahead with merge
9. Merges dev branch into QA
10. Pushes QA branch
11. Deletes dev branch
12. Optionally shows reminders (from configuration file) after merge

The `--skip-pr-check` option skips step 2 of the above sequence.

Installation
------------

1. Install the required Python modules:

    pip install -r requirements.txt

2. Stick the "smush" script somewhere you can run it from.

Configuration
-------------

Edit the $HOME/.smush.yml YAML-formatted config file and set "qa branch" to desired QA branch.

Example:

    qa branch: qa/2.5.x

Setting "github owner" and "github repo" in your configuration file can, optionally, enable you
to have smush check to make sure an open pull request exists for the dev branch.

Setting "before notes" in your configuration file can, optionally, display
notes/reminders before you merge. Likewise, setting "after notes" can display
notes/reminders after you merge.
