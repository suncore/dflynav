
import hashlib, sys
s = "cm29sh5g9sxk24fg2.dr"
e = sys.argv[1]
version="1.0"
h = hashlib.sha1(e+version+s).hexdigest()[0:8]
print e+','+version+','+h
