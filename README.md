# .swim — a file format for swimming race & biomechanics data

`.swim` is an HDF5 file with a fixed schema for swimming race results
and athlete biomechanics (kinematics, IMU, force, video-sync). Because
it's plain HDF5, it opens natively in Python and MATLAB (and C, Julia,
R, HDFView, `h5dump`, etc.) — no custom parser needed.

[https://swimbio.readthedocs.io/en/latest/](https://swimbio.readthedocs.io/en/latest/)

## Files in this package

| File                     | Purpose                                                        |
|--------------------------|-----------------------------------------------------------------|
| `SWIM_FORMAT_SPEC.md`    | The schema: group/dataset/attribute layout, units, conventions |
| `swim_format.py`         | Python library (`h5py`-based): `SwimFile` class + `read_swim`/`write_swim`/`validate_swim` |
| `example_usage.py`       | Minimal Python example — write then read a `.swim` file        |
| `test_roundtrip.py`      | Fuller test exercising every group, with assertions             |
| `readSwimFile.m`         | MATLAB: generic recursive reader, any `.swim` file → nested struct |
| `writeSwimFile.m`        | MATLAB: generic recursive writer, nested struct → `.swim` file |
| `example_usage.m`        | Minimal MATLAB example — build a struct, write, read it back   |
| `example_race.swim`      | Sample file produced by `test_roundtrip.py` (real data, for you to poke at) |

## Requirements

- **Python**: `pip install h5py numpy`
- **MATLAB**: no toolbox needed.

## Python quick start

```python
from swim_format import SwimFile
import numpy as np

with SwimFile("race001.swim", "w") as f:
    f.set_metadata(athlete_name="Jane Doe", event="100m Freestyle",
                    distance_m=100, stroke="freestyle", course="LCM",
                    date="2026-09-18", result_time_s=52.31)
    f.add_kinematics(time=np.linspace(0, 52.31, 5231),
                      joint_names=["hip", "shoulder_r", "wrist_r"],
                      position=np.random.randn(5231, 3, 3))

with SwimFile("race001.swim", "r") as f:
    print(f.summary())
    kin = f.get_kinematics()
```

Or the one-shot functional API: `write_swim(path, metadata={...}, kinematics={...}, ...)`
and `data = read_swim(path)` for a full dict dump.

## MATLAB quick start

```matlab
s.metadata.attrs.athlete_name = 'Jane Doe';
s.metadata.attrs.event = '100m Freestyle';
s.metadata.attrs.result_time_s = 52.31;
s.kinematics.time = (0:5230)'/100;
s.kinematics.joint_names = {'hip','shoulder_r','wrist_r'};
s.kinematics.position = randn(5231, 3, 3);

writeSwimFile('race001.swim', s);
r = readSwimFile('race001.swim');
disp(r.metadata.attrs.athlete_name)
```

A file written by the Python library opens directly in MATLAB with
`readSwimFile`, and vice versa — that's the entire point of building
this on plain HDF5 rather than a bespoke binary layout.

## Extending it

Add new fields freely (extra metadata attributes, extra sensor
locations via `add_imu`, custom groups under `/custom/...`). See
`SWIM_FORMAT_SPEC.md` section 5 ("Extensibility") for the convention
on where to put things that aren't in the core schema, so future tools
don't collide with your additions.

## Verified

`test_roundtrip.py` was run end-to-end in Python (write → validate →
read → assert equality on every field) — see `example_race.swim`
produced by it. The MATLAB functions are written against MATLAB's
documented `h5create`/`h5write`/`h5read`/`H5G`/`H5T`/`H5D` APIs but
could not be executed in this environment (no MATLAB available here),
so test them on your first real file and see the axis-order note in
the spec if a multi-dimensional array looks transposed.
