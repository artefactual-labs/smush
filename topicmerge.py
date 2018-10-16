from __future__ import print_function
import git


class TopicMerge:
    def __init__(self, base_branch, topic_branch, delete_local=False):
        self.base_branch = base_branch
        self.topic_branch = topic_branch
        self.delete_local = delete_local

        try:
            # Throws error if not in a Git repository
            git.Repo(path='.', search_parent_directories=True).git_dir

            self.g = git.cmd.Git('.')
        except git.exc.InvalidGitRepositoryError:
            raise Exception('Not a valid git repository.')

    def update_base_and_rebase_topic(self):
        # Make sure base branch is up to date
        print('Checking out base branch...')
        self.g.checkout(self.base_branch)
        print('Updating base branch...')
        self.g.pull('--rebase')

        # Rebase topic branch
        print('Checking out topic branch..')
        self.g.checkout(self.topic_branch)
        print('Updating topic branch with work from base branch...')
        self.g.rebase(self.base_branch)

        # Push rebased version (so it'll get marked as merged later if on
        # Github)
        print('Pushing updated topic branch...')
        self.g.push('--force')

    def merge_and_cleanup(self):
        print('Checking out base branch and merging topic branch...')
        self.g.checkout(self.base_branch)
        self.g.merge('--ff-only', self.topic_branch)

        # Push merge and delete topic branch
        print('Pushing base branch with topic branch merged...')
        self.g.push()
        print('Deleting topic branch...')
        self.g.push('origin', ':{}'.format(self.topic_branch))

        # Optionally delete local topic branch
        if self.delete_local:
            print('Deleting local topic branch.')
            self.g.branch('-D', self.topic_branch)

    def active_branch(self):
        return git.Repo(path='.', search_parent_directories=True).active_branch.name

    def unmerged_log(self):
        return self.g.log('{}..{}'.format(self.base_branch, self.topic_branch))

    def unmerged_total(self):
        return int(self.g.rev_list('--count', '{}..{}'.format(self.base_branch, self.topic_branch)))
