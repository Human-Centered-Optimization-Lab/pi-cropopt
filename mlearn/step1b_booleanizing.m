

%% Constants
FEATURE_TABLE_INPUT_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features.xlsx";
TARGET_TABLE_INPUT_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets.xlsx";
FEATURE_TABLE_OUTPUT_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features_boold.mat";
TARGET_TABLE_OUTPUT_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets_boold.mat";

% FEATURE_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";


%% Load data

if ~exist("features", 'var')
    features = readtable(FEATURE_TABLE_INPUT_PATH);
end

if ~exist("targets_raw", 'var')
    targets_raw = readtable(TARGET_TABLE_INPUT_PATH);
end
targets = targets_raw;



%% Booleanize (booleanaise?)

% Make front a boolean
targets.front = targets_raw.front == 0;
cp = classperf(targets.front);

% Make yield a boolean
sortedYield = sort(targets_raw.yield_);
upperQuartile = sortedYield(uint32(length(sortedYield)*.75));
targets.yield = targets_raw.yield_ > upperQuartile;

% Make leaching a boolean
sortedLeaching = sort(targets_raw.leaching);
lowerQuartile = sortedLeaching(uint32(length(sortedLeaching)*.25));
targets.leaching = targets_raw.leaching < 10;

save(FEATURE_TABLE_OUTPUT_PATH, "features")
save(TARGET_TABLE_OUTPUT_PATH, "targets")


