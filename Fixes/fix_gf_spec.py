'''
Fix/add requirements from ProjectChecklist.md
'''
def main():
    # Add README file if it does not exist

    font = Glyphs.font
    font.date = datetime.now()
    font.customParameters['license'] = 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL'
    font.customParameters['licenseURL'] = 'http://scripts.sil.org/OFL'
    font.customParameters['fsType'] = 0
    font.customParameters['Use Typo Metrics'] = True
    if 'panose' in font.customParameters:
        del font.customParameters['panose']
    if 'glyphOrder' in font.customParameters:
        del font.customParameters['glyphOrder']


if __name__ == '__main__':
    main()