# Copilot Instructions

## Repo at a glance
- This workspace is a collection of small experiments; the only substantial logic today lives in `ch01/love.py`, a Tkinter heart animation.
- `ch01/ch1_1.py` is just a scratch script (`print` statements); use it for quick sanity checks, not shared utilities.
- Python standard library plus Tkinter are the only dependencies; no virtualenv, packaging, or third-party modules are present.
- `love/loveTest.html` is an empty placeholder—treat it as future work, not an authoritative source.

## Heart animation architecture
- `Heart` precomputes point clouds for each animation frame inside `self.all_points`; generation happens in `__init__` via `build()` then `calc()` per frame (default `generate_frame=20`).
- `Heart.build(2000)` seeds the outline, then diffuses each point three times for edges and 4000 random picks for the core; tweak counts sparingly to avoid long startup.
- Geometry helpers (`heart_function`, `scatter_inside`, `shrink`, `curve`) transform polar inputs into canvas coordinates and jitter; they rely on the module-level canvas constants.
- `calc()` recomputes halo radii and counts every frame, creating ~7k halo particles—keep new math operations O(1) per point.
- `draw()` is the Tkinter render loop: it clears the canvas, paints the precomputed frame, then re-enqueues itself with `after(160, ...)`.
- Rendering always uses `Canvas.create_rectangle` with small random sizes to simulate glow; if you add new effects, keep them lightweight to maintain frame time.

## Conventions & guardrails
- Stick with integer pixel positions when touching render data; `Heart.render` assumes whole-number coordinates.
- All randomization comes from Python's `random`; if you introduce repeatability, pass a seeded `random.Random` through instead of using globals.
- Constants such as `CANVAS_WIDTH`, `IMAGE_ENLARGE`, and `HEART_COLOR` act as the public "knobs"—reuse them or add nearby constants rather than sprinkling literals.
- Avoid new dependencies unless absolutely necessary; prefer extending the existing math helpers for new visual effects.

## Developer workflow
- Run the animation with `python ch01/love.py` (PowerShell: `python .\ch01\love.py`). Tkinter must be available in the active Python install.
- There is no automated test suite; validate visually by running the script. If you add logic that can be unit-tested, colocate lightweight tests under `ch01/`.
- When modifying animation loops, watch for performance regressions—keep `generate_frame` manageable (currently 20) to avoid load-time delays.

## Extending this project
- New animations can live beside `love.py` under `ch01/`; mirror the structure (module constants, helper math, `Heart`-like class, `draw` loop) for consistency.
- For UI tweaks (window title, background color), adjust the constants at the bottom of `love.py` rather than hard-coding inside functions.
- If you revive `loveTest.html`, document any build steps because none currently exist; otherwise keep web assets decoupled from the Tkinter app.
