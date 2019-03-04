#MenuTitle: Angularizzle
# -*- coding: utf-8 -*-
__doc__="""
Creates angular versions of glyphs made up of cubic paths.
"""
import math
import vanilla
import copy
import GlyphsApp

f = Glyphs.font
masterlen = len(f.masters)

# Script name by Type Overlord Florian Horatio Runge of Flensborre @FlorianRunge

class Angela( object ):

    def __init__( self ):

        windowWidth = 222
        windowHeight = 130

        self.w = vanilla.FloatingWindow(
            ( windowWidth, windowHeight ), 
            "Angularizzle Yo", 
            autosaveName = "com.LNP.Angela.mainwindow" 
        )
        
        self.w.titlesize = vanilla.TextBox((20, 20, -10, 17), "Min plane:")
        self.w.inputSize = vanilla.EditText( (100, 20, 100, 20), "80", sizeStyle = 'small') 
        self.w.checkBox = vanilla.CheckBox((20, 50, -10, 17), "Keep detail", value=True)
        self.w.cancelButton = vanilla.Button((20, 80, 85, 30), "Cancel", sizeStyle='regular', callback=self.CloseApp )
        self.w.runButton = vanilla.Button((120, 80, 85, 30), "Process", sizeStyle='regular', callback=self.DoIt )
        self.w.setDefaultButton (self.w.runButton)
        
        # Load Settings: Save/Load settings by Toschi Omagari 
        if not self.LoadP():
            pass
            #print "Could not load preferences. Will resort to defaults"

        self.w.open()
        self.w.makeKey()

        global font
        font = Glyphs.font
        global selectedGlyphs
        selectedGlyphs = [ l.parent for l in font.selectedLayers ]
        
        # if single glyph save state
        if len(selectedGlyphs)==1:
            thisgl = font.selectedLayers[0]
            global GlyphStartPaths
            GlyphStartPaths = copy.deepcopy(thisgl.paths)

    def CloseApp(self, sender):
        thisgl = font.selectedLayers[0]
        self.ClearScreen(thisgl)
        for p in GlyphStartPaths: thisgl.paths.append(p)
        self.w.close()

    def SaveP( self, sender ):
        try:
            Glyphs.defaults["com.LNP.Angela.inputSize"] = self.w.inputSize.get()
            Glyphs.defaults["com.LNP.Angela.checkBox"] = self.w.checkbox.get()
        except:
            return False
        return True

    def LoadP( self ):
        try:
            self.w.inputSize.set( Glyphs.defaults["com.LNP.Angela.inputSize"] )
            self.w.checkbox.set( Glyphs.defaults["com.LNP.Angela.checkbox"] )
        except:
            return False
        return True

    def MainAngela( self, asize, detail ):

        if asize.isdigit()==True:

            global stepnum, tStepSize
            asize = int(asize)
            stepnum=130
            tStepSize = 1.0/stepnum # !impt
            font = Glyphs.font
            angsize = int(asize)
            font.disableUpdateInterface()

            for glyph in selectedGlyphs:

                thisgl = font.glyphs[glyph.name].layers[0]
                if thisgl.paths==0:
                    continue
                thisgl.color = 8 #purple

                if len(selectedGlyphs)>1:
                    ang = self.ReturnNodesAlongPath(thisgl.paths, angsize)
                else:
                    ang = self.ReturnNodesAlongPath(GlyphStartPaths, angsize)
                    
                if detail==False:
                    ang = self.StripDetail(ang, asize)

                if ang:

                    #thisgl = font.selectedLayers[0]
                    self.ClearScreen(thisgl)

                    for n in ang:
                        pts = n[2]
                        isclosed = n[1]
                        outline = self.ListToPath(pts, isclosed)
                        thisgl.paths.append( outline )

            font.enableUpdateInterface()

            if not self.SaveP( self ):
                pass
                #print "Could not save preferences." 

            if len(selectedGlyphs)>1:
                self.w.close()

    def StripDetail (self, nlist, asize):

        newList = list()

        for s in nlist:

            newnodes = list()
            length = s[0]
            isclosed = s[1]
            nlist = s[2]
            p1x = nlist[0][0]
            p1y = nlist[0][1]

            for n in range(1, len(nlist)-1):

                p2x = nlist[n][0]
                p2y = nlist[n][1]
                dist = math.hypot(p2x - p1x, p2y - p1y)

                if dist > asize:
                    newnodes.append([p1x, p1y])
                    p1x = p2x
                    p1y = p2y
                else: 
                    continue

            nl = [length, isclosed, newnodes]
            newList.append(nl)

        return newList

    def DoIt( self, sender ):
        asize = self.w.inputSize.get()
        detail = self.w.checkBox.get()
        if int(asize) > 4:
            self.MainAngela(asize, detail)
        else:
            pass

    # Remove any duplicate points from list
    def RemoveDuplicatePts(self, ptlist):
        ptl = []
        for i in ptlist:
            if i not in ptl:
                ptl.append(i)

        ptl.append(ptlist[-1])
        return ptl

    # the main return t postion on curve script p0,1,2,3 is segment
    def GetPoint(self, p0, p1, p2, p3, t):

        ax = self.lerp( [p0[0], p1[0]], t )
        ay = self.lerp( [p0[1], p1[1]], t )
        bx = self.lerp( [p1[0], p2[0]], t )
        by = self.lerp( [p1[1], p2[1]], t )
        cx = self.lerp( [p2[0], p3[0]], t )
        cy = self.lerp( [p2[1], p3[1]], t )
        dx = self.lerp( [ax, bx], t )
        dy = self.lerp( [ay, by], t )
        ex = self.lerp( [bx, cx], t )
        ey = self.lerp( [by, cy], t )

        pointx = self.lerp( [dx, ex], t )
        pointy = self.lerp( [dy, ey], t )

        calc = [pointx,pointy]
        return calc

    # Put all the xy coords of linear t GetPoint() increments in list 
    def CreatePointList(self,p0,p1,p2,p3):
        pl = list() 
        tmp=0
        while tmp<1:
            t = tmp
            calc = self.GetPoint(p0,p1,p2,p3,tmp)
            pl.append(calc)
            tmp = tmp + tStepSize
        return pl

    #Clear layer except components
    def ClearScreen(self, clearlayer):
        for i in range( len( clearlayer.paths ))[::-1]:
            del clearlayer.paths[i]

    def lerp(self, v, d):
        return v[0] * (1 - d) + v[1] * d

    # create distance look up list from pointlist so we can determine a % position along spine
    # each item represents cumulative distances from beginning of segments
    def CreateDistList(self, pointlist):

        lookup = list()
        totallength = 0

        for tp in range (0,len(pointlist)-1):
            p1x = pointlist[tp][0]
            p1y = pointlist[tp][1]
            p2x = pointlist[tp+1][0]
            p2y = pointlist[tp+1][1]
            dist = math.hypot(p2x - p1x, p2y - p1y)
            totallength += dist
            lookup.append(totallength)
            
        lookup.insert(0,0)

        return lookup

    #find at which index the desired length matches to determine nearest t step value
    #return new precise t value between the two indexes desiredlen falls
    def FindPosInDistList(self, lookup, newlen): #newlen = length along curve

        for s in range (0,len(lookup)-1):

            b1 = lookup[s]
            b2 = lookup[s+1]

            if b1 <= newlen <= b2:
                if b1==0:
                    newt=0
                else:
                    percentb = ( 100 / (b2 - b1) ) * (newlen - b1)
                    newt = (s*tStepSize) + ( tStepSize * (percentb/100) )
                return (newt)

    # Draw new angular path from list
    def ListToPath(self, ptlist, isopen):
        np = GSPath()
        if isopen == True and len(ptlist)>2: del ptlist[-1] 
        if len(ptlist)>2: #so counters don't devolve completely
            for pt in ptlist:
                newnode = GSNode()
                newnode.type = GSLINE
                newnode.position = (pt[0], pt[1])
                np.nodes.append( newnode )
            np.closed = isopen
        return np

    def PointToPointSteps(self, tp0, tp1, spacebetween):

        n1x, n1y, n2x, n2y = tp0[0], tp0[1], tp1[0], tp1[1]
        tmplist = list()

        dist = math.hypot(n2x - n1x, n2y - n1y)

        currentx = n1x
        currenty = n1y

        psteps = int(math.ceil(dist/spacebetween))

        stepx = (n2x-n1x) / psteps
        stepy = (n2y-n1y) / psteps

        for n in range(psteps):

            tmplist.append([currentx, currenty])
            currentx+=stepx
            currenty+=stepy

        return tmplist

    # returns nodes along a curve at intervals of space between
    def ReturnNodesAlongPath(self, GlyphStartPaths, spacebetween):

        allPaths = list()

        for path in GlyphStartPaths:

            pathTotalLength = 0
            allpointslist = []
            scount=0
            
            if path.closed==False:
                continue

            for segment in path.segments:
                
                nodenum = len(segment)
                scount+=1

                if segment.type=="move":
                    continue

                # if straight segment 
                if nodenum==2:

                    if scount<1: continue
                    tp0 = (segment[0].x, segment[0].y)
                    tp1 = (segment[1].x, segment[1].y)
                    dist = math.hypot(tp1[0] - tp0[0], tp1[1] - tp0[1])
                    pathTotalLength+=dist
                    straightlinepts = self.PointToPointSteps(tp0,tp1,spacebetween)
                    for sl in straightlinepts: allpointslist.append(sl)

                # if bezier curve segment
                if nodenum==4:

                    tp0 = (segment[0].x, segment[0].y)
                    tp1 = (segment[1].x, segment[1].y)
                    tp2 = (segment[2].x, segment[2].y)
                    tp3 = (segment[3].x, segment[3].y)

                    pointlist = self.CreatePointList(tp0, tp1, tp2, tp3) 
                    lookup = self.CreateDistList(pointlist) 
                    totallength = lookup[-1] 
                    pathTotalLength += totallength

                    # check that the distance of curve segment is at least as big as spacebetween jump
                    if totallength > spacebetween:
                        steps = 20
                        stepinc = totallength / steps
                        steps = int(math.floor(totallength/spacebetween))
                        stepinc = totallength / steps
                        dlen=0 # distance to check in list of distances

                        for s in range(0,steps+1):

                            if s==0:
                                newt=0
                            elif s==steps:
                                newt=1
                            else:
                                newt = self.FindPosInDistList(lookup,dlen)
                            
                            calc = self.GetPoint(tp0,tp1,tp2,tp3,newt)
                            allpointslist.append(calc)
                            dlen+=stepinc
                    else:
                        allpointslist.append([tp0[0],tp0[1]])
                        allpointslist.append([tp3[0],tp3[1]])

            if allpointslist:
                allpointslist = self.RemoveDuplicatePts(allpointslist)
                pathdata = [pathTotalLength, path.closed, allpointslist]
                allPaths.append(pathdata) 

        return allPaths

Angela()