
class MDLogger(object):
    """Generate reports formatted in structured text"""
    def __init__(self):
        self.rows = []

    def header1(self, text):
        self.rows.append('# %s' % text)

    def header2(self, text):
        self.rows.append('## %s' % text)

    def test(self, text):
        self.rows.append('\n### Test: %s' % text)

    def passed(self, text):
        self.rows.append('PASS: %s' % text)

    def failed(self, text):
        self.rows.append('**ERROR: %s**' % text)

    def bullet(self, text):
        self.rows.append('- %s' % text)

    def bullets(self, a):
        for item in a:
            self.rows.append('- %s' % item)

    def clear(self):
        self.rows = []

    def __str__(self):
        return '\r'.join(self.rows)


logger = MDLogger()
logger.clear()