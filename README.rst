=====
Marc Foley Glyphsapp Scripts
=====

Description:
-----
Repo of Marc's scripts for GlyphsApp.

Installation:
-----
Drop the scripts in your GlyphsApp script folder.
/Users/user/Library/Application Support/Glyphs/Scripts

Usage:
____
Use on .glyphs source files only. Reports will save to the same directory as the source file. No need for Vanilla ;)

FAQ:
-----
***My accented glyphs are not attaching to the base glyphs?***
- You may have placed anchors on diacritic glyphs which are not in the 'Combining Diacritical Marks'. You may have anchors on acute when they should be on acutecomb. Combining Diacritical Marks reside in the unicode range U+0300 to U+036F. 
- Some shaping engines do not support certain combinations.

***Why am I getting crap kerning strings for Hebrew, Arabic, Devanagari...
- Scripts only support Latin, Greek and Cyrillic at the moment.

Version History:
-----
***V0.001***
- Report/proof anchors and kerning for non-Latin scripts only.