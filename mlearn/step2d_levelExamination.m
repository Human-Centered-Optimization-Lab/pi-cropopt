
%% Constants
FEATURE_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features_boold.mat";
TARGET_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets_boold.mat";
% FEATURE_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";



%% Load data
load(FEATURE_TABLE_PATH)
load(TARGET_TABLE_PATH)


%% Determine levels of predictors 
% (largely from
% https://www.mathworks.com/help/stats/select-predictors-for-random-forests.html)

% I'm pretty sure these are functionally the same
%countLevels = @(x)numel(categories(categorical(x)));
countLevels = @(x)numel(unique(x));
numLevels = varfun(countLevels,features,'OutputFormat','uniform');

%% Plot!

figure
bar(numLevels)
title('Number of Levels Among Predictors')
xlabel('Predictor variable')
ylabel('Number of levels')
h = gca;

h.XTick = 1:numel(features.Properties.VariableNames);

h.XTickLabel = features.Properties.VariableNames(1:end-1);
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';

