#MenuTitle: Git previous commit
#!/usr/bin/env python
# coding: utf-8
'''
WARNING: This is ghetto as hell.

Reload the glyph file to the previous commit.
'''
import os
import git
import re

font = Glyphs.font
font_path = font.filepath

repo = git.Git(os.path.dirname(font_path))
git_commits = re.findall(r'(?<=commit ).*', repo.log())

font.close()
commit = git_commits.pop(1)
branch = repo.branch().split('\n  ')[-1]
repo.checkout(commit)
font = Glyphs.open(font_path)
Glyphs.showMacroWindow()
print 'On commit %s, branch %s' % (commit, branch)
