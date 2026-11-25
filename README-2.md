# Space Simulations

Two interactive astronomy simulations built with Python and pygame: a gravity sandbox where you launch your own planets, and a three-scene star lab covering pulsars, binary stars, and the full life cycle of a star.

![Solar system simulator](assets/solar-system.png)

## Contents

| File | What it is |
| --- | --- |
| `solar_system.py` | N-body solar system sandbox with real Newtonian gravity |
| `star_lab.py` | Star Lab: pulsar, binary star, and life of a star in one window |

## Quick start

Requires Python 3.9 or newer.

```bash
git clone https://github.com/AOngomefen/REPO-NAME.git
cd REPO-NAME
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python solar_system.py
python star_lab.py
```

If `pygame` fails to install on a very new Python release, use `pip install pygame-ce` instead. It is a drop-in replacement and the code runs unchanged.

## Solar system simulator

A sun and four planets start on circular orbits. Every body pulls on every other body, so planets tug on each other and orbits drift in realistic ways.

| Input | Action |
| --- | --- |
| Click and drag | Launch a new planet. Drag direction and length set its velocity |
| `Space` | Pause or resume |
| `Up` / `Down` | Speed up or slow down time |
| `T` | Toggle orbit trails |
| `C` | Clear trails |
| `R` | Reset the system |
| `Esc` | Quit |

Planets that hit the sun are absorbed, and ones flung far away are removed.

## Star Lab

Press `1`, `2`, or `3` (or click a tab) to switch scenes. `Space` pauses, `H` hides the text overlay, and `Esc` quits.

### 1. Pulsar

![Pulsar](assets/pulsar.png)

A spinning neutron star with two radiation beams and rotating magnetic field lines. Each time a beam sweeps across Earth, the planet flashes and a spike appears in the brightness graph.

- `Up` / `Down`: spin faster or slower

### 2. Binary star

![Binary star](assets/binary-star.png)

Two stars orbit their shared centre of mass. An inset shows the edge-on view from Earth, and the graph records the total brightness, which dips when one star passes in front of the other.

- `Left` / `Right`: change the mass ratio (1:1, 2:1, 4:1)
- `E`: change the orbit shape (circular to elongated)
- `T`: toggle trails
- `Up` / `Down`: change time speed

### 3. Life of a star

| Main sequence | Supernova | Black hole |
| --- | --- | --- |
| ![Main sequence](assets/life-main-sequence.png) | ![Supernova](assets/life-supernova.png) | ![Black hole](assets/life-black-hole.png) |

Six stages with a clickable timeline: nebula, protostar, main sequence, red giant or supergiant, then the ending. Three star types, each with its own fate:

| Star type | Ending |
| --- | --- |
| Sun-like | Planetary nebula, then a cooling white dwarf |
| Massive | Supernova, then a neutron star with pulsar beams |
| Very massive | Supernova, then a black hole with an accretion disk |

- `Left` / `Right`: previous or next stage
- `M`: cycle the star type
- `A`: toggle auto-advance
- `Up` / `Down`: change speed
- Click any stage on the timeline to jump to it

## How it works

- **Gravity:** both simulations compute pairwise Newtonian gravity, `F = G * m1 * m2 / r^2`. The solar system uses velocity Verlet integration and the binary star uses leapfrog (kick-drift-kick). Both are symplectic, so orbits stay stable instead of slowly spiraling in or out.
- **Softening:** a small softening term keeps forces finite when two bodies pass very close together.
- **Binary orbits:** starting speeds come from the vis-viva equation, so the eccentricity setting produces the intended orbit shape.
- **Eclipse light curve:** the brightness graph is computed from the real overlap area of the two stellar discs, weighted by each star's surface brightness, so the dips have the right depth and shape.
- **Pulsar timing:** the beam angle is sampled several times per frame so narrow pulses are never skipped, even at high spin rates.
- **Glow effects:** radial gradients are drawn once, cached, and added onto the screen with additive blending. This keeps the scenes smooth at 60 FPS.

## Ideas for next steps

- Planet collisions that merge masses
- A second sun in the solar system sandbox
- Recording GIFs of each Star Lab scene for this README
- A fourth Star Lab scene for neutron star mergers

## Tech

Python, pygame, Newtonian physics, numerical integration, procedural graphics.

## License

MIT
