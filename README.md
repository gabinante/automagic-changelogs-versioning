# Automagic changelogs and versioning

# Is this going to work out of the box?
No. A bunch of legwork is required to make this function -- both at the team level, getting buyin
for using conventional commits, etc. and at the CI level, enforcing conventional commits, introducing parsing,
adding the versioning process to your current automation. Sorry.

# Commits
All commits must use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard.
We'll check for this in CI to ensure that commits are formatted properly, and we reject non-standard
commits. This allows for machine parsing of commits and is the basis for both changelog generation and
automated semantic versioning.

# Merges
Merges should be done using squash methodology, and will trigger a CI job that updates the version.
We don't use three-way merges because they create an extra commit which is useless and annoying.
If you know what you're doing, or are prone to large changesets with well-articulated commits pre-push,
there are other merging strategies which can work as well -- but generally commits
should be squashed into a single conventional commit that details a summary of changes.
Some magic is done in the jenkinsfile to prevent an infinite loop of version updates, and to ignore accidental
three-way merge commits.

# Changelogs
Changelogs are built from conventional commits using generate_changelog.py
example usage:
`python generate_changelog.py -r myrepo -from_sha 1eb4a5e018ef7673de72a6393d4a33 -to_sha 9b87613f0bcff1940f4c6b971c -v 1.0.1`

# Resources
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
[Commitizen](https://github.com/commitizen/cz-cli)
