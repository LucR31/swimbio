%% Minimal example: create a .swim file for one race, then read it back.
% Requires readSwimFile.m and writeSwimFile.m to be on the MATLAB path.

fps = 100;
duration_s = 52.31;
n = round(duration_s * fps);
t = (0:n-1)' / fps;
jointNames = {'hip','shoulder_r','shoulder_l','wrist_r','wrist_l'};
position = cumsum(randn(n, numel(jointNames), 3) * 0.01, 1);

%% ---- build the struct ----
% Scalar metadata fields go under .attrs so they are written as HDF5
% attributes on /metadata (matching the spec and the Python library),
% and so they round-trip back into r.metadata.attrs.* via readSwimFile.

s = struct();
s.metadata.attrs.athlete_name   = 'Jane Doe';
s.metadata.attrs.event          = '100m Freestyle';
s.metadata.attrs.distance_m     = 100;
s.metadata.attrs.stroke         = 'freestyle';
s.metadata.attrs.course         = 'LCM';
s.metadata.attrs.date           = '2026-09-18';
s.metadata.attrs.result_time_s  = duration_s;

s.race.splits.split_distance_m  = [50, 100];
s.race.splits.split_time_s      = [25.10, 27.21];
s.race.splits.cumulative_time_s = [25.10, 52.31];

s.kinematics.time         = t;
s.kinematics.joint_names  = jointNames;
s.kinematics.position     = position;
s.kinematics.attrs.sample_rate_hz     = fps;
s.kinematics.attrs.coordinate_system  = 'pool: x=length, y=width, z=vertical(up), origin=start wall, right-handed';
s.kinematics.attrs.units              = 'meters, seconds';

%% ---- write ----
writeSwimFile('demo_race_matlab.swim', s);

%% ---- read back ----
r = readSwimFile('demo_race_matlab.swim');
fprintf('Athlete: %s\n', r.metadata.attrs.athlete_name);
fprintf('Event: %s | Result: %.2f s\n', r.metadata.attrs.event, r.metadata.attrs.result_time_s);
fprintf('Kinematics joints: %s\n', strjoin(r.kinematics.joint_names, ', '));
fprintf('Position array size: %s\n', mat2str(size(r.kinematics.position)));

% You can also open a file that was written by the Python library
% (swim_format.py) directly:
%   r2 = readSwimFile('example_race.swim');
%   plot(r2.kinematics.time, squeeze(r2.kinematics.position(:,1,1)));
%   xlabel('time (s)'); ylabel('hip x position (m)');
