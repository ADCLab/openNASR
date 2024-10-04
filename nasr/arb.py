from shapely.geometry import Polygon


class Boundary():
    def __init__(self, lons = None, lats = None):
        self.__boundary = Polygon(  [(lon,lat) for lon,lat in zip(lons,lats)]   )
        
    @property
    def lat(self):
        return self.__boundary.exterior.coords.xy[1].tolist()

    @property
    def lon(self):
        return self.__boundary.exterior.coords.xy[0].tolist()        

    @property
    def latlon(self):
        return [(lat,lon) for lat, lon in zip(self.lat,self.lon)]

    @property
    def lonlat(self):
        return [(lon,lat) for lat, lon in zip(self.lat,self.lon)]

    @property
    def getShape(self):
        return self.__boundary
    
    @property
    def bbox(self):
        return min(self.lon),min(self.lat),max(self.lon),max(self.lat)

class ARTCC():
    def __init__(self, id, name, centerType, city, state, country, lat, lon):
        self.id = id
        self.name = name
        self.centerType = centerType
        self.city = city
        self.state = state
        self.country = country
        self.lat = lat
        self.lon = lon
        
    def addboundary(self,boundaryType,altitude,lons,lats):
        setattr(  self, altitude.lower(), Boundary(lons,lats)  )
        
    @property
    def boundaryTypes(self):
        return list(self.boundary.keys())
    

    
class ARB():
    def __init__(self, arb_base,arb_seg,arbType):
        self.centers=set()
       
        for index, row in arb_seg[['LOCATION_ID','ALTITUDE','TYPE']].drop_duplicates().iterrows():
            cLocID=row['LOCATION_ID']
            cLocAlt=row['ALTITUDE']
            cLocType=row['TYPE']

            if row['TYPE']==arbType:
                tmpARB_BASE=arb_base[(arb_base['LOCATION_TYPE']==cLocType) & (arb_base['LOCATION_ID']==cLocID)].iloc[0]
                if cLocID not in dir(self):
                    setattr(  self, tmpARB_BASE['LOCATION_ID'], 
                            ARTCC(id=tmpARB_BASE['LOCATION_ID'],
                                  name=tmpARB_BASE['LOCATION_NAME'],
                                  centerType=tmpARB_BASE['LOCATION_TYPE'],
                                  city=tmpARB_BASE['CITY'],
                                  state=tmpARB_BASE['STATE'],
                                  country=tmpARB_BASE['COUNTRY_CODE'],
                                  lat=tmpARB_BASE['LAT_DECIMAL'],
                                  lon=tmpARB_BASE['LONG_DECIMAL'])  )
                    self.centers.add(  tmpARB_BASE['LOCATION_ID']  )                
                
                tmpDF = arb_seg[(arb_seg['LOCATION_ID']==row['LOCATION_ID']) & (arb_seg['ALTITUDE']==row['ALTITUDE']) & (arb_seg['TYPE']==row['TYPE'])  ]
                cARTCC=getattr(  self, row['LOCATION_ID'])
                cARTCC.addboundary(row['TYPE'], row['ALTITUDE'],tmpDF['LONG_DECIMAL'],tmpDF['LAT_DECIMAL'])