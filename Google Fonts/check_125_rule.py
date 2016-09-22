#MenuTitle: Check 125% metrics rule
# -*- coding: utf-8 -*-
'''
Check 125% metrics rule.
'''


def main():
    font = Glyphs.font
    masters = font.masters
    Glyphs.showMacroWindow()

    high_glyph = 0
    for i, master in enumerate(masters):
        try:
            m_asc = size = master.customParameters['typoAscender']
            m_desc = abs(master.customParameters['typoDescender'])
            typo_v_size = m_asc + m_desc
        except TypeError:
            print('missing custom Parameter vertical metric keys')
            raise

        rule = font.upm * 1.25
        if typo_v_size >= rule:
            print 'PASS: typo asc + desc size is %s, whilst 125 of metrics is %s' % (
                   typo_v_size, rule
            )
        else:
            print 'ERROR: typo asc + desc size is %s, whilst 125 of metrics is %s' % (
                   typo_v_size, rule
            )


if __name__ == '__main__':
    main()
