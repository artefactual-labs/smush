smush
=====

Script to automate merging of feature branches

Usage: `smush <dev branch>`

Does the following:

1. Updates QA branch
2. Rebases dev branch using QA
3. Forces push dev branch
4. Merges dev branch into QA
5. Pushes QA branch
6. Deletes dev branch

Installation
------------

1. Install the required Python modules:

    pip install -r requirements.txt

2. Stick the "smush" script somewhere you can run it from.

Configuration
-------------

Edit $HOME/.smush.yml and set "qa branch" to desired QA branch.

Example:

    qa branch: qa/2.5.x

Setting "before notes" in your configuration file can, optionally, display
notes/reminders before you merge. Likewise, setting "after notes" can display
notes/reminders after you merge.
