#MenuTitle: Git latest commit
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
Glyphs.showMacroWindow()

repo = git.Git(os.path.dirname(font_path))
branch = repo.branch()

if '\n' in branch:
    branch = branch.split('\n  ')[-1]
    font.close()
    repo.checkout(branch)
    font = Glyphs.open(font_path)
    print 'On latest commit, branch %s' % (branch)
else:
    branch = repo.branch().split('* ')[-1]
    print 'Already on latest commit, branch %s' % (branch)
