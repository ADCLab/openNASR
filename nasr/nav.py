from types import SimpleNamespace
from basictypes import Point      

class Nav(Point):
    def __init__(self, nav,NASR):
        if NASR.isNav(nav):    
            self._addBASE(nav,NASR['NAV_BASE'])
        else:
            print("Unable to find %s"%nav)
            raise 'Navaid does not exist in FAA database'    
        
    def _addBASE(self,nav,NAV_BASE):
        self.base = SimpleNamespace( **NAV_BASE[NAV_BASE['NAV_ID']==nav].to_dict(orient='records')[0] )
    
    # @property    
    # def lat(self):
    #     return self.base.LAT_DECIMAL

    # @property    
    # def lon(self):
    #     return self.base.LONG_DECIMAL
        