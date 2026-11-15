"""Build data/mola.json (real NASA MOLA elevation for the map region).

Uses the MOLA 4 pixel/degree topography map, ONE file of about 2 MB (1440 x 720 pixels,
16-bit big-endian metres), averaged down to a 0.5 degree whole-planet grid (about 1.3 MB output). Only needs numpy:  pip install numpy
Run from this folder:  python prepare_data.py

If the automatic download fails (NASA may move files), download megt90n000cb.img by hand from
https://pds-geosciences.wustl.edu/missions/mgs/megdr.html  (MEG004 directory, topography)
and save it as  data/megt90n000cb.img , then run this script again.
"""
import json, os, sys, urllib.request
import numpy as np

NAME, SIZE = "megt90n000cb.img", 720 * 1440 * 2
LOCAL = os.path.join("data", NAME)
URLS = [
    "https://pds-geosciences.wustl.edu/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg004/" + NAME,
    "https://pds-geosciences.wustl.edu/mgs/mgs-m-mola-5-megdr-l3-v1/mgsl_300x/meg004/" + NAME,
]
os.makedirs("data", exist_ok=True)

def ok():
    return os.path.exists(LOCAL) and os.path.getsize(LOCAL) == SIZE

for url in URLS:
    if ok():
        break
    try:
        print("Downloading", url)
        urllib.request.urlretrieve(url, LOCAL)
    except Exception as e:
        print("  failed:", e)
if not ok():
    sys.exit("Could not get %s (expected %d bytes). See the note at the top of this script." % (NAME, SIZE))

# Row 0 is 90N, column 0 is 0E, 0.25 degrees per pixel, east longitude 0-360.
grid = np.fromfile(LOCAL, dtype=">i2").reshape(720, 1440).astype(float)
NX, NY = 720, 360                       # must match G in index.html: 0.5 degree cells, whole planet
g = grid.reshape(360, 2, 720, 2).mean(axis=(1, 3))   # average 2x2 blocks: 0.25 to 0.5 degrees
z = np.roll(g, -360, axis=1)            # longitude 0..360 east becomes -180..180
if z.min() < -9000 or z.max() > 22000:
    sys.exit("Values look wrong (%s to %s). The file may be damaged." % (z.min(), z.max()))
json.dump({"nx": NX, "ny": NY, "z": [int(v) for v in z.ravel()]}, open("data/mola.json", "w"))
print("Saved data/mola.json. Elevation range %d to %d m" % (z.min(), z.max()))
