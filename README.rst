smush
=====

Script to automate merging of topic branches

Summary
-------

This script automates steps required to cleanly merge a topic branch into a
base branch. No merge commits are made. Before merging, the topic branch is
rebased so it can be merged using ``--ff-only`` then pushed.

If merging this way and using GitHub, and a pull request exists for the topic
branch, the pull request will be automatically marked as merged and closed.

Functionality
-------------

Usage: ``smush [topic branch]``

Does the following:


#. Optionally verify (depending on config file settings/CLI options) if open
   pull request exists for topic branch
#. Optionally verify (depending on config file settings/CLI options) if pull
   request base branch matches configuration
#. Optionally shows text reminders (if set in config file) before merge
#. Updates base branch
#. Rebases topic branch using base branch
#. Force pushes topic branch
#. Displays unmerged commits
#. Displays commit style issues (see **Style Checking**\ )
#. Prompts to allow interactive rebasing if more than one commit is to be merged
#. Asks confirmation to go ahead with merge
#. Merges topic branch into base branch
#. Pushes base branch
#. Deletes topic branch
#. Optionally (depending on CLI options) deletes local topic branch
#. Optionally shows reminders (if set in config file) after merge

If no topic branch is specified, the active branch will be used.

The ``--skip-pr-check`` option skips step 2 of the above sequence.

The ``--skip-style-check`` option skips step 8 of the above sequence.

The ``--delete-local`` option deletes the local topic branch.

Installation
------------


#. 
   Install the required Python modules:

    pip install -r requirements.txt

#. 
   Stick the ``smush`` script somewhere you can run it from.


Configuration
-------------

Edit the ``$HOME/.smush.yml`` YAML-formatted configuration file and set
``base branch`` to desired base branch.

Example:

.. code-block::

   base branch: qa/2.5.x

Setting ``github owner`` and ``github repo`` in your configuration file can,
optionally, enable you to have smush check to make sure an open pull request
exists for the topic branch.

Setting ``before notes`` in your configuration file can, optionally, display
notes/reminders before you merge. Likewise, setting ``after notes`` can display
notes/reminders after you merge.

Setting ``syntax check scripts`` in your configuration file can, optionally,
check files, changed by commits in your topic branch, using an external script
that you specify. Different scripts can be specified for different file
extensions.

Example:

.. code-block::

    syntax check scripts:
        php: "php -l {}"

The ``--profile`` option can be used to load an alternative configuration. Using
``--profile=backport``\ , for example, would result in ``$HOME/.smush-backport.yml``
being used as a configuration file.


Use without configuration
-------------------------

Smush can also be run without configuration using command-line options.

Example:

    smush --base-branch="qa/2.6.x" --github-owner="artefactual" \
        --github-repo="atom" dev/issue-13177-remove-js-file-reference


Style checking
--------------

The commit style check checks commit messages to make sure that:


#. 
   The first line of the commit message (described as the "subject line") isn't
   over 50 characters in length.

#. 
   Subsequent lines in the commit message (described as "body lines") aren't
   over 72 characters in length.

#. 
   There's a blank line between the subject line of the commit message and any
   subsequent body lines.

This convention, and the reasoning behind it, is described here:

https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

If you want to check the style of a branch without merging it, you can use the
``--check`` option.

Branch creation
---------------

If you want to create a topic branch, locally and remotely, from the base
branch, you can use the ``--new`` option.
