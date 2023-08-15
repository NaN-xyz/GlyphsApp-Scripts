#MenuTitle: MasterBlaster
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__="""
Display all available masters in a given text list. Define list in UI or local txt file.
"""

from Foundation import NSRange
import vanilla, codecs, GlyphsApp

class Master(object):

    def __init__(self):

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
            (windowWidth, windowHeight), # default window size
            "MasterBlaster", # window title
            autosaveName = "com.LNP.MasterBlaster.mainwindow" # stores last window position and size
        )


        self.w.titleCustom = vanilla.TextBox((20, 15, -10, 17), "Comma separated list:")
        self.w.inputCustom = vanilla.EditText((20, 45, 300, 20), "", sizeStyle='small')
        self.w.titlePreset = vanilla.TextBox((20, 75, -10, 17), "OR Select preset from local txt file:")
        self.w.presets = vanilla.List((20, 105, 305, 180), presets, doubleClickCallback=self.GoDblC, autohidesScrollers=False, allowsEmptySelection=True, showColumnTitles=True)
        self.w.radioGroup = vanilla.RadioGroup((20, 285, 250, 40), ["Stacked", "Side-by-side"], isVertical=False)
        self.w.runButton = vanilla.Button((20, 330, 120, 30), "List as Masters", callback=self.GoButton)

        self.w.radioGroup.set(1)

        # Load Settings:
        if not self.LoadP():
            print("Could not load preferences. Will resort to defaults")

        self.w.open()
        self.w.makeKey()

    def SaveP(self, sender):
        try:
            Glyphs.defaults["com.LNP.MasterBlaster.inputCustom"] = self.w.inputCustom.get()
            Glyphs.defaults["com.LNP.MasterBlaster.radioGroup"] = self.w.radioGroup.get()
        except:
            return False
        return True

    def LoadP(self):
        try:
            self.w.inputCustom.set(Glyphs.defaults["com.LNP.MasterBlaster.inputCustom"])
            self.w.radioGroup.set(Glyphs.defaults["com.LNP.MasterBlaster.radioGroup"])
        except:
            return False
        return True

    def layersForWords(self, word, masterId):
        layers = []
        for c in word:
            g = self.font.glyphForCharacter_(ord(c))
            if g:
                l = g.layers[masterId]
                if l:
                    layers.append(l)
        return layers
    
    def Blaster(self, wordlist):
        layout = self.w.radioGroup.get() # 0=stacked 1=sidebyside
        layer_list = []
        for w in wordlist:
            for m in self.font.masters:
                masterID = m.id
                layers = self.layersForWords(w, masterID)
                if len(layers) == 0:
                    break
                layer_list.extend(layers)
                if layout == 1:
                    layer_list.extend(self.layersForWords(" ", masterID))
                else:
                    layer_list.append(GSControlLayer.newline())
            layer_list.append(GSControlLayer.newline())

        self.font.newTab(layer_list)

        if not self.SaveP(self):
            print("Could not save preferences.")

    def GoDblC(self, sender):

        preset_selections = self.w.presets.getSelection()
        for p in preset_selections: preselect = presets[p]
        self.Blaster(preselect.split(","))

    def GoButton(self, sender):
        self.font = Glyphs.font
        customT = self.w.inputCustom.get()
        preset_selections = self.w.presets.getSelection()

        # force permit one selection for now
        for p in preset_selections: preselect = presets[p]

        if customT != "":
            self.Blaster(customT.split(","))
        else:
            self.Blaster(preselect.split(","))

Master()
