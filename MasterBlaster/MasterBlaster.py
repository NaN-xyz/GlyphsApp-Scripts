#MenuTitle: MasterBlaster
# -*- coding: utf-8 -*-
__doc__="""
Display all available masters in a given text list. Define list in UI or local txt file.
"""

import vanilla
import codecs
import GlyphsApp

f = Glyphs.font
masterlen = len(f.masters)

class Master( object ):

    def __init__( self ):

        global presets

        try:
            fd = codecs.open('MasterBlaster-presets.txt','r',encoding='utf-8')
            data = fd.read()
            presets = data.split("\n")
        except:    
            # if txt file doesn't load
            presets = [
                u"arrowroot,barley,chervil,dumpling,endive,flaxseed,garbanzo,hijiki,ishtu,jicama,kale,lychee,marjioram,nectarine,oxtail,pizza,quinoa,roquefort,squash,tofu,uppuma,vanilla,wheat,xergis,yogurt,zweiback",
                u"Arrowroot,Barley,Chervil,Dumpling,Endive,Flaxseed,Garbanzo,Hijiki,Ishtu,Jicama,Kale,Lychee,Marjioram,Nectarine,Oxtail,Pizza,Quinoa,Roquefort,Squash,Tofu,Uppuma,Vanilla,Wheat,Xergis,Yogurt,Zweiback",            
                u"ARROWROOT,BARLEY,CHERVIL,DUMPLING,ENDIVE,FLAXSEED,GARBANZO,HIJIKI,ISHTU,JICAMA,KALE,LYCHEE,MARJIORAM,NECTARINE,OXTAIL,PIZZA,QUINOA,ROQUEFORT,SQUASH,TOFU,UPPUMA,VANILLA,WHEAT,XERGIS,YOGURT,ZWEIBACK",
                "00000,00100,00200,00300,00400,00500,00600,00700,00800,00900"
                ]

        wlist = ""

        windowWidth = 340
        windowHeight = 380

        self.w = vanilla.FloatingWindow(
            ( windowWidth, windowHeight ), # default window size
            "MasterBlaster", # window title
            autosaveName = "com.LNP.MasterBlaster.mainwindow" # stores last window position and size
        )


        self.w.titleCustom = vanilla.TextBox((20, 15, -10, 17), "Comma separated list:")
        self.w.inputCustom = vanilla.EditText( (20, 45, 300, 20), "", sizeStyle = 'small')
        self.w.titlePreset = vanilla.TextBox((20, 75, -10, 17), "OR Select preset from local txt file:")
        self.w.presets = vanilla.List((20, 105, 305, 180), presets, doubleClickCallback=self.GoDblC, autohidesScrollers = False, allowsEmptySelection = True, showColumnTitles=True)
        self.w.radioGroup = vanilla.RadioGroup((20, 285, 250, 40),["Stacked", "Side-by-side"],isVertical = False, sizeStyle='regular')
        self.w.runButton = vanilla.Button((20, 330, 120, 30), "List as Masters", sizeStyle='regular', callback=self.GoButton )

        self.w.radioGroup.set(1)

        # Load Settings:
        if not self.LoadP():
            print "Could not load preferences. Will resort to defaults"

        self.w.open()
        self.w.makeKey()

    def SaveP( self, sender ):
        try:
            Glyphs.defaults["com.LNP.MasterBlaster.inputCustom"] = self.w.inputCustom.get()
            Glyphs.defaults["com.LNP.MasterBlaster.radioGroup"] = self.w.radioGroup.get()
        except:
            return False
        return True

    def LoadP( self ):
        try:
            self.w.inputCustom.set( Glyphs.defaults["com.LNP.MasterBlaster.inputCustom"] )
            self.w.radioGroup.set( Glyphs.defaults["com.LNP.MasterBlaster.radioGroup"] )
        except:
            return False
        return True

    def Sanitise( self, wordlist):

        santised_list = list()        

        for w in wordlist:

            tmp_entry = ""

            for l in w:
                if f.glyphs[l]: 
                    tmp_entry = tmp_entry + l

            if tmp_entry!="": santised_list.append(tmp_entry)

        return santised_list

    def Blaster( self, wordlist ):

        layout = self.w.radioGroup.get() # 0=stacked 1=sidebyside
        wordlist = self.Sanitise(wordlist)

        repeater = ""
        wlist = ""

        for w in wordlist:

            s=0
            while s<masterlen: 
                if layout==1:
                    repeater = repeater + w + " "  
                else:
                    repeater = repeater + w + "\n"  
                s=s+1
            
            wlist = wlist + repeater + "\n"
            repeater = ""

        Glyphs.currentDocument.windowController().addTabWithString_( wlist ) # add text
        currentEditViewController = Glyphs.currentDocument.windowController().activeEditViewController()
        currentTab = currentEditViewController.graphicView()

        s=0
        location_start = 0
        listlen = len(wordlist)

        while s<listlen:

            myRangeOfGlyphs = NSRange()
            t=0

            while t<masterlen: 

                myRangeOfGlyphs.location = location_start
                myRangeOfGlyphs.length = len(wordlist[s])

                # assign master value to range
                masterID = f.masters[t].id
                Attributes = { "GSLayerIdAttrib": masterID }
                currentTab.textStorage().text().addAttributes_range_( Attributes, myRangeOfGlyphs )

                location_start = location_start + len(wordlist[s]) + 1
                t+=1

            location_start+=1
            s=s+1

        if not self.SaveP( self ):
            print "Could not save preferences." 

        currentEditViewController.forceRedraw()

    def GoDblC( self, sender ):

        preset_selections = self.w.presets.getSelection()
        for p in preset_selections: preselect = presets[p] 
        self.Blaster(preselect.split(","))

    def GoButton( self, sender ):

        customT = self.w.inputCustom.get()
        preset_selections = self.w.presets.getSelection()

        # force permit one selection for now
        for p in preset_selections: preselect = presets[p] 

        if customT != "":
            self.Blaster(customT.split(","))
        else:
            self.Blaster(preselect.split(","))

Master()
