from nasr.nasr import NASR
from time import time
from trino.dbapi import connect
from trino.auth import OAuth2Authentication
from shapely.geometry import Point
from numpy import nan

myNASR=NASR()
ztl_boundary=myNASR.artcc.ZTL.high.lonlat
ztl_bbox=myNASR.artcc.ZTL.high.bbox
ZTL_polygon=myNASR.artcc.ZTL.high.getShape


from nasr.airport import Airport
myAirport = Airport('DCA',myNASR)
# myAirport.rwy('01')
myAirport.ils_raw('01')

conn = connect(
    host="trino.opensky-network.org",
    port=443,
    user="aevela",
    catalog="minio",
    schema="osky",
    http_scheme='https',
    auth=OAuth2Authentication()
)
cur = conn.cursor()

# startTime=1717200000
# endTime=startTime+30*24*60*60

startTime=1718388000
endTime = 1719792000
cTime=startTime

kCols='time,icao24,lon,lat,velocity,heading,vertrate,callsign,baroaltitude,geoaltitude'
while cTime<endTime:
    with open('ZTL/%s_%i.csv'%('ZTL',cTime),'w') as fout:
        fout.write('%s\n'%kCols)
        myQRY_p1='SELECT %s FROM minio.osky.state_vectors_data4'%kCols
        myQRY_p2='WHERE lon>=%f and lat>=%f and lon<=%f and lat<=%f'%ztl_bbox
        myQRY_p3='AND HOUR=%i'%cTime
        myQRY=' '.join([myQRY_p1,myQRY_p2,myQRY_p3])

        cur.execute(myQRY)
        while True:
            cRow = cur.fetchone()
            if cRow is None:
                break
            elif ZTL_polygon.contains(Point(cRow[2],cRow[3])):
                cRow = [nan if x is None else x for x in cRow]
                fout.write('%i,%s,%f,%f,%f,%f,%f,%s,%f,%f\n'%tuple(cRow))
    cTime=cTime+60*60
conn.close()


