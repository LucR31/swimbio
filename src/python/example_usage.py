"""
Minimal example: create a .swim file for one race, then read it back.
Run: python3 example_usage.py
"""
import numpy as np
from swim_format import SwimFile, read_swim

path = "demo_race.swim"
fps = 100.0
duration_s = 52.31
n = int(duration_s * fps)
t = np.arange(n) / fps
joints = ["hip", "shoulder_r", "shoulder_l", "wrist_r", "wrist_l"]
position = np.cumsum(np.random.randn(n, len(joints), 3) * 0.01, axis=0)

# ---- write ----
with SwimFile(path, "w") as f:
    f.set_metadata(
        athlete_name="Jane Doe",
        event="100m Freestyle",
        distance_m=100,
        stroke="freestyle",
        course="LCM",
        date="2026-09-18",
        result_time_s=duration_s,
    )
    f.add_splits(
        split_distance_m=[50, 100],
        split_time_s=[25.10, 27.21],
        cumulative_time_s=[25.10, 52.31],
    )
    f.add_kinematics(time=t, joint_names=joints, position=position, sample_rate_hz=fps)

# ---- read ----
data = read_swim(path)
print("Athlete:", data["metadata"]["athlete_name"])
print(
    "Event:",
    data["metadata"]["event"],
    "| Result:",
    data["metadata"]["result_time_s"],
    "s",
)
print("Kinematics joints:", data["kinematics"]["joint_names"])
print("Position array shape:", data["kinematics"]["position"].shape)
print("Splits:", data["splits"])
