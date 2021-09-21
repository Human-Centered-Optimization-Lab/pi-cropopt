

%% Constants
% FEATURE_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features.xlsx";
% TARGET_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets.xlsx";
FEATURE_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
TARGET_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";


%% Load data

if ~exist("features", 'var')
    features = readtable(FEATURE_TABLE_PATH);
end

if ~exist("targets_raw", 'var')
    targets_raw = readtable(TARGET_TABLE_PATH);
end
targets = targets_raw;

%% Make front a boolean
targets.front = targets_raw.front == 0;
cp = classperf(targets.front);

%% Make yield a boolean

sortedYield = sort(targets_raw.yield_);
upperQuartile = sortedYield(uint32(length(sortedYield)*.75));
targets.yield = targets_raw.yield_ > upperQuartile;

%% Make leaching a boolean
sortedLeaching = sort(targets_raw.leaching);
lowerQuartile = sortedLeaching(uint32(length(sortedLeaching)*.25));
targets.leaching = targets_raw.leaching < 10;


%% fit the tree for front

%% front
%mdlFront = fitctree(features, targets.front, 'MaxNumSplits', 20, 'CrossVal', 'on');

%% yield
mdlYield = fitctree(features, targets.yield, 'MaxNumSplits', 15, 'CrossVal', 'on');
view(mdlYield.Trained{1},'Mode','graph')



% leaching
% mdlLeaching = fitctree(features, targets.leaching, 'MaxNumSplits', 10, 'CrossVal', 'on');
% view(mdlLeaching.Trained{1},'Mode','graph')




%rs = evaluateTraining(treeModel)

%% Functions

% function rs = evaluateTraining(model, x, y_obs)
%         
% end
