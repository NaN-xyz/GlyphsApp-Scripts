# GlyphsApp Scripts

Mischief.

## Angularizzle.py

Takes lovingly crafted glyphs and disfigures their curves by sharp line. Visually it has something akin to Illustrator's "Simplify" but is more nuanced (imvfho). The 'Keep detail' option attempts to protect the form's integrity. Unselected it's allowed to devolve down to brutish polygon. Only works with cubic curves so if you import TTFs be sure to convert.

Can be used on a glyph-by-glyph basis or across the entire selected font.

## MasterBlaster.py

The script takes a comma separated list from input or local txt file and displays each entry in all available masters. If the local file fails to load presets can also be set within the script itself.

Dummy presets are defined in MasterBlaster-presets.txt. You’ll want to edit according to your needs. Each line represents one list and like UI input must be comma separated. 

At the moment it doesn’t handle GlyphsApp glyph names and the Vanilla List of presets remains abridged till I find a fix. Tested in Glyphs 2.4.2 OS X 10.10.5.

Please report all bugs, comments and feature requests via GitHub.

## CommonGlyphs.py

Prints glyphs common to all open fonts to the macro window by unicode, Glyphs NiceNames and ProductionNames. Edit the variable below and common glyphs across all open fonts will have a charcoal colour label.

'''
SetGlyphColour=True
'''

## License

Copyright 2019 [Luke Prowse](http://twitter.com/luke_prowse). Licensed under the Apache License, Version 2.0 (the "License"); you may not use the software provided here except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
