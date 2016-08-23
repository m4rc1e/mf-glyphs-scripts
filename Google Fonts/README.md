# Scripts for Google Fonts project

## test_gf_spec.py
Check if fonts pass [gf-checklist.md](https://github.com/googlefonts/gf-docs/blob/master/ProjectChecklist.md)


## test_kalapi_metrics.py
Check if fonts pass [Kalapis proposed vertical metrics setup](https://groups.google.com/d/msg/googlefonts-discuss/W4PHxnLk3JY/KoMyM2CfAwAJ)

    1. OS/2 sTypoAscender: highest extent of capital 'H' or lowercase ascender 'h', whichever is taller
    2. OS/2 sTypoDescender: Font UPM - OS/2 sTypoAscender
    3. OS/2 sTypoLineGap: 250 (to compensate for the 125% legacy)

    4. OS/2 usWinAscent: == yMax (head table)
    5. OS/2 usWinDescent: == yMin (head table)

    6. hhea ascent: == OS/2 sTypoAscender
    7. hhea descent: == OS/2 sTypoDescender
    8. hhea linegap: == OS/2 sTypoLineGap

This scheme should be adopted for new fonts.


## test_khaled_metrics.py
Check if fonts pass [Khaled's proposed vertical metrics setup](

    1. Set OS/2 Typo and hhea metrics to the values that gives the desired 
       line spacing for *non Vietnamese text*. 
    2. Set OS/2 fSelection “USE_TYPO_METRICS” bit. 
    3. Set OS/2 Win metrics to big enough value to avoid any clipping. 

    4. hhea ascent: == OS/2 sTypoAscender
    5. hhea descent: == OS/2 sTypoDescender
    6. hhea linegap: == OS/2 sTypoLineGap == 0

    Then test the font with this setup and see if there are any problems 
    with any of the major browsers. )


## test_125_rule.py
Check vertical metrics are greater than 125% of fonts upm. This was the legacy vertical metrics setup.