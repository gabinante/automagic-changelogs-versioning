#!/usr/bin/env python
# pylint: disable=C0103

"""
- Creates change log by taking two git shas as input.
For usage, see:
./create_changelog.py --help
Pre-requisites:
    * pip install -r requirements.txt
"""
import logging
import os
import json
import shutil
import click
import git

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# pylint: disable=too-many-instance-attributes, E1101, W0703
@click.command()
@click.option(
    '--repo', '-r',
    help='the repo to clone and generate a changelog for'
)
@click.option(
    '--from_sha', '-f',
    help='sha to create changelog from'
)
@click.option(
    '--to_sha', '-t',
    help='sha to create changelog up to'
)
@click.option(
    '--version', '-v',
    help='current semantic version for changelog header, format example 3.0.0.123'
)

def generate_change_log(repo:str, from_sha:str, to_sha:str, version:str):
    """
    :param repo <str> The git repository of the module
    :param from_sha <str> git sha for changelog start (first entry)
    :param to_sha <str> git sha for changelog end
    :param version <str> the semantic version for the changelog
    :return None
    """
        file_name = f"changelog-{version}"

        git.Repo.clone_from('ssh://git@git.corp.whatever/repo/'+repo, 'tmp-'+repo)

        # # This isn't exactly how we're doing it so I wrote some pseudocode --
        # # The idea is that you can have a manifest which maps your
        # # semantic versions to git shas. Then this script becomes more user-friendly
        # # and can be invoked using from_version and to_version rather than git shas
        # manifest = json.load(manifest.json')
        # from_sha = manifest[from_version]['sha']
        # to_sha = manifest[to_version]['sha']

        repo = git.Repo('tmp-'+repo)
        logs = repo.git.log("--oneline", from_sha+".."+to_sha).splitlines()
        # if the changelog file exists, we can append to it. This allows for looping
        # if a changelog is being generated for multiple modules in a project.
        if os.path.exists(file_name):
            append_write = 'a'
        else:
            append_write = 'w'
        with open(file_name,append_write) as f:
            f.write(f"\n========== {repo} ==========\n")
            for log in logs:
                if is_valid_commit(log):
                    f.write(log+"\n")
        shutil.rmtree('tmp-'+repo, ignore_errors=False)
        LOG.info("Change log file changelog-%s-%s is created locally"

        # Clean up temporary files
        shutil.rmtree('tmp-repo', ignore_errors=False)
        os.remove(f'{from_version}.json')
        os.remove(f'{to_version}.json')
    except Exception as e:
        LOG.error("Failed to create change log  %s", e)


def is_valid_commit(msg):
    """
    Checks is the commit message is eligible for a changelog entry
    msg: str
    return: bool
    """
    # Exclude ci incrementing versions, tests, and 3-way merges. Squash merges are
    # used to avoid Merge commits like this, but just in case that process doesn't happen.
    exclude_list = ["ci: automated version update", "Merge pull request",
                    "test: ", "ci: trigger build"]

    for i in exclude_list:
        if i in msg:
            return False
    return True


if __name__ == "__main__":
    generate_change_log()
