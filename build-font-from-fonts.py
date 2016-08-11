#MenuTitle: Combine all open fonts into selected font
'''
Combine all open single weigth fonts into the selected font.

'''
def main():
    fonts = Glyphs.fonts
    new_font = fonts[0]
    source_fonts = list(fonts)[1:]
    
    # Prep source instance first
    new_font.instances[0].weightValue = new_font.masters[0].weightValue
    # Add master custom parameters to instance
    for key in new_font.masters[0].customParameters:
        new_font.instances[0].customParameters[key.name] = new_font.masters[0].customParameters[key.name]

    if new_font.customParameters['panose']:
        new_font.instances[0].customParameters['panose'] = new_font.customParameters['panose']

    for i, font in enumerate(source_fonts):    
        # append master to font
        new_font.masters[font.masters[0].id] = font.masters[0]
        layer_id = new_font.masters[font.masters[0].id].id

        # Add glyphs to master
        for glyph in font.glyphs:
            glyf = font.glyphs[glyph.name].layers[0]
            if new_font.glyphs[glyph.name]:
                new_font.glyphs[glyph.name].layers[layer_id] = glyf

        # Add instances and set values correctly
        if font.instances[0] not in new_font.instances:
            new_font.instances.append(font.instances[0])

            # Set weight of instance to masters weight
            new_font.instances[-1].weightValue = font.masters[0].weightValue
            if font.customParameters['panose']:
                new_font.instances[-1].customParameters['panose'] = font.customParameters['panose']
            for key in font.masters[0].customParameters:
                new_font.instances[-1].customParameters[key.name] = font.masters[0].customParameters[key.name]

    print 'done'

if __name__ == '__main__':
    main()
