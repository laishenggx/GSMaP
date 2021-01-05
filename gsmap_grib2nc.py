import gzip
import numpy as np
import netCDF4 as nc
from dateutil.rrule import *
from dateutil.parser import *

lon = np.arange(0.125, (360 - 0.125) + 0.25, 0.25)
lat = np.arange(59.875, (-60 + 0.125) - 0.25, -0.25)
time_units = 'hours since 1900-01-01 00:00:00'
time_cal = 'gregorian'

for year in range(2001,2019,1):
    root='C:/pyproj/gsmap_download/p12Z-11Z/%s/'%year
    time_list = list(rrule(DAILY, dtstart=parse("%s0101"%year), until=parse('%s1231'%year)))
    file_list=[root+'gsmap_gauge.%s.0.25d.daily.p12Z-11Z.dat.gz'%t.strftime('%Y%m%d') for t in time_list]

    out=nc.Dataset('gsmap_gauge_NRT.%s.0.25d.daily.p12Z-11Z.nc'%year,mode='w',format='NETCDF4')
    out.createDimension('lons', len(lon))
    out.createDimension('lats', len(lat))
    out.createDimension('times', len(file_list))

    out.createVariable('lon', 'f', ('lons'), complevel=9)
    out.createVariable('lat', 'f', ('lats'), complevel=9)
    out.createVariable('time', 'i', ('times'), complevel=9)
    out.createVariable('pre', 'f', ('times','lats', 'lons'), complevel=9)
    out.variables['pre'].units = 'mm/day'
    out.variables['lon'][:] = lon
    out.variables['lat'][:] = lat
    out.variables['time']=nc.date2num(time_list, units=time_units, calendar=time_cal)

    data=np.zeros((len(file_list),len(lat),len(lon)))
    for i,fn in enumerate(file_list):
        print(year,i)
        gz = gzip.GzipFile(fn,'rb')
        dd=np.frombuffer(gz.read(),dtype=np.float32)
        pre = np.copy(dd.reshape((480, 1440)))
        pre*=24
        pre[np.where(pre<0)]=-999
        data[i]=pre
    out.variables['pre'][:] = data
    out.description = "GSMaP_Gauge_NRT Daily Precipitation [12:00Z(previous day)-11:59Z]"
    out.res='0.25x0.25 deg'
    out.original = "JAXA,EORC dir:/realtime_ver/v6/daily_G/p12Z-11Z/"
    out.author = "ICCES,IAP/CAS"
    out.close()
