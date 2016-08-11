'''
Find duplicate glyphs
'''
from collections import Counter


def main():
    # Add README file if it does not exist

    font = Glyphs.font
    glyphs_count = Counter([g.name for g in font.glyphs])
    for glyph in glyphs_count:
        if glyphs_count[glyph] >= 2:
            print glyph


if __name__ == '__main__':
    main()
