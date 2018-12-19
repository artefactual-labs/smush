class GitLogStyleChecker:
    def __init__(self, git_log_output):
        """Create git log style checker instance.

        Args:
            git_log_output (str): Git log (no flags set) output to parse/check.
        """
        self.commits = self.parse_and_check_git_log_output(git_log_output)

    def parse_and_check_git_log_output(self, git_log_output):
        """Return array of commit data and related errors.

        Parse git log output and return array of data relating to commits and
        any style errors found.

        Args:
            git_log_output (str): Git log output to parse and check.

        Returns:
            array: Commit information.
        """
        commits = []
        commit = {}
        blank_lines = 0

        for line in git_log_output.split("\n"):
            if line.startswith("commit "):
                # Note errors, append commit, reset bookkeeping variables
                if commit != {}:
                    self.check_commit_and_note_style_errors(commit)
                    commits.append(commit)
                    commit = {}
                    blank_lines = 0
                commit["hash"] = line.replace("commit ", "")
            elif line.startswith("Author: "):
                commit["author"] = line.replace("Author: ", "")
            elif line.startswith("Date:   "):
                commit["date"] = line.replace("Date:   ", "")
            elif "body" not in commit and line.strip() != "":
                commit["header"] = line[4:]
                commit["body"] = []
            elif line.strip() != "":
                # Note if body line appears too early
                if blank_lines == 1:
                    commit["no blank line before body"] = True
                commit["body"].append(line[4:])
            else:
                blank_lines += 1

        if commit != {}:
            self.check_commit_and_note_style_errors(commit)
            commits.append(commit)

        return commits

    def check_commit_and_note_style_errors(self, commit):
        """Add style error information to dict containing commit data.

        Error information, if found, is put into the "errors" key.

        Args:
            commit (dict): Commit data containing commit header and body.
        """
        errors = []

        # Check header
        if len(commit["header"]) > 50:
            errors.append("Subject line exceeds 50 characters.")

        # Check if body occurs directly after header
        if "no blank line before body" in commit:
            errors.append("If multi-line, needs blank line after subject line.")

        # Check lines
        line_number = 1
        for line in commit["body"]:
            if len(line) > 72:
                line_description = 'starting with "{}"'.format(line[:15])
                errors.append("Body line {} ({}) exceeds 72 characters.".format(line_number, line_description))
            line_number += 1

        # Add any errors to commit and append
        if len(errors):
            commit["errors"] = errors

    def summarize_style_errors(self):
        """Return text summary of errors found in commits parsed from the log.

        Returns:
            str: Text summary.
        """
        summary = ''

        # Create text summary of style errors
        for commit in self.commits:
            if "errors" in commit and len(commit["errors"]):
                summary += "Style error(s) found in commit {}:\n\n".format(commit["hash"])

                for line in commit["errors"]:
                    summary += "    {}\n".format(line)

                summary += "\n"

        if summary == '':
            summary += "No style errors found.\n"

        return summary
