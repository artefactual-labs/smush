smush
=====

Script to automate merging of topic branches

Summary
-------

This script automates steps required to cleanly merge a topic branch into a
base branch. No merge commits are made. Before merging, the topic branch is
rebased so it can be merged using `--ff-only` then pushed.

If using GitHub, and a pull request exists for the topic branch, the pull
request will be automatically marked as merged and closed.

Functionality
-------------

Usage: `smush <topic branch>`

Does the following:

1. Optionally verify (depending on config file settings) if open pull request
  exists for topic branch
2. Optionally verify (depending on config file settings) if pull request base
  branch matches configuration
3. Optionally shows text reminders (from config file) before merge
4. Updates base branch
5. Rebases topic branch using base branch
6. Force pushes topic branch
7. Allows optional interactive rebasing if more than one commit is to be merged
8. Displays unmerged commits
9. Displays commit style issues (see **Style Checking**)
10. Asks confirmation to go ahead with merge
11. Merges topic branch into base branch
12. Pushes base branch
13. Deletes topic branch
14. Optionally delete local topic branch
15. Optionally shows reminders (from config file) after merge

The `--skip-pr-check` option skips step 2 of the above sequence.

The `--skip-style-check` option skips step 8 of the above sequence.

The `--delete-local` option deletes the local topic branch.

Installation
------------

1. Install the required Python modules:

    pip install -r requirements.txt

2. Stick the `smush` script somewhere you can run it from.

Configuration
-------------

Edit the `$HOME/.smush.yml` YAML-formatted configuration file and set
`base branch` to desired base branch.

Example:

    base branch: qa/2.5.x

Setting `github owner` and `github repo` in your configuration file can,
optionally, enable you to have smush check to make sure an open pull request
exists for the topic branch.

Setting `before notes` in your configuration file can, optionally, display
notes/reminders before you merge. Likewise, setting `after notes` can display
notes/reminders after you merge.

The `--profile` option can be used to load an alternative configuration. Using
`--profile=backport`, for example, would result in `$HOME/.smush-backport.yml`
being used as a configuration file.

Style checking
--------------

The commit style check checks commit messages to make sure that:

1. The first line of the commit message (described as the "subject line") isn't
   over 50 characters in length.

2. Subsequent lines in the commit message (described as "body lines") aren't
   over 72 characters in length.

3. There's a blank line between the subject line of the commit message and any
   subsequent body lines.

This convention, and the reasoning behind it, is described here:

https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

If you want to check the style of a branch without merging it, you can use the
`--check` option.
