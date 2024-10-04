from types import SimpleNamespace
from basictypes import Point      

      
class Fix(Point):
    def __init__(self, fix,NASR):
        if NASR.isFix(fix):    
            self._addBASE(fix,NASR['FIX_BASE'])
        else:
            print("Unable to find %s"%fix)
            raise 'Fix does not exist in FAA database'    
        
    def _addBASE(self,fix,FIX_BASE):
        self.base = SimpleNamespace( **FIX_BASE[FIX_BASE['FIX_ID']==fix].to_dict(orient='records')[0] )
    
        