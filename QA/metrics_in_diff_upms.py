#MenuTitle: Show Metric keys at different upms
'''
Display the value of each metric key for 1000, 1024 and 2048 upm values.
'''

font = Glyphs.font
Glyphs.showMacroWindow()

UPMS = [
    1000,
    1024,
    2048,
]


def main():
    print 'Showing metrics keys at different upms'
    for master in font.masters:
        for upm in UPMS:
            print '\n**Master: %s upm: %s**' % (master.name, upm)
            for field in master.customParameters:
                if int(field.value):
                    print field.name, int((float(field.value) / font.upm) * upm)

if __name__ == '__main__':
    main()
