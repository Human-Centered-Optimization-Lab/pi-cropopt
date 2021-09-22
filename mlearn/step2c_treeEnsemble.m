

%% Constants
FEATURE_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features_boold.mat";
TARGET_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets_boold.mat";
% FEATURE_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";

toNum = @(x)str2num(x);

%% Load data
load(FEATURE_TABLE_PATH)
load(TARGET_TABLE_PATH)


%% split data into training and testing subsets
total_samples = size(targets, 1);

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


%% front
if ~exist("mdlFrontEnsemb", 'var')
    mdlFrontEnsemb = TreeBagger(100 ,features(train_ind,:), targets(train_ind,:).front, 'OOBPredictorImportance', 'on', 'Method', 'classification');
else
    disp('Front model results already exists. Skipping training');
end

yHatTest = predict(mdlFrontEnsemb, features(test_ind,:));
% Convert cell array to numerical matrix 
yHatTest = cell2mat(yHatTest) == '1';
testAccur = sum(yHatTest == targets(test_ind,:).front)/double(total_testing_samples);

yHatTrain = predict(mdlFrontEnsemb, features(train_ind,:));
% Convert cell array to numerical matrix 
yHatTrain = cell2mat(yHatTrain) == '1';
trainingAccur = sum(yHatTrain == targets(train_ind,:).front)/double(total_training_samples);

fprintf("Front training error: %f\n", trainingAccur);
fprintf("Front test error: %f\n", testAccur);

% Plot variable importance
figure
bar(mdlFrontEnsemb.OOBPermutedPredictorDeltaError)

title("Predictor importance for Pareto optimality")
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTick = 1:numel(mdlFrontEnsemb.PredictorNames);
h.XTickLabel = mdlFrontEnsemb.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';


%% Fit a model for yield
if ~exist("mdlYieldEnsemb", 'var')
    mdlYieldEnsemb = TreeBagger(100 ,features(train_ind,:), targets(train_ind,:).yield, 'OOBPredictorImportance', 'on', 'Method', 'classification');
else
    disp('Yield model results already exists. Skipping training');
end

yHatTest = predict(mdlYieldEnsemb, features(test_ind,:));
% Convert cell array to numerical matrix 
yHatTest = cell2mat(yHatTest) == '1';

testAccur = sum(yHatTest == targets(test_ind,:).yield)/double(total_testing_samples);

yHatTrain = predict(mdlYieldEnsemb, features(train_ind,:));
yHatTrain = cell2mat(yHatTrain) == '1';
trainingAccur = sum(yHatTrain == targets(train_ind,:).yield)/double(total_training_samples);

fprintf("Yield training error: %f\n", trainingAccur);
fprintf("Yield test error: %f\n", testAccur);

% Plot variable importance
figure
bar(mdlYieldEnsemb.OOBPermutedPredictorDeltaError)

title("Predictor importance for yield")
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTick = 1:numel(mdlYieldEnsemb.PredictorNames);
h.XTickLabel = mdlYieldEnsemb.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';

%% Fit a leaching model
if ~exist("mdlLeachingEnsemb", 'var')
    mdlLeachingEnsemb = TreeBagger(100 ,features(train_ind,:), targets(train_ind,:).leaching, 'OOBPredictorImportance', 'on', 'Method', 'classification');
else
    disp('Leaching model results already exists. Skipping training');
end

yHatTest = predict(mdlLeachingEnsemb, features(test_ind,:));
% Convert cell array to numerical matrix 
yHatTest = cell2mat(yHatTest) == '1';

testAccur = sum(yHatTest == targets(test_ind,:).leaching)/double(total_testing_samples);

yHatTrain = predict(mdlLeachingEnsemb, features(train_ind,:));
yHatTrain = cell2mat(yHatTrain) == '1';
trainingAccur = sum(yHatTrain == targets(train_ind,:).leaching)/double(total_training_samples);

fprintf("Leaching training error: %f\n", trainingAccur);
fprintf("Leaching error: %f\n", testAccur);

% Plot variable importance
figure
bar(mdlLeachingEnsemb.OOBPermutedPredictorDeltaError)

title("Predictor importance for leaching")
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTick = 1:numel(mdlLeachingEnsemb.PredictorNames);
h.XTickLabel = mdlLeachingEnsemb.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';

%% References
% https://www.mathworks.com/help/stats/ensemble-algorithms.html#bsxabwd
% Permutated variable delta error 
% https://stackoverflow.com/questions/31555265/what-is-permutedvardeltaerror-in-random-forest
