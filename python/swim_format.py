"""
swim_format.py
==============
Read/write library for the .swim file format (HDF5-based container for
swimming race and biomechanics data). See SWIM_FORMAT_SPEC.md for the
full schema.

Requires: h5py, numpy

Quick start
-----------
    from swim_format import SwimFile
    import numpy as np

    with SwimFile("race001.swim", "w") as f:
        f.set_metadata(athlete_name="Jane Doe", event="100m Freestyle",
                        distance_m=100, stroke="freestyle", course="LCM",
                        date="2026-09-18", result_time_s=52.31)
        f.add_splits(split_distance_m=[50, 100],
                     split_time_s=[25.1, 27.21],
                     cumulative_time_s=[25.1, 52.31])
        f.add_kinematics(time=np.linspace(0, 52.31, 5231),
                          joint_names=["hip", "shoulder_r", "wrist_r"],
                          position=np.random.randn(5231, 3, 3))

    with SwimFile("race001.swim", "r") as f:
        meta = f.get_metadata()
        kin = f.get_kinematics()

Author: generated for user request (swimming biomechanics HDF5 format)
"""

from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

import h5py
import numpy as np

FORMAT_NAME = "SWIM"
FORMAT_VERSION = "1.0"
CREATOR = "swim_format.py v1.0"

ArrayLike = Union[np.ndarray, Sequence[float], Sequence[Sequence[float]]]

_STR_DTYPE = h5py.string_dtype(encoding="utf-8")


def _as_array(x: ArrayLike, dtype=np.float64) -> np.ndarray:
    return np.asarray(x, dtype=dtype)


def _write_strings(group: h5py.Group, name: str, strings: Iterable[str]) -> None:
    data = np.array(list(strings), dtype=object)
    group.create_dataset(name, data=data, dtype=_STR_DTYPE)


def _read_strings(dataset: h5py.Dataset) -> List[str]:
    return [s.decode("utf-8") if isinstance(s, bytes) else str(s) for s in dataset[()]]


def _chunks_for(shape):
    """Reasonable chunk shape: chunk the leading (time/frame) axis only."""
    if not shape:
        return None
    n = shape[0]
    if n <= 1024:
        return None  # too small to bother compressing/chunking
    first = min(n, 4096)
    return (first,) + tuple(shape[1:])


def _create_dataset(group: h5py.Group, name: str, data: np.ndarray) -> h5py.Dataset:
    chunks = _chunks_for(data.shape)
    kwargs: Dict[str, Any] = {}
    if chunks is not None:
        kwargs.update(chunks=chunks, compression="gzip", compression_opts=4)
    return group.create_dataset(name, data=data, **kwargs)


