#MenuTitle: Print Common Glyphs
# -*- coding: utf-8 -*-
__doc__="""
Prints glyphs common to all open fonts to the macro panel.
"""

# Change to True and common glyph label color is set to charcoal
SetGlyphColour=False	

Glyphs.showMacroWindow()
Glyphs.clearLog()

allfonts = Glyphs.fonts
allglyphs = list()
ofonts=[]

if len(allfonts) > 0: 

	for f in allfonts:
		niceglyphs = []
		ofonts.append(f.familyName)
		for g in f.glyphs: 
			niceglyphs.append(g.name) # see g.string and g.unicode
		allglyphs.append(niceglyphs)

	allglyphs.sort() 
	temp = allglyphs[0]
	for f in range(1,len(allglyphs)): temp = set(temp).intersection(allglyphs[f])

	print "Analysed fonts: " + ", ".join(ofonts)
	print "Number of common glyphs: " + str(len(temp)) + "\n"
	
	nice, prod, simp = "", "", ""
	string =""

	for p in temp: 
		nice+=p+" "
		prod+=Glyphs.productionGlyphName(p)+" "
		string = Glyphs.fonts[0].glyphs[p].string
		if string:
			string.encode('unicode_escape')
			simp+=string+" "

	print simp
	print "\n"
	print "Nice names: \n" + nice
	print "\n"
	print "Production names: \n" + prod
	print "\n"

	if SetGlyphColour==True:
		for f in allfonts:
			for p in temp:
				f.glyphs[p].color = 11
			



else:
	print "Insufficient number of fonts open to compare."
