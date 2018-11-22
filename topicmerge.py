from __future__ import print_function
import git


class TopicMerge:
    def __init__(self, base_branch, topic_branch, delete_local=False):
        """Create topic branch merge helper instance.

        Args:
            base_branch (str): Base branch.
            topic_branch (str): Topic branch.
            delete_local (bool, optional): Whether or not to delete topic
                branch after merge.
        """
        self.base_branch = base_branch
        self.topic_branch = topic_branch
        self.delete_local = delete_local

        try:
            # Throws error if not in a Git repository
            self.repo = git.Repo(path='.', search_parent_directories=True)
            self.git = git.cmd.Git('.')
        except git.exc.InvalidGitRepositoryError:
            raise Exception('Not a valid git repository.')

        if not self.branch_exists(base_branch):
            raise Exception("Base branch '{}' not checked out locally.".format(base_branch))

    def update_base_branch(self):
        """Update base branch and rebase topic branch."""
        # Make sure base branch is up to date
        print('Checking out base branch...')
        self.git.checkout(self.base_branch)
        print('Updating base branch...')
        self.git.pull('--rebase')

    def rebase_topic_branch_and_push(self):
        """Rebase topic branch with work from base branch and push."""
        # Rebase topic branch
        print('Checking out topic branch..')
        self.git.checkout(self.topic_branch)
        print('Updating topic branch with work from base branch...')
        self.git.rebase(self.base_branch)

        # Push rebased version (so it'll get marked as merged later if on
        # Github)
        print('Pushing updated topic branch...')
        self.git.push('--force')

    def merge_and_cleanup(self):
        """Merge topic branch then delete remotely and, optionally, locally."""
        print('Checking out base branch and merging topic branch...')
        self.git.checkout(self.base_branch)
        self.git.merge('--ff-only', self.topic_branch)

        # Push merge and delete topic branch
        print('Pushing base branch with topic branch merged...')
        self.git.push()
        print('Deleting remote topic branch...')
        self.git.push('origin', ':{}'.format(self.topic_branch))

        # Optionally delete local topic branch
        if self.delete_local:
            print('Deleting local topic branch...')
            self.git.branch('-D', self.topic_branch)

    def check_out_topic_branch_from_remote(self):
        """Check out local version of topic branch."""
        base_branch_remote = self.git.config('--get', 'branch.{}.remote'.format(self.base_branch))
        self.git.checkout('-b', self.topic_branch, '{}/{}'.format(base_branch_remote, self.topic_branch))

    def active_branch(self):
        """Return name of active branch."""
        return self.repo.active_branch.name

    def branch_exists(self, branch):
        """Check whether a branch exists in the current repository.

        Args:
            branch (str): Name of branch that may or may not exist.

        Returns:
            bool: True if branch exists, otherwise false.
        """
        return branch in self.repo.branches

    def unmerged_log(self):
        """Return Git log output for unmerged commits."""
        return self.git.log('{}..{}'.format(self.base_branch, self.topic_branch))

    def unmerged_total(self):
        """Return number of unmerged commits."""
        return int(self.git.rev_list('--count', '{}..{}'.format(self.base_branch, self.topic_branch)))