class SwimFile:
    """Context-manager wrapper around an h5py.File following the SWIM schema."""

    def __init__(self, path: str, mode: str = "r"):
        self.path = path
        self.mode = mode
        self._h5: Optional[h5py.File] = None

    # -- lifecycle -----------------------------------------------------
    def __enter__(self) -> "SwimFile":
        self._h5 = h5py.File(self.path, self.mode)
        if self.mode in ("w", "w-", "x"):
            self._h5.attrs["format"] = FORMAT_NAME
            self._h5.attrs["format_version"] = FORMAT_VERSION
            self._h5.attrs["created"] = _dt.datetime.utcnow().isoformat() + "Z"
            self._h5.attrs["creator"] = CREATOR
            self._h5.require_group("metadata")
        elif self.mode in ("a", "r+"):
            if "format" not in self._h5.attrs:
                self._h5.attrs["format"] = FORMAT_NAME
                self._h5.attrs["format_version"] = FORMAT_VERSION
                self._h5.attrs["created"] = _dt.datetime.utcnow().isoformat() + "Z"
                self._h5.attrs["creator"] = CREATOR
            self._h5.require_group("metadata")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        if self._h5 is not None:
            self._h5.close()
            self._h5 = None

    @property
    def h5(self) -> h5py.File:
        if self._h5 is None:
            raise RuntimeError("SwimFile is not open (use as a context manager)")
        return self._h5

    # -- metadata --------------------------------------------------------
    def set_metadata(self, **fields: Any) -> None:
        """Set free-form metadata fields (athlete_name, event, distance_m,
        stroke, course, date, result_time_s, etc.) as attributes on
        /metadata. Values must be strings, numbers, or bools."""
        grp = self.h5.require_group("metadata")
        for key, value in fields.items():
            if value is None:
                continue
            grp.attrs[key] = value

    def get_metadata(self) -> Dict[str, Any]:
        grp = self.h5["metadata"]
        return {k: (v.item() if isinstance(v, np.generic) else v) for k, v in grp.attrs.items()}

    # -- race: splits / laps ---------------------------------------------
    def add_splits(self, split_distance_m: ArrayLike, split_time_s: ArrayLike,
                    cumulative_time_s: ArrayLike) -> None:
        grp = self.h5.require_group("race/splits")
        _create_dataset(grp, "split_distance_m", _as_array(split_distance_m))
        _create_dataset(grp, "split_time_s", _as_array(split_time_s))
        _create_dataset(grp, "cumulative_time_s", _as_array(cumulative_time_s))

    def get_splits(self) -> Dict[str, np.ndarray]:
        grp = self.h5["race/splits"]
        return {k: grp[k][()] for k in grp.keys()}

    def add_laps(self, lap_number: ArrayLike, lap_time_s: ArrayLike,
                  stroke_count: Optional[ArrayLike] = None,
                  stroke_rate_spm: Optional[ArrayLike] = None,
                  stroke_length_m: Optional[ArrayLike] = None) -> None:
        grp = self.h5.require_group("race/laps")
        _create_dataset(grp, "lap_number", _as_array(lap_number, dtype=np.int32))
        _create_dataset(grp, "lap_time_s", _as_array(lap_time_s))
        if stroke_count is not None:
            _create_dataset(grp, "stroke_count", _as_array(stroke_count, dtype=np.int32))
        if stroke_rate_spm is not None:
            _create_dataset(grp, "stroke_rate_spm", _as_array(stroke_rate_spm))
        if stroke_length_m is not None:
            _create_dataset(grp, "stroke_length_m", _as_array(stroke_length_m))

    def get_laps(self) -> Dict[str, np.ndarray]:
        grp = self.h5["race/laps"]
        return {k: grp[k][()] for k in grp.keys()}

    # -- kinematics --------------------------------------------------------
    def add_kinematics(self, time: ArrayLike, joint_names: Sequence[str],
                        position: ArrayLike,
                        velocity: Optional[ArrayLike] = None,
                        acceleration: Optional[ArrayLike] = None,
                        joint_angle_names: Optional[Sequence[str]] = None,
                        joint_angles: Optional[ArrayLike] = None,
                        sample_rate_hz: Optional[float] = None,
                        coordinate_system: str = "pool: x=length, y=width, "
                        "z=vertical(up), origin=start wall, right-handed",
                        units: str = "meters, seconds") -> None:
        grp = self.h5.require_group("kinematics")
        grp.attrs["coordinate_system"] = coordinate_system
        grp.attrs["units"] = units
        if sample_rate_hz is not None:
            grp.attrs["sample_rate_hz"] = float(sample_rate_hz)

        t = _as_array(time)
        pos = _as_array(position)
        if pos.shape[0] != t.shape[0]:
            raise ValueError("position first axis must match len(time)")
        if pos.shape[1] != len(joint_names):
            raise ValueError("position second axis must match len(joint_names)")

        _create_dataset(grp, "time", t)
        _write_strings(grp, "joint_names", joint_names)
        _create_dataset(grp, "position", pos)

        if velocity is not None:
            _create_dataset(grp, "velocity", _as_array(velocity))
        if acceleration is not None:
            _create_dataset(grp, "acceleration", _as_array(acceleration))
        if joint_angles is not None:
            if joint_angle_names is None:
                raise ValueError("joint_angle_names required if joint_angles is given")
            _write_strings(grp, "joint_angle_names", joint_angle_names)
            _create_dataset(grp, "joint_angles", _as_array(joint_angles))

    def get_kinematics(self) -> Dict[str, Any]:
        grp = self.h5["kinematics"]
        out: Dict[str, Any] = dict(grp.attrs)
        for key in ("time", "position", "velocity", "acceleration", "joint_angles"):
            if key in grp:
                out[key] = grp[key][()]
        if "joint_names" in grp:
            out["joint_names"] = _read_strings(grp["joint_names"])
        if "joint_angle_names" in grp:
            out["joint_angle_names"] = _read_strings(grp["joint_angle_names"])
        return out

    # -- stroke metrics ------------------------------------------------------
    def add_stroke_metrics(self, stroke_index: ArrayLike, stroke_time_s: ArrayLike,
                            stroke_rate_spm: ArrayLike, stroke_length_m: ArrayLike,
                            dps: Optional[ArrayLike] = None,
                            sample_rate_hz: Optional[float] = None) -> None:
        grp = self.h5.require_group("stroke_metrics")
        if sample_rate_hz is not None:
            grp.attrs["sample_rate_hz"] = float(sample_rate_hz)
        _create_dataset(grp, "stroke_index", _as_array(stroke_index, dtype=np.int32))
        _create_dataset(grp, "stroke_time_s", _as_array(stroke_time_s))
        _create_dataset(grp, "stroke_rate_spm", _as_array(stroke_rate_spm))
        _create_dataset(grp, "stroke_length_m", _as_array(stroke_length_m))
        if dps is not None:
            _create_dataset(grp, "dps", _as_array(dps))

    def get_stroke_metrics(self) -> Dict[str, np.ndarray]:
        grp = self.h5["stroke_metrics"]
        return {k: grp[k][()] for k in grp.keys()}

    # -- sensors (IMU) ------------------------------------------------------
    def add_imu(self, location: str, time: ArrayLike, accel: ArrayLike,
                gyro: ArrayLike, mag: Optional[ArrayLike] = None,
                sample_rate_hz: Optional[float] = None) -> None:
        grp = self.h5.require_group(f"sensors/imu_{location}")
        grp.attrs["location"] = location
        if sample_rate_hz is not None:
            grp.attrs["sample_rate_hz"] = float(sample_rate_hz)
        _create_dataset(grp, "time", _as_array(time))
        _create_dataset(grp, "accel", _as_array(accel))
        _create_dataset(grp, "gyro", _as_array(gyro))
        if mag is not None:
            _create_dataset(grp, "mag", _as_array(mag))

    def list_sensors(self) -> List[str]:
        if "sensors" not in self.h5:
            return []
        return [name[len("imu_"):] for name in self.h5["sensors"].keys()
                if name.startswith("imu_")]

    def get_imu(self, location: str) -> Dict[str, Any]:
        grp = self.h5[f"sensors/imu_{location}"]
        out: Dict[str, Any] = dict(grp.attrs)
        for key in ("time", "accel", "gyro", "mag"):
            if key in grp:
                out[key] = grp[key][()]
        return out

    # -- forces --------------------------------------------------------------
    def add_forces(self, time: ArrayLike, force_n: ArrayLike,
                    sample_rate_hz: Optional[float] = None) -> None:
        grp = self.h5.require_group("forces")
        if sample_rate_hz is not None:
            grp.attrs["sample_rate_hz"] = float(sample_rate_hz)
        _create_dataset(grp, "time", _as_array(time))
        _create_dataset(grp, "force_n", _as_array(force_n))

    def get_forces(self) -> Dict[str, np.ndarray]:
        grp = self.h5["forces"]
        return {k: grp[k][()] for k in grp.keys()}

    # -- video sync ------------------------------------------------------------
    def add_video_sync(self, sync_timestamps: ArrayLike, frame_rate_hz: float,
                        resolution: Optional[str] = None,
                        camera_id: Optional[str] = None) -> None:
        grp = self.h5.require_group("video")
        grp.attrs["frame_rate_hz"] = float(frame_rate_hz)
        if resolution is not None:
            grp.attrs["resolution"] = resolution
        if camera_id is not None:
            grp.attrs["camera_id"] = camera_id
        _create_dataset(grp, "sync_timestamps", _as_array(sync_timestamps))

    def get_video_sync(self) -> Dict[str, Any]:
        grp = self.h5["video"]
        out: Dict[str, Any] = dict(grp.attrs)
        out["sync_timestamps"] = grp["sync_timestamps"][()]
        return out

    # -- introspection --------------------------------------------------------
    def summary(self) -> str:
        lines = [f"SWIM file: {self.path}",
                 f"  format_version: {self.h5.attrs.get('format_version')}",
                 f"  created: {self.h5.attrs.get('created')}"]
        meta = self.get_metadata()
        if meta:
            lines.append("  metadata: " + ", ".join(f"{k}={v}" for k, v in meta.items()))
        for grp_name in ("race/splits", "race/laps", "kinematics",
                         "stroke_metrics", "forces", "video"):
            if grp_name in self.h5:
                grp = self.h5[grp_name]
                shapes = ", ".join(f"{k}{grp[k].shape}" for k in grp.keys()
                                    if isinstance(grp[k], h5py.Dataset))
                lines.append(f"  {grp_name}: {shapes}")
        sensors = self.list_sensors()
        if sensors:
            lines.append(f"  sensors: {', '.join(sensors)}")
        return "\n".join(lines)


