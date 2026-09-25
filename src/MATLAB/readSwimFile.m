function s = readSwimFile(filename)
%READSWIMFILE Read a .swim (HDF5) race/biomechanics file into a struct.
%
%   S = READSWIMFILE(FILENAME) reads every group, dataset, and attribute
%   in the .swim file at FILENAME and returns a nested MATLAB struct
%   mirroring the HDF5 group hierarchy described in
%   SWIM_FORMAT_SPEC.md.
%
%   Layout of the returned struct:
%     s.attrs.<name>              root-level attributes (format, format_version, ...)
%     s.metadata.<field>          athlete/race metadata (all attributes)
%     s.kinematics.time           (F x 1) double
%     s.kinematics.joint_names    {J x 1} cell array of char
%     s.kinematics.position       (F x J x 3) double
%     s.kinematics.attrs.<name>   group attributes (sample_rate_hz, ...)
%     s.race.splits.split_time_s  ...
%     s.race.laps.lap_time_s      ...
%     s.stroke_metrics.<field>    ...
%     s.sensors.imu_<location>.time / accel / gyro / mag
%     s.forces.time / force_n
%     s.video.sync_timestamps, s.video.attrs.frame_rate_hz
%
%   Any group/dataset present in the file is included; anything absent
%   is simply not a field of S. Variable-length HDF5 strings come back
%   as MATLAB cell arrays of char row vectors (or a single char array
%   for scalar strings).
%
%   Example:
%       s = readSwimFile('example_race.swim');
%       disp(s.metadata.athlete_name)
%       plot(s.kinematics.time, squeeze(s.kinematics.position(:,1,1)))
%
%   NOTE on multi-dimensional arrays: HDF5 is unambiguous about a
%   dataset's shape, but Python/NumPy (row-major) and MATLAB
%   (column-major) can present the same on-disk array with dimensions
%   in different orders. 1-D datasets are unaffected. For 2+D datasets
%   (position, velocity, accel, gyro, ...), check size(...) against the
%   expected shape (e.g. [nFrames, nJoints, 3]); if axes appear
%   reversed, use permute(x, ndims(x):-1:1) to restore the expected
%   order. See SWIM_FORMAT_SPEC.md section 5.
%
%   See also WRITESWIMFILE, H5INFO, H5READ.

    if ~isfile(filename)
        error('readSwimFile:fileNotFound', 'File not found: %s', filename);
    end

    info = h5info(filename);

    s = struct();
    s.attrs = attrsToStruct(info.Attributes);

    for i = 1:numel(info.Groups)
        grp = info.Groups(i);
        [~, grpName] = fileparts(grp.Name);   % e.g. '/kinematics' -> 'kinematics'
        fieldName = sanitizeFieldName(grpName);
        s.(fieldName) = readGroup(filename, grp);
    end
end

% ------------------------------------------------------------------------
function out = readGroup(filename, grpInfo)
% Recursively read one HDF5 group (datasets, attributes, subgroups).
    out = struct();

    % Attributes on this group
    if ~isempty(grpInfo.Attributes)
        out.attrs = attrsToStruct(grpInfo.Attributes);
    end

    % Datasets directly in this group
    for i = 1:numel(grpInfo.Datasets)
        ds = grpInfo.Datasets(i);
        fullPath = [grpInfo.Name '/' ds.Name];
        raw = h5read(filename, fullPath);
        out.(sanitizeFieldName(ds.Name)) = postprocessDataset(raw, ds);
    end

    % Subgroups (recurse) -- e.g. race/splits, race/laps, sensors/imu_*
    for i = 1:numel(grpInfo.Groups)
        subGrp = grpInfo.Groups(i);
        [~, subName] = fileparts(subGrp.Name);
        out.(sanitizeFieldName(subName)) = readGroup(filename, subGrp);
    end
end

% ------------------------------------------------------------------------
function val = postprocessDataset(raw, dsInfo)
% Convert HDF5 variable-length strings (read as cell arrays already by
% h5read) into a tidy cell array; convert numeric arrays so that the
% first (fastest-varying-in-file) dimension in MATLAB matches the
% leading dimension as stored (h5read already returns dims in the same
% order HDF5 stores them, i.e. matches Python's row-major shape when
% you read shape(1) as MATLAB dim 1).
    isCharLike = false;
    try
        if isa(dsInfo.Datatype, 'struct') && isfield(dsInfo.Datatype, 'Class')
            isCharLike = strcmpi(dsInfo.Datatype.Class, 'H5T_STRING');
        end
    catch
        % older MATLAB h5info datatype representation; fall back to
        % runtime type check below
    end

    if isCharLike || iscell(raw) || ischar(raw)
        if iscell(raw)
            val = cellfun(@(c) char(c), raw, 'UniformOutput', false);
        else
            val = char(raw);
        end
    else
        val = raw;
    end
end

% ------------------------------------------------------------------------
function s = attrsToStruct(attrArray)
    s = struct();
    for i = 1:numel(attrArray)
        name = sanitizeFieldName(attrArray(i).Name);
        value = attrArray(i).Value;
        if iscell(value) && numel(value) == 1
            value = value{1};
        end
        if ischar(value) || (iscell(value) && all(cellfun(@ischar, value)))
            s.(name) = value;
        else
            s.(name) = value;
        end
    end
end

% ------------------------------------------------------------------------
function f = sanitizeFieldName(name)
% MATLAB struct fields can't start with a digit or contain some
% characters; HDF5 group/dataset names in this schema are already
% valid identifiers, but guard against edge cases.
    f = regexprep(name, '[^a-zA-Z0-9_]', '_');
    if isempty(f) || ~isletter(f(1))
        f = ['x_' f];
    end
end
