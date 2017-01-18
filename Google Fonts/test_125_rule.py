#MenuTitle: Test vertical metric sets are between 120-125% of upm
# -*- coding: utf-8 -*-
'''
Check each master's font metrics sets are between 120-125% of upm
[Discussion](http://tinyurl.com/zlozasg)
'''
from vertmetrics import VERT_SETS
from test_masters_vert_keys import test_font_vert_keys
from utils import logger


def master_vert_metrics_125(master, ignore='win'):
    vert_metrics = []

    # loop through typo, hhea and win vert sets
    for vert_set in VERT_SETS:
        if vert_set is ignore:
            continue
        vert_set_name = vert_set
        vert_set = VERT_SETS[vert_set]

        v_set_total = sum([abs(master[k]) for k in vert_set])

        v_set_a = {
            'category': vert_set_name,
            'total': v_set_total,
            }

        if v_set_total < 1250 and v_set_total > 1200:
            v_set_a['passed'] = True
        else:
            v_set_a['passed'] = False
        vert_metrics.append(v_set_a)
    return vert_metrics


def test_metrics_under_125(masters):
    bad_masters = []

    logger.test("Vertical metric sets are between 120-125% of upm")
    for master in masters:
        vert_metrics = master_vert_metrics_125(master.customParameters)
        for vert_set in vert_metrics:
            log_string = '%s %s total is %s' % (
                master.name,
                vert_set['category'],
                vert_set['total'],
            )
            if vert_set['passed']:
                logger.passed(log_string)
            else:
                bad_masters.append(master.name)
                logger.failed('%s, target range is 1200-1250' % log_string)

    if bad_masters:
        return False
    return True


if __name__ == '__main__':
    logger.header1('Running %s' % __file__)
    font = Glyphs.font
    Glyphs.showMacroWindow()
    logger.header2('Conducting preflight tests:')
    if test_font_vert_keys(font.masters):
        logger.header2('Starting test')
        test_metrics_under_125(font.masters)
    else:
        logger.header2('Starting test')
        logger.failed('Test could not start, add all metric keys first!')
    print logger
    logger.clear()
