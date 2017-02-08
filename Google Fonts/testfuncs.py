from utils import logger
import operator
import re

OPERATORS = {
    '>=': operator.ge,
    '==': operator.eq,
    '<=': operator.le
}


def compare(arg1_name, arg1_val, op, arg2_name, arg2_val):
    '''Compare two arguements.'''
    if OPERATORS[op](arg1_val, arg2_val):
        logger.passed('%s %s is %s to %s %s' %
            (arg1_name, arg1_val, op, arg2_name, arg2_val))
        return True
    logger.failed('%s %s is not %s to %s %s' %
        (arg1_name, arg1_val, op, arg2_name, arg2_val))
    return False


def consistent(arg_name, a):
    if len(set(a)) == 1:
        logger.passed("%s is consistent, %s" % (
            arg_name, a[0]))
        return True
    logger.failed("%s is inconsistent, %s" % (
        arg_name, ', '.join(map(str, a))))
    return False


def leftover(set1_name, set1, set2_name, set2):
    sub = set1 - set2
    if len(set1 - set2) == 0:
        logger.passed("%s matches %s" % (
            set2_name,
            set1_name,
        ))
        return True
    logger.failed("%s when compare to %s, is missing:\n%s" % (
        set2_name,
        set1_name,
        '\n'.join(sub),
    ))
    return False


def enabled(arg_name, arg):
    if arg:
        logger.passed('%s is enabled' % arg_name)
        return True
    logger.failed('%s is disabled' % arg_name)
    return False


def contains(segment, item):
    if segment in item:
        logger.passed('%s is in %s' % (segment, item))
        return True
    logger.failed('%s not in %s' % (segment, item))
    return False


def regex_contains(string_name, pattern, string):
    match = re.match(pattern, string)
    if match:
        logger.passed("%s matches %s" % (string_name, pattern))
        return True
    logger.failed("%s does not match %s" % (string_name, pattern))
    return False


def exists(item_name, item):
    if item:
        logger.passed('%s exists' % item_name)
        return True
    logger.failed('%s does not exist' % item_name)
    return False
