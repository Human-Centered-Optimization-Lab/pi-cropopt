

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
total_samples = size(targets, 1);



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

%% split data into training and testing subsets

% Figure the number of training and testing samples
train_ind = zeros(total_samples,1);
total_training_samples = uint32(total_samples*0.8);
total_testing_samples = total_samples - total_training_samples;

% Randomly determine location of training indices
train_ind(randperm(total_samples, total_training_samples), 1) = 1;
test_ind = ~train_ind;

train_ind = find(train_ind);
test_ind = find(test_ind);

% Report on preportions of fronts 
fprintf("Total proportion of yield: %f\n", sum(targets.yield == 1)/total_samples);

fprintf("Test proportion of yield: %f\n", sum(targets(test_ind,:).yield == 1)/double(total_testing_samples));

fprintf("Training proportion of yield: %f\n", sum(targets(train_ind,:).yield == 1)/double(total_training_samples));


%% fit the tree for various objectives

% front
%mdlFront = fitctree(features, targets.front, 'MaxNumSplits', 20, 'CrossVal', 'on');

% yield
mdlYield = fitctree(features(train_ind,:), targets(train_ind,:).yield, 'MaxNumSplits', 15);
view(mdlYield,'Mode','graph')

yHatTest = predict(mdlYield, features(test_ind,:));
testAccur = sum(yHatTest == targets(test_ind,:).yield)/double(total_testing_samples);

yHatTrain = predict(mdlYield, features(train_ind,:));
trainingAccur = sum(yHatTrain == targets(train_ind,:).yield)/double(total_training_samples);


fprintf("Training error: %f\n", trainingAccur);
fprintf("Test error: %f\n", testAccur);



% leaching
% mdlLeaching = fitctree(features, targets.leaching, 'MaxNumSplits', 10, 'CrossVal', 'on');
% view(mdlLeaching.Trained{1},'Mode','graph')



%% Functions

% function rs = evaluateTraining(model, x, y_obs)
%         
% end
