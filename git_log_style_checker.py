def parse_and_check_git_log_output(log):
    commits = []
    commit = {}
    blank_lines = 0

    for line in log.split("\n"):
        if line.startswith("commit "):
            # Note errors, append commit, reset bookkeeping variables
            if commit != {}:
                check_commit_and_note_style_errors(commit)
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
        check_commit_and_note_style_errors(commit)
        commits.append(commit)

    return commits


def check_commit_and_note_style_errors(commit):
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
            errors.append("Body line {} exceeds 72 characters.".format(line_number))
        line_number += 1

    # Add any errors to commit and append
    if len(errors):
        commit["errors"] = errors
