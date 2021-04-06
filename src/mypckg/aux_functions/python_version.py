import sys

VERSION = None
if sys.version_info.major == 2:
    VERSION = 2
elif sys.version_info.major == 3:
    VERSION =3
