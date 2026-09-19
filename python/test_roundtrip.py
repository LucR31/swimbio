import numpy as np
from python.swim_format import SwimFile, write_swim, read_swim, validate_swim

path = "/home/claude/swimfmt/example_race.swim"

n_frames = 5231
fps = 100.0
t = np.arange(n_frames) / fps
joints = ["hip", "shoulder_r", "shoulder_l", "wrist_r", "wrist_l", "ankle_r", "ankle_l"]
pos = np.cumsum(np.random.randn(n_frames, len(joints), 3) * 0.01, axis=0)
vel = np.gradient(pos, t, axis=0)

with SwimFile(path, "w") as f:
    f.set_metadata(athlete_name="Jane Doe", athlete_id="USA-12345", sex="F",
                    age=22, height_cm=178, weight_kg=68,
                    event="100m Freestyle", distance_m=100, stroke="freestyle",
                    course="LCM", pool_length_m=50, date="2026-09-18",
                    competition="World Cup Berlin", location="Berlin, GER",
                    lane=4, heat=3, result_time_s=52.31,
                    notes="Personal best")
    f.add_splits(split_distance_m=[50, 100], split_time_s=[25.10, 27.21],
                 cumulative_time_s=[25.10, 52.31])
    f.add_laps(lap_number=[1, 2], lap_time_s=[25.10, 27.21],
               stroke_count=[32, 34], stroke_rate_spm=[52.3, 50.1],
               stroke_length_m=[2.1, 2.0])
    f.add_kinematics(time=t, joint_names=joints, position=pos, velocity=vel,
                      sample_rate_hz=fps)
    f.add_stroke_metrics(stroke_index=np.arange(66), stroke_time_s=np.linspace(0, 52.31, 66),
                          stroke_rate_spm=np.random.uniform(48, 54, 66),
                          stroke_length_m=np.random.uniform(1.9, 2.2, 66))
    f.add_imu(location="sacrum", time=t, accel=np.random.randn(n_frames, 3),
              gyro=np.random.randn(n_frames, 3), sample_rate_hz=fps)
    f.add_forces(time=np.linspace(0, 0.4, 400), force_n=np.random.uniform(200, 600, 400))
    f.add_video_sync(sync_timestamps=t[::4], frame_rate_hz=25.0,
                      resolution="1920x1080", camera_id="cam_side_1")

print("---- validate ----")
print(validate_swim(path) or "OK, no problems found")

print("\n---- summary() ----")
with SwimFile(path, "r") as f:
    print(f.summary())

print("\n---- read_swim() round-trip checks ----")
data = read_swim(path)
assert data["metadata"]["athlete_name"] == "Jane Doe"
assert abs(data["metadata"]["result_time_s"] - 52.31) < 1e-9
assert data["kinematics"]["joint_names"] == joints
assert np.allclose(data["kinematics"]["position"], pos)
assert np.allclose(data["kinematics"]["velocity"], vel)
assert data["splits"]["split_distance_m"].tolist() == [50.0, 100.0]
assert data["laps"]["stroke_count"].tolist() == [32, 34]
assert "sacrum" in data["imu"]
assert data["forces"]["force_n"].shape == (400,)
assert data["video"]["resolution"] == "1920x1080"
print("All round-trip assertions passed.")

import os
print(f"\nFile size: {os.path.getsize(path)/1024:.1f} KB")
