# Dusk Traverse – a Martian route planner

NASA Space Apps 2026 entry for **Interplanetary Survival Guide: Martian Map**. You plan a crewed traverse across the Isidis and Jezero region of Mars, balancing time, distance and risk on a map built from NASA data.

[Launch the deployed app](https://dusk-traverse.vercel.app/)

## What is in the folder

- `index.html` is the **project website**. Its **Launch platform** button opens the app.
- `app.html` is the **platform** itself (open it directly if you prefer).
- `assets/` holds the website's screenshots, `vendor/` the bundled map and 3D libraries, and `prepare_data.py` builds real NASA elevation data into `data/`.

## Run it

1. Unzip the folder and keep `index.html`, `app.html`, `assets/` and `vendor/` together.
2. Start a local server, which avoids browser restrictions:
   - `cd martian-map`
   - `python3 -m http.server 8000`
   - Open http://localhost:8000
3. You can also double-click `index.html`. It usually works without a server.

You need an internet connection for the Mars imagery. Leaflet is bundled in `vendor/`, so nothing else downloads.

## Two separate modes

The panel has two tabs that never mix:
- **Story traverse:** the mission game. Pick landing-region sites, stay inside the sol and risk limits, then **Launch traverse**. It has its own route, analytics and log.
- **Path finder:** the planning tool for any two points on Mars (or beacons), with fastest, balanced and safest routes, **Drive this route**, 3D, export and the dust storm slider.

Switching tabs clears the other mode's route and rover from the map, so **Drive this route** can only ever drive the path-finder route, and **Launch traverse** only the story route.

## How to play (story traverse)

1. Read the briefing. Your crew has landed at Jezero Delta.
2. Click a glowing beacon, read its story card, and press **Add to traverse**.
3. Watch the three meters: sols used (limit 80), kilometres, and risk (limit 35%).
4. Meet the goal: visit at least four sites within both limits. Green means safe, amber means close to the limit, red means you are over it.
5. Press **Launch traverse**. The rover drives your route, the story reveals each site, and the mission log records every arrival.
6. Use **Undo last stop** or **Start over** to try a different route.

The layer switch (top right) toggles between colour elevation relief and the Viking surface mosaic.

**Tip:** flat ground like Isidis Planitia is cheap in risk, while Nili Patera and Libya Montes are costly. The best routes mix the two.

## How it works

- **Map:** Leaflet with a geographic projection, loading NASA Mars Trek tiles (MOLA elevation, Viking colour mosaic).
- **Distance:** great-circle distance on a 3,389.5 km Mars radius.
- **Time:** 50 km per sol of driving, plus 2 sols of science at each stop (planning assumptions).
- **Risk:** each leg's risk rises with its length and the average hazard rating of its two ends, and legs combine as independent chances of trouble.
- **Hazard ratings (1 to 5)** are the author's estimates for gameplay, not official NASA values.

## 3D view and VR

Plan a route, then press **View in 3D**.

- **Orbit view:** drag to rotate, scroll to zoom. The rover drives your route while captions tell each site's story.
- **Chase view:** a camera follows behind the rover.
- **Replay** restarts the drive, and **Esc** closes the 3D view.
- **VR:** if your browser supports WebXR (for example a Meta Quest browser), a VR button appears. It shows the landscape as a miniature on a virtual table. This has not been tested on a headset, so treat it as experimental. WebXR needs the page served over HTTPS (GitHub Pages and Netlify both work), or `localhost` for local testing.
- The 3D terrain is built from the same elevation grid as the slope analysis, around whatever route you are viewing, with relief exaggerated 20 times. With stand-in terrain it is not real topography; once `data/mola.json` is loaded it is real NASA MOLA elevation.
- Three.js (r147) is bundled in `vendor/`, so no extra downloads are needed.

## Traverse graphs, multi-stop paths and your own places (new)

- The **analytics panel** now also shows for your story traverse (elevation profile, statistics and slope risk per leg). It follows the rover during **Launch traverse**.
- **Path finder with named places:** while the path finder is waiting for a point, click any glowing beacon to use it as a start, stop or destination. After the first route appears, press **Add another stop** to extend it into a multi-stop route. **New path** starts over.
- **Add a place:** press the button, click a plain, basin or crater, and name it. It becomes a beacon you can use in both the path finder and the traverse planner. Its hazard rating comes from the local slope.
- **Coverage:** slope analysis now covers all of Mars on a 0.5 degree grid (cells about 30 km wide), so the path finder works between any two points, with 14 more major places added (Olympus Mons, Valles Marineris, Hellas, Argyre, Utopia, Elysium, Gale, Gusev, Meridiani, Chryse, Acidalia, Arcadia, Amazonis and Arsia Mons). **Whole Mars** zooms out to see them all. Routes cannot cross the 180 degree line, and 30 km cells are too coarse for rover-scale hazards.

## Next steps
- Finer local grids (for example HiRISE or CTX terrain) around landing sites, and a route that can cross the 180 degree line.
- More NASA layers (minerals, ice, sunlight) to score science value, not just slope.

## Analytics, driving and what-if

After the path finder solves a route, a **Route analytics** panel appears at the bottom of the map:
- **Elevation profile** along the selected route, coloured by slope (green gentle, red steep). Hover over it and a marker follows the same spot on the map.
- **Risk comparison** bars for the fastest, balanced and safest routes.
- **Statistics:** distance, drive time, risk, steepest slope, kilometres of ground over 3 degrees, total climb and descent.

Click a row in the route table to select a route. Then:
- **Drive this route** animates the rover, and the profile cursor moves with it.
- **View in 3D** shows the chosen route in the 3D landscape.
- **Download route** saves it as a GeoJSON file you can open in GIS tools.
- The **dust storm slider** is a what-if scenario: it slows driving and raises risk, and recalculates all three routes live. Its numbers are modelling assumptions, not NASA data.

## Path finder and slope hazard

- A colour **slope hazard** layer (green flat, red steep) is on by default. Switch it off in the layer menu (top right).
- Press **Find the safest path**, click a start point, then a destination (inside the shaded region). The app compares three routes: **fastest** (straight line), **balanced** and **safest**, showing distance, sols, risk and steepest slope for each.
- The safest route is found with Dijkstra's algorithm over the elevation grid. Its cost and the risk score use the same slope formula, so "safest" really means lowest modelled risk.

### Real NASA elevation

`data/mola.json` (1.6 MB, real NASA MOLA elevation averaged to a 0.5 degree whole-planet grid) is **already included**, so the platform shows "real NASA MOLA data" with no extra steps. To rebuild it, run `pip install numpy` and then `python prepare_data.py`, which downloads the 2 MB NASA source file `megt90n000cb.img` (or save that file as `data/megt90n000cb.img` yourself). Browsers block loading the data file when `app.html` is opened by double-clicking, so use a server (Live Server, `python -m http.server`, or the deployed site).

## Customize

The platform is `app.html` and the website is `index.html`.

- Add or edit sites in the `SITES` array. Each has coordinates `ll: [lat, lon]`, a hazard `h`, a type `t` and a story `s`.
- Tune difficulty with the constants `KM_SOL`, `STOP_SOLS`, `MAX_SOLS`, `MAX_RISK` and `NEED`.
- If tiles do not appear, open the browser console and check the tile URL in the `trek()` function. The site may have changed its path or file extension. Then look up the current layer at https://trek.nasa.gov/mars/.

## Ideas for the next version

- Real slope and hazard from elevation data instead of rated sites.
- Landing-site comparison, sunlight and dust-storm layers.
- A share link for each route, and a mobile install option.

## Credits

Imagery: NASA/JPL, Mars Trek. Elevation: NASA MGS MOLA (PDS). Map engine: Leaflet (BSD-2). 3D: three.js (MIT). Not an official NASA product.
