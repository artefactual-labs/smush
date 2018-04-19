smush
=====

Script to automate merging of feature branches

Usage: `smush <dev branch>`

Does the following:

1. Optionally shows text reminders (from configuration file) before merge
2. Updates QA branch
3. Rebases dev branch using QA
4. Force pushes dev branch
5. Displays unmerged commits
6. Asks confirmation to go ahead with merge
7. Merges dev branch into QA
8. Pushes QA branch
9. Deletes dev branch
10. Optionally shows reminders (from configuration file) after merge

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

Setting "before notes" in your configuration file can, optionally, display
notes/reminders before you merge. Likewise, setting "after notes" can display
notes/reminders after you merge.
