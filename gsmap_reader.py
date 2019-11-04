import gzip
import numpy as np

root='C:\\pyproj\\gsmap_download\\'
filename1=root+'2001\\gsmap_gauge.20010101.1400.dat.gz'

gz = gzip.GzipFile(filename1,'rb')
dd=np.frombuffer(gz.read(),dtype=np.float32)
print(dd[:100])

