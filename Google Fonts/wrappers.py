import vanilla


class GlyphsUI(object):
    '''Dialog for enabling/disabling checks'''
    def __init__(self, title):
        self.w = vanilla.FloatingWindow((330, 500), title, minSize=(300,500), maxSize=(1000,700))
        self.leading = 14
        self.head_count = 0

        self.w.open()
    
    def _heading(self, title):
        self.leading += 20
        setattr(self.w, 'text%s' % self.head_count, vanilla.TextBox((14, self.leading, 300, 14), title, sizeStyle='small'))
        self.leading += 12
        self.head_count += 1
        setattr(self.w, 'rule%s' % self.head_count, vanilla.HorizontalLine((14, self.leading, 300, 14)))
        self.leading += 12
    
    def _checkbox(self, attr,  title, value=True):
        setattr(self.w, attr, vanilla.CheckBox((14, self.leading, 300, 20), title, value=value))
        self.leading += 20

    def _combobox(self, attr, vals):
        setattr(self.w, attr, vanilla.PopUpButton((14, self.leading, 300, 20), vals))
        self.leading += 20

    def _from_config():
        if config_file != None:
            for key in config_file:
                self._checkbox(key, '%s' % key)
