function writeSwimFile(filename, s)
%WRITESWIMFILE Write a .swim (HDF5) race/biomechanics file from a struct.
%
%   WRITESWIMFILE(FILENAME, S) creates (overwriting if it exists) an
%   HDF5 file at FILENAME following the SWIM schema (see
%   SWIM_FORMAT_SPEC.md), from the nested struct S. S should be built
%   the same way READSWIMFILE returns it:
%
%     s.metadata.attrs.athlete_name  = 'Jane Doe';
%     s.metadata.attrs.event         = '100m Freestyle';
%     s.metadata.attrs.distance_m    = 100;
%     s.metadata.attrs.result_time_s = 52.31;
%
%     s.kinematics.time         = t(:);                 % (F x 1)
%     s.kinematics.joint_names  = {'hip','shoulder_r'};  % {1 x J} cell
%     s.kinematics.position     = position;              % (F x J x 3)
%     s.kinematics.attrs.sample_rate_hz = 100;
%     s.kinematics.attrs.coordinate_system = 'pool: x=length,...';
%
%     s.race.splits.split_distance_m  = [50 100];
%     s.race.splits.split_time_s      = [25.1 27.21];
%     s.race.splits.cumulative_time_s = [25.1 52.31];
%
%     s.sensors.imu_sacrum.time  = t(:);
%     s.sensors.imu_sacrum.accel = accelData;   % (F x 3)
%     s.sensors.imu_sacrum.gyro  = gyroData;    % (F x 3)
%
%     writeSwimFile('race001.swim', s);
%
%   Top-level struct fields become HDF5 groups; a field named 'attrs'
%   inside any (sub)struct is written as HDF5 attributes on that group
%   instead of a dataset -- this is how you store scalar metadata
%   fields (athlete_name, event, sample_rate_hz, ...), matching what
%   READSWIMFILE hands back under the same '.attrs' field. Any other
%   struct field holding a numeric array becomes an HDF5 dataset; a
%   char array or cell array of strings becomes an HDF5 variable-length
%   UTF-8 string dataset (use this only for array-valued string data
%   like joint_names, not for scalar metadata, which belongs in
%   '.attrs').
%
%   See also READSWIMFILE, H5CREATE, H5WRITE, H5WRITEATT.

    if isfile(filename)
        delete(filename);
    end

    % Create the file with a dummy attribute call trick isn't needed --
    % h5create will create the file on first call. Write root attrs via
    % low-level HDF5 API so the file exists even if S has no data yet.
    fid = H5F.create(filename, 'H5F_ACC_TRUNC', 'H5P_DEFAULT', 'H5P_DEFAULT');
    H5F.close(fid);

    rootAttrs = struct('format', 'SWIM', 'format_version', '1.0', ...
                        'created', char(datetime('now','TimeZone','UTC', ...
                            'Format','yyyy-MM-dd''T''HH:mm:ss''Z''')), ...
                        'creator', 'writeSwimFile.m v1.0');
    if isfield(s, 'attrs')
        userAttrs = s.attrs;
        fn = fieldnames(userAttrs);
        for i = 1:numel(fn)
            rootAttrs.(fn{i}) = userAttrs.(fn{i});
        end
    end
    writeAttrsToGroup(filename, '/', rootAttrs);

    % Ensure /metadata always exists even if empty
    if ~isfield(s, 'metadata')
        s.metadata = struct();
    end

    topFields = fieldnames(s);
    for i = 1:numel(topFields)
        name = topFields{i};
        if strcmp(name, 'attrs')
            continue  % already handled as root attrs
        end
        writeGroup(filename, ['/' name], s.(name));
    end
end

% ------------------------------------------------------------------------
function writeGroup(filename, h5path, groupStruct)
% Recursively write a struct as an HDF5 group at h5path.
    createGroupIfNeeded(filename, h5path);

    if ~isstruct(groupStruct) || isempty(fieldnames(groupStruct))
        return
    end

    fn = fieldnames(groupStruct);
    for i = 1:numel(fn)
        name = fn{i};
        value = groupStruct.(name);

        if strcmp(name, 'attrs')
            writeAttrsToGroup(filename, h5path, value);
            continue
        end

        if isstruct(value)
            % Subgroup (e.g. race.splits, sensors.imu_sacrum)
            writeGroup(filename, [h5path '/' name], value);
        elseif iscell(value) || (ischar(value) && size(value,1) <= 1)
            % String / cell-of-strings dataset (e.g. joint_names)
            writeStringDataset(filename, [h5path '/' name], value);
        elseif isnumeric(value) || islogical(value)
            writeNumericDataset(filename, [h5path '/' name], double(value));
        else
            warning('writeSwimFile:skip', ...
                'Skipping field %s%s (unsupported type %s)', ...
                h5path, name, class(value));
        end
    end
end

% ------------------------------------------------------------------------
function createGroupIfNeeded(filename, h5path)
    if strcmp(h5path, '/')
        return
    end
    fid = H5F.open(filename, 'H5F_ACC_RDWR', 'H5P_DEFAULT');
    try
        gid = H5G.open(fid, h5path);
        H5G.close(gid);
    catch
        gid = H5G.create(fid, h5path, 'H5P_DEFAULT', 'H5P_DEFAULT', 'H5P_DEFAULT');
        H5G.close(gid);
    end
    H5F.close(fid);
end

% ------------------------------------------------------------------------
function writeNumericDataset(filename, h5path, data)
% Write a numeric array, preserving orientation as given (F x J x 3 etc).
    if isvector(data)
        data = data(:);   % store 1-D vectors as column, matches Python's (N,)
        sz = numel(data);
    else
        sz = size(data);
    end
    h5create(filename, h5path, sz, 'Datatype', 'double');
    h5write(filename, h5path, data);
end

% ------------------------------------------------------------------------
function writeStringDataset(filename, h5path, value)
% Write char array or cell array of char as a variable-length UTF-8
% string dataset (matches h5py.string_dtype()).
    if ischar(value)
        strs = {value};
    else
        strs = value;
    end
    strs = cellfun(@char, strs, 'UniformOutput', false);

    fid = H5F.open(filename, 'H5F_ACC_RDWR', 'H5P_DEFAULT');
    typeId = H5T.copy('H5T_C_S1');
    H5T.set_size(typeId, 'H5T_VARIABLE');
    H5T.set_cset(typeId, H5ML.get_constant_value('H5T_CSET_UTF8'));

    dims = numel(strs);
    spaceId = H5S.create_simple(1, dims, dims);
    dsetId = H5D.create(fid, h5path, typeId, spaceId, 'H5P_DEFAULT');
    H5D.write(dsetId, typeId, 'H5S_ALL', 'H5S_ALL', 'H5P_DEFAULT', strs(:));

    H5D.close(dsetId);
    H5S.close(spaceId);
    H5T.close(typeId);
    H5F.close(fid);
end

% ------------------------------------------------------------------------
function writeAttrsToGroup(filename, h5path, attrStruct)
    if ~isstruct(attrStruct)
        return
    end
    fn = fieldnames(attrStruct);
    for i = 1:numel(fn)
        h5writeatt(filename, h5path, fn{i}, attrStruct.(fn{i}));
    end
end
