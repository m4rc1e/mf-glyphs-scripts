VERT_KEYS = [
    'typoDescender',
    'typoLineGap',
    'hheaLineGap',
    'hheaAscender',
    'typoAscender',
    'hheaDescender',
    'winDescent',
    'winAscent',
]

def synced(layer, masters):
    '''Check if masters share same vertical metrics'''
    print '***Checking %s share same vert metrics***' % layer
    bad_masters = []
    for master1 in masters:
        for master2 in masters:
            for key in VERT_KEYS:
                if key not in master1.customParameters:
                    print 'ERROR: %s %s is missing in %s\n' %(layer, key, master1.name)
                    print 'Add all Vertical metrics parameters first!'
                    return False
                if master1.customParameters[key] != master2.customParameters[key]:
                    bad_masters.append((layer, master1.name, master2.name, key))
    
    if bad_masters:
        for layer, master1, master2, key in bad_masters:
            print "ERROR: %s's %s %s %s not even. Fix first!\n" % (layer, master1, master2, key)
        return False
    else:
        print 'PASS: %s share same metrics\n' % layer
        return True