# -- convenience functional API ---------------------------------------------

def write_swim(path: str, metadata: Dict[str, Any],
               splits: Optional[Dict[str, ArrayLike]] = None,
               laps: Optional[Dict[str, ArrayLike]] = None,
               kinematics: Optional[Dict[str, Any]] = None,
               stroke_metrics: Optional[Dict[str, ArrayLike]] = None,
               imu: Optional[Dict[str, Dict[str, Any]]] = None,
               forces: Optional[Dict[str, ArrayLike]] = None,
               video: Optional[Dict[str, Any]] = None) -> None:
    """One-shot writer: pass plain dicts matching each add_* method's kwargs."""
    with SwimFile(path, "w") as f:
        f.set_metadata(**metadata)
        if splits:
            f.add_splits(**splits)
        if laps:
            f.add_laps(**laps)
        if kinematics:
            f.add_kinematics(**kinematics)
        if stroke_metrics:
            f.add_stroke_metrics(**stroke_metrics)
        if imu:
            for location, data in imu.items():
                f.add_imu(location=location, **data)
        if forces:
            f.add_forces(**forces)
        if video:
            f.add_video_sync(**video)


def read_swim(path: str) -> Dict[str, Any]:
    """One-shot reader: returns a nested dict with everything in the file."""
    out: Dict[str, Any] = {}
    with SwimFile(path, "r") as f:
        out["metadata"] = f.get_metadata()
        if "race/splits" in f.h5:
            out["splits"] = f.get_splits()
        if "race/laps" in f.h5:
            out["laps"] = f.get_laps()
        if "kinematics" in f.h5:
            out["kinematics"] = f.get_kinematics()
        if "stroke_metrics" in f.h5:
            out["stroke_metrics"] = f.get_stroke_metrics()
        sensors = f.list_sensors()
        if sensors:
            out["imu"] = {loc: f.get_imu(loc) for loc in sensors}
        if "forces" in f.h5:
            out["forces"] = f.get_forces()
        if "video" in f.h5:
            out["video"] = f.get_video_sync()
    return out


def validate_swim(path: str) -> List[str]:
    """Return a list of problems found (empty list = looks valid)."""
    problems = []
    try:
        with h5py.File(path, "r") as h5:
            if h5.attrs.get("format") != FORMAT_NAME:
                problems.append("root attribute 'format' missing or != 'SWIM'")
            if "format_version" not in h5.attrs:
                problems.append("root attribute 'format_version' missing")
            if "metadata" not in h5:
                problems.append("required group 'metadata' missing")
            if "kinematics" in h5:
                grp = h5["kinematics"]
                if "time" in grp and "position" in grp:
                    if grp["time"].shape[0] != grp["position"].shape[0]:
                        problems.append("kinematics/time and kinematics/position "
                                         "length mismatch")
    except OSError as exc:
        problems.append(f"could not open file as HDF5: {exc}")
    return problems
