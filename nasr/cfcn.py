from numpy import radians, cos, sin, median, radians, sqrt, percentile, float64, array, matmul, generic, ndarray
import time


def ll2xy(lats,lons, latc=None, lonc=None, llc=None):
    # See https://en.wikipedia.org/wiki/Earth_radius#Equatorial_radius
    lats=radians(lats)
    lons=radians(lons)      
    if llc is not None:
        latc=radians(llc[0])
        lonc=radians(llc[1])
    elif latc is not None and lonc is not None and llc is None:
        latc=radians(latc)
        lonc=radians(lonc)
    else:
        latc=median(lats)
        lonc=median(lons)
        
        
    eqRad=3443.91847352  # Radius [NM] at the equator
    eqPol=3432.37169102   # Radius [NM] at the polar 
    eqNum = (eqRad*eqRad*cos(latc))**2+(eqPol*eqPol*sin(latc))**2
    eqDon = (eqRad*cos(latc))**2+(eqPol*sin(latc))**2
    earthRad=sqrt(eqNum/eqDon)
    
    cosc=sin(latc)*sin(lats)+cos(latc)*cos(lats)*cos(lons-lonc)
    
    x=earthRad*( cos(lats)*sin(lons-lonc) ) / cosc
    y=earthRad*( cos(latc)*sin(lats)-sin(latc)*cos(lats)*cos(lons-lonc) ) /cosc
    dist=sqrt(x**2+y**2)

    return x,y,array([latc,lonc]),dist
    