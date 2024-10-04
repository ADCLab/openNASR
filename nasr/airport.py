from basictypes import Raw, getRecord      
from ils import ILSBase,ILSitem,ILSDME,DMEitem,ILSGS,GSitem,ILSMKR,MKRitem
from rwy import RWY,RWYitem,RWYEnd,RWYEnditem
from matplotlib import pyplot as plt
# import wmm2020
from shapely.geometry import LineString
 

class AirportBase(Raw): 
    def __init__(self,airport,nasrDF,airportIDCol):
        super().__init__(   getRecord(airport,nasrDF,airportIDCol)  ) 

    @property    
    def elevation(self):
        return self._raw.ELEV
        
    @property    
    def icao_id(self):
        return self._raw.ICAO_ID 

    @property    
    def faa_id(self):
        return self._raw.ARPT_ID     
             

class Airport():
    def __init__(self, airport,NASR):
        isAirport, airportIDCol = NASR.isAirport(airport)
        if isAirport:
            self.base = AirportBase(airport,NASR['APT_BASE'],airportIDCol)
            # self.decl = wmm2020.wmm_point(self.lat,self.lon, self.elevation,NASR.yearDecimal)['decl']
            self.rwy = RWY(RWYitem,airport,NASR['APT_RWY'],airportIDCol,useRWYID=True)
            self.ils = ILSBase(ILSitem,airport,NASR['ILS_BASE'],airportIDCol)
            self.ils.setDecl(self.decl)
            self.dme = ILSDME(DMEitem,airport,NASR['ILS_DME'],airportIDCol)
            self.gs = ILSGS(GSitem,airport,NASR['ILS_GS'],airportIDCol)
            self.mkr = ILSMKR(MKRitem,airport,NASR['ILS_MKR'],airportIDCol)
            self.rwyend = RWYEnd(RWYEnditem,airport,NASR['APT_RWY_END'],airportIDCol)
        else:
            print("Unable to find %s"%airport)
            raise 'Airport does not exist in FAA database (as ICAO or FAA code)'  

    @property    
    def elevation(self):
        return self.base.elevation

    @property    
    def lat(self):
        return self.base.lat
    
    @property    
    def lon(self):
        return self.base.lon
        
    @property    
    def icao_id(self):
        return self.base.icao_id 

    @property    
    def faa_id(self):
        return self.base.faa_id 
    
    def plot(self):
        plt.close('all')
        self.fig, self.ax = plt.subplots()  
        self.plotRWY()
        self.ils.plot(self.ax,self.lat,self.lon)
        self.gs.plot(self.ax,self.lat,self.lon)

        plt.gca().set_aspect('equal')
        
    
    def plotRWY(self):
        for cRWY in self.rwy.ids:
            rwyEnds = cRWY.split('/')
            if len(rwyEnds)==2:
                x0,y0 = self.rwyend[rwyEnds[0]].xy(self.lat,self.lon)
                x1,y1 = self.rwyend[rwyEnds[1]].xy(self.lat,self.lon)
                xp,yp=makeRWYpoly([x0,y0],[x1,y1], width=self.rwy[cRWY].width)
                self.ax.fill(xp, yp, alpha=0.5, fc='black', edgecolor='black')
                
 
def makeRWYpoly(xy_start,xy_end,width):
    # Create a LineString from the start and end points
    line = LineString([xy_start, xy_end])
    
    # Create a buffered polygon around the line
    polygon = line.buffer(width/6076.1/2)  # Buffering by half the width
    
    return polygon.exterior.xy    
        
        # x,y=self.xy
        # axs.scatter(x,y,color='blue',marker='x')
        