#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import git
import csv
import tqdm


# specify the path to the Git repository
repo_path = "pdfbox"

# create a Git repo object
repo = git.Repo(repo_path)

output = []

for i in tqdm.trange(1, 6000):
    # specify the regular expression for the issue number pattern
    issue_pattern = r"PDFBOX-"+str(i)

    # execute git log with --grep option
    commit_hash = repo.git.log(
        "trunk", "--grep=" + issue_pattern, "--format=%H").split("\n")
    if len(commit_hash) == 1 and commit_hash[0] == '':
        continue
    commit_hash = set(commit_hash)

    M = 0
    A = 0
    D = 0

    for hash_ in (commit_hash):
        commit = repo.commit(hash_)

        modified_files = [item.a_path for item in commit.diff(
            commit.parents[0]) if item.change_type == "M"]
        num_modified_files = len(modified_files)
        M = M + num_modified_files

        added_files = [item.a_path for item in commit.diff(
            commit.parents[0]) if item.change_type == "A"]
        num_added_files = len(added_files)
        A = A + num_added_files

        deleted_files = [item.a_path for item in commit.diff(
            commit.parents[0]) if item.change_type == "D"]
        num_deleted_files = len(deleted_files)
        D = D + num_deleted_files

    output.append([issue_pattern, ','.join(commit_hash), M, A, D])

with open('final_output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['issue_id', 'commit_hash', 'M', 'A', 'D'])
    writer.writerows(output)
