from basictypes import Raw, RawDict      
# --------------------------------------- 
# --------------------------------------- 
class RWYEnditem(Raw):
    @property            
    def bearing(self,id):
        if hasattr(self._raw,'TRUE_ALIGNMENT'):
            return self._raw.TRUE_ALIGNMENT
        else:
            return None   

    @property            
    def glidepath(self,id):
        if hasattr(self._raw,'VISUAL_GLIDE_PATH_ANGLE'):
            return self._raw.VISUAL_GLIDE_PATH_ANGLE
        else:
            return None   
        

class RWYEnd(RawDict): 
    pass

# --------------------------------------- 
# --------------------------------------- 

class RWYitem(Raw):
    @property
    def rwyType(self):
        return self._raw.SITE_TYPE_CODE

    def trueBearing(self):
        return self._raw.TRUE_ALIGNMENT

    def trueAngle(self):
        return 90-self._raw.TRUE_ALIGNMENT
    
class RWY(RawDict): 
    pass
    # def __init__(self,airport,nasrDF,airportIDCol):
    #     super().__init__(airport,nasrDF,airportIDCol, useRWYID=True)
    #     self._map_ends=dict()
    #     for cRWYinfo in [(idx,cRec.RWY_ID.split('/')) for idx,cRec in enumerate(self._raw)]:
    #         for cRWY in cRWYinfo[1]:
    #             self._map_ends[cRWY]=cRWYinfo[0]