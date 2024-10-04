from basictypes import Raw, RawDict   
from cfcn import ll2xy   
from math import pi, cos, sin

class ILSitem(Raw):
    def category(self):
        if hasattr(self._raw,'CATEGORY'):
            return self._raw.CATEGORY
        else:
            return None

    @property            
    def trueBearing(self):
        magBearing=self.magBearing
        # magVar=self.decl
        magVar=-self.magVar

        if (magBearing is not None) and (magVar is not None):
            return magBearing+magVar
        else:
            return None

    @property            
    def trueAngle(self):
        return 90-self.trueBearing

    @property            
    def magBearing(self):
        if hasattr(self._raw,'APCH_BEAR'):
            return self._raw.APCH_BEAR
        else:
            return None

    @property            
    def magVar(self):
        if hasattr(self._raw,'MAG_VAR'):
            return self._raw.MAG_VAR
        else:
            return None
        
    def plot(self,ax,latc,lonc,rwyTrueAngle=None):
        x0,y0=self.xy(latc,lonc)
        ax.scatter(x0,y0,color='blue',marker='h')
        
        ang = self.trueAngle
        dx=-cos(ang*pi/180)
        dy=-sin(ang*pi/180)    
        ax.quiver(x0,y0, dx, dy, scale=5,color='red')
    

      

class ILSBase(RawDict):
    def plot(self,ax,lonc,latc):
        for cID in self.ids:
            self[cID].plot(ax,lonc,latc)
            
    def setDecl(self,decl):
        for cID in self.ids:
            self[cID].decl=decl
            
# --------------------------------------- 
# --------------------------------------- 
class DMEitem(Raw):
    pass
     
class ILSDME(RawDict): 
    pass
# --------------------------------------- 
# --------------------------------------- 
class GSitem(Raw):
    @property            
    def angle(self,id):
        if hasattr(self[id]._raw,'G_S_ANGLE'):
            return self[id]._raw.G_S_ANGLE
        else:
            return None

    def plot(self,ax,latc,lonc,rwyTrueAngle=None):
        x0,y0=self.xy(latc,lonc)
        ax.scatter(x0,y0,color='blue',marker='x')
        
        # ang = self.trueAngle
        # dx=-cos(ang*pi/180)
        # dy=-sin(ang*pi/180)    
        # ax.quiver(x0,y0, dx, dy, scale=4,color='red')

class ILSGS(RawDict):
    def plot(self,ax,lonc,latc):
        for cID in self.ids:
            self[cID].plot(ax,lonc,latc)

# --------------------------------------- 
# --------------------------------------- 
class MKRitem(Raw):
    pass

class ILSMKR(RawDict): 
    pass