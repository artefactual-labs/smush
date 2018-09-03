smush
=====

Script to automate merging of feature branches

Usage: `smush <dev branch>`

Does the following:

1. Optionally shows text reminders (from config file) before merge
2. Optionally verify (depending on config file settings) if open pull request exists for dev branch
3. Updates QA branch
4. Rebases dev branch using QA
5. Force pushes dev branch
6. Allows optional interactive rebasing if more than one commit is to be merged
7. Displays unmerged commits
8. Displays commit style issues (see **Style Checking**)
9. Asks confirmation to go ahead with merge
10. Merges dev branch into QA
11. Pushes QA branch
12. Deletes dev branch
13. Optionally shows reminders (from config file) after merge

The `--skip-pr-check` option skips step 2 of the above sequence.

The `--skip-style-check` option skips step 8 of the above sequence.

Installation
------------

1. Install the required Python modules:

    pip install -r requirements.txt

2. Stick the `smush` script somewhere you can run it from.

Configuration
-------------

Edit the $HOME/.smush.yml YAML-formatted config file and set `qa branch` to desired QA branch.

Example:

    qa branch: qa/2.5.x

Setting `github owner` and `github repo` in your configuration file can, optionally, enable you
to have smush check to make sure an open pull request exists for the dev branch.

Setting `before notes` in your configuration file can, optionally, display
notes/reminders before you merge. Likewise, setting `after notes` can display
notes/reminders after you merge.

Style checking
--------------

The commit style check checks commit messages to make sure that:

1. The first line of the commit message (described as the "subject line") isn't
   over 50 characters in length.

2. Subsequent lines in the commit message aren't over 72 characters in length.

3. There's a blank line between the first line of the commit message and any
   subsequent lines.

This convention, and the reasoning behind it, is described here:

https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
