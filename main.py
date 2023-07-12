try:
    import numpy as np
    print("numpy OK")
except:
    print("No numpy module")

try:
    import matplotlib
    print("matplotlib OK")
except:
    print("No matplotlib module")

try:
    from astropy.time import Time
    print("astropy OK")
except:
    print("No astropy module")

try:
    from astroquery.jplhorizons import Horizons
    print("astroquery OK")
except:
    print("No astroquery module")
