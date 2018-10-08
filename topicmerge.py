from __future__ import print_function
import git


class TopicMerge:
    def __init__(self, base_branch, topic_branch):
        self.base_branch = base_branch
        self.topic_branch = topic_branch

        try:
            # Throws error if not in a Git repository
            git.Repo(path='.', search_parent_directories=True).git_dir

            self.g = git.cmd.Git('.')
        except git.exc.InvalidGitRepositoryError:
            raise Exception('Not a valid git repository.')

    def rebase_topic_branch(self):
        # Make sure QA branch is up to date
        print('Checking out QA branch...')
        self.g.checkout(self.base_branch)
        print('Updating QA branch...')
        self.g.pull('--rebase')

        # Rebase topic branch
        print('Checking out topic branch..')
        self.g.checkout(self.topic_branch)
        print('Updating topic branch with work from QA...')
        self.g.rebase(self.base_branch)

        # Push rebased version (so it'll get marked as merged later if on
        # Github)
        print('Pushing updated topic branch...')
        self.g.push('--force')

    def merge_and_cleanup(self):
        print('Merging topic branch...')
        self.g.merge('--ff-only', self.topic_branch)

        # Push merge and delete topic branch
        print('Pushing base branch with topic branch merged...')
        self.g.push()
        print('Deleting topic branch...')
        self.g.push('origin', ':{}'.format(self.topic_branch))

    def active_branch(self):
        return git.Repo(path='.', search_parent_directories=True).active_branch.name
