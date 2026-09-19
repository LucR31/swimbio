# .swim File Format Specification (v1.0)

## 1. Overview

`.swim` is a domain-specific container format for swimming race and
athlete biomechanics data. It is **not a new binary format** — a `.swim`
file *is* a standard HDF5 file (fully compliant with the HDF5 spec) that
follows a fixed group/dataset/attribute layout, plus the `.swim`
extension by convention.

Because it is plain HDF5, it can be opened by:
- **Python** — `h5py` (see `swim_format.py` in this package), or generic
  tools like `h5dump`.
- **MATLAB** — the built-in `h5read`/`h5write`/`h5info`/`h5create`
  family, or the convenience wrappers `readSwimFile.m` / `writeSwimFile.m`.
- Any other HDF5 binding (C/C++, Julia, R, `h5dump` CLI, HDFView GUI).

Renaming a `.swim` file to `.h5` (or vice versa) does not change its
contents — the extension is purely a naming convention that signals
"this HDF5 file follows the SWIM schema below."

## 2. Root-level attributes

Every `.swim` file has these attributes on the root group `/`:

| Attribute        | Type   | Description                                   |
|------------------|--------|------------------------------------------------|
| `format`         | string | Always `"SWIM"`                                |
| `format_version` | string | Schema version, e.g. `"1.0"`                   |
| `created`        | string | ISO-8601 creation timestamp                    |
| `creator`        | string | Tool/library + version that wrote the file     |

## 3. Group layout

```
/ (root, attrs: format, format_version, created, creator)
├── metadata/                     (group, all fields stored as attrs)
│     athlete_name, athlete_id, sex, age, height_cm, weight_kg,
│     event, distance_m, stroke, course, pool_length_m, date,
│     competition, location, lane, heat, result_time_s, notes, ...
│
├── race/
│     ├── splits/                 (group)
│     │     split_distance_m   (N,)  float64
│     │     split_time_s       (N,)  float64
│     │     cumulative_time_s  (N,)  float64
│     └── laps/                   (group)
│           lap_number         (N,)  int32
│           lap_time_s         (N,)  float64
│           stroke_count       (N,)  int32
│           stroke_rate_spm    (N,)  float64
│           stroke_length_m    (N,)  float64
│
├── kinematics/                    (group, attrs: sample_rate_hz,
│    │                              coordinate_system, units)
│     time                 (F,)        float64, seconds
│     joint_names           (J,)        variable-length UTF-8 strings
│     position              (F, J, 3)   float64, meters
│     velocity              (F, J, 3)   float64, m/s        [optional]
│     acceleration          (F, J, 3)   float64, m/s^2      [optional]
│     joint_angle_names     (A,)        variable-length UTF-8 strings [optional]
│     joint_angles          (F, A)      float64, degrees    [optional]
│
├── stroke_metrics/                (group, attrs: sample_rate_hz)
│     stroke_index          (S,)   int32
│     stroke_time_s         (S,)   float64
│     stroke_rate_spm       (S,)   float64
│     stroke_length_m       (S,)   float64
│     dps                   (S,)   float64   (distance per stroke, m)
│
├── sensors/
│     └── imu_<location>/         (group per sensor, e.g. imu_sacrum,
│           │                      imu_wrist_left; attrs: sample_rate_hz,
│           │                      location)
│           time             (T,)      float64, seconds
│           accel            (T, 3)    float64, m/s^2
│           gyro             (T, 3)    float64, deg/s
│           mag              (T, 3)    float64, microtesla [optional]
│
├── forces/                        (group, attrs: sample_rate_hz)
│     time                 (K,)   float64, seconds
│     force_n              (K,)   float64, Newtons
│     (e.g. tethered swimming force or wall push-off force plate)
│
└── video/                         (group, attrs: frame_rate_hz,
     │                              resolution, camera_id)
     sync_timestamps        (F,)   float64, seconds (aligned to
                                    kinematics/time)
```

All groups except `metadata` and root are **optional** — write only the
groups relevant to the data you have. Datasets within `kinematics`,
`sensors/*`, `forces`, etc. marked `[optional]` may be omitted.

## 4. Conventions

- **Units**: SI throughout (meters, seconds, m/s, m/s², Newtons,
  degrees for angles, degrees/s for angular rates). Any deviation must
  be declared in the relevant group's attributes.
- **Time**: every time series has its own `time` dataset in seconds,
  relative to the start of the recording (`t=0` at race start /
  first sample). Multiple time series are not assumed to share a clock
  unless explicitly noted (e.g. `video/sync_timestamps` is aligned to
  `kinematics/time` by definition).
- **Coordinate system**: declared in `kinematics` attrs
  (`coordinate_system`, e.g. `"pool: x=length, y=width, z=vertical, origin=start wall, right-handed"`).
  x should follow the direction of swimming, z should be vertical (up
  positive).
- **Strings**: stored as HDF5 variable-length UTF-8 (`h5py.string_dtype()`
  in Python; MATLAB reads these back as cell arrays of char).
- **Compression**: datasets over ~1000 elements should use gzip
  compression (level 4) with chunking; this is transparent to readers.
- **Missing data**: use `NaN` for missing numeric samples rather than
  omitting rows, so time alignment is preserved.

## 5. Cross-language note: multi-dimensional array axis order

HDF5 itself is unambiguous about a dataset's shape (e.g. `(F, J, 3)`),
but Python/NumPy (row-major/C order) and MATLAB (column-major/Fortran
order) can present that same on-disk data with dimensions reported in
different orders. In practice, 1-D datasets (`time`, `split_time_s`,
etc.) are unaffected. For datasets with 2+ dimensions (`position`,
`velocity`, `joint_angles`, `accel`, `gyro`), after calling
`readSwimFile` in MATLAB, check `size(...)` against what you expect
(e.g. `[nFrames, nJoints, 3]`); if the axes come back reversed relative
to the Python shape, use `permute(x, ndims(x):-1:1)` to restore the
expected order. This is a property of MATLAB's HDF5 bindings, not of
the file itself — the underlying data is identical either way.

## 6. Extensibility

Additional groups/attributes not in this spec are allowed (readers
should ignore what they don't recognize) but should be namespaced under
a top-level group, e.g. `/custom/<vendor>/...`, to avoid clashing with
future core schema additions. Bump `format_version` only for
breaking changes to the core groups above.
