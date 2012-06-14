
import hashlib, sys
s = "cm29sh5g9sxk24fg2.dr"
e = sys.argv[1]
h = hashlib.sha1(e+s).hexdigest()[0:8]
print e+','+h
