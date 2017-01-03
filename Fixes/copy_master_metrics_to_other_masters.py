#MenuTitle: Copy Selected Master's Vert Metrics To Other Masters

METRICS_KEYS = [
    'typoAscender',
    'typoDescender',
    'typoLineGap',
    'hheaAscender',
    'hheaDescender',
    'hheaLineGap',
    'winAscent',
    'winDescent',
]


def main():
    font = Glyphs.font

    selected_master = font.selectedFontMaster
    masters = font.masters

    updates = False
    for master in masters:
        for key in METRICS_KEYS:
            if master.customParameters[key] != selected_master.customParameters[key]:
                print 'Swapping: %s %s, %s for %s %s, %s' % (
                    master.name,
                    key,
                    master.customParameters[key],
                    selected_master.name,
                    key,
                    selected_master.customParameters[key]
                )
                updates = True
                master.customParameters[key] = selected_master.customParameters[key]
    if updates:
        print 'Metrics have been updated'
    else:
        print 'Metric keys are the same'

if __name__ == '__main__':
    main()
