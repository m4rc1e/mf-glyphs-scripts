from utils import logger
import operator


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
    else:
        logger.failed('%s %s is not %s to %s %s' %
            (arg1_name, arg1_val, op, arg2_name, arg2_val))
        return False


def consistent(arg_name, a):
    if len(set(a)) == 1:
        logger.passed("%s is consistent, %s" % (
            arg_name, a[0]))
        return True
    logger.failed("%s is inconsistent, %s" % (
        arg_name, ', '.join(a)))
    return False


def leftover(set1_name, set1, set2_name, set2):
    sub = set1 - set2
    if len(set1 - set2) == 0:
        logger.passed("%s matches %s" % (
            set2_name,
            set1_name,
        ))
        return True
    else:
        logger.failed("%s missing %s, compared to %s" % (
            set2_name,
            ', '.join(sub),
            set1_name,
        ))
        return False


def enabled(arg_name, arg):
    if arg:
        logger.passed('%s is enabled' % arg_name)
    else:
        logger.failed('%s is disabled' % arg_name)
 