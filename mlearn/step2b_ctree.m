

%% Constants
FEATURE_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features_boold.mat";
TARGET_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets_boold.mat";
% FEATURE_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features_boold.xlsx";
% TARGET_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets_boold.xlsx";


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

mdlFront = fitctree(features(train_ind,:), targets(train_ind,:).front, 'MaxNumSplits', 15);
view(mdlFront,'Mode','graph')

yHatTest = predict(mdlFront, features(test_ind,:));
testAccur = sum(yHatTest == targets(test_ind,:).front)/double(total_testing_samples);

yHatTrain = predict(mdlFront, features(train_ind,:));
trainingAccur = sum(yHatTrain == targets(train_ind,:).front)/double(total_training_samples);

fprintf("Front training error: %f\n", trainingAccur);
fprintf("Front test error: %f\n", testAccur);

% Plot variable importance
figure
bar(predictorImportance(mdlFront))

title("Predictor importance for Pareto optimality")
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTick = 1:numel(mdlFront.PredictorNames);
h.XTickLabel = mdlFront.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';


%% Fit a model for yield


mdlYield = fitctree(features(train_ind,:), targets(train_ind,:).yield, 'MaxNumSplits', 15);
view(mdlYield,'Mode','graph')

yHatTest = predict(mdlYield, features(test_ind,:));
testAccur = sum(yHatTest == targets(test_ind,:).yield)/double(total_testing_samples);

yHatTrain = predict(mdlYield, features(train_ind,:));
trainingAccur = sum(yHatTrain == targets(train_ind,:).yield)/double(total_training_samples);

fprintf("Yield training error: %f\n", trainingAccur);
fprintf("Yield test error: %f\n", testAccur);

% Plot variable importance
figure
bar(predictorImportance(mdlYield))

title("Predictor importance for yield")
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTick = 1:numel(mdlYield.PredictorNames);
h.XTickLabel = mdlYield.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';

%% Fit a leaching model
mdlLeaching = fitctree(features(train_ind,:), targets(train_ind,:).leaching, 'MaxNumSplits', 15);
view(mdlLeaching,'Mode','graph')

yHatTest = predict(mdlLeaching, features(test_ind,:));
testAccur = sum(yHatTest == targets(test_ind,:).leaching)/double(total_testing_samples);

yHatTrain = predict(mdlLeaching, features(train_ind,:));
trainingAccur = sum(yHatTrain == targets(train_ind,:).leaching)/double(total_training_samples);

fprintf("Leaching training error: %f\n", trainingAccur);
fprintf("Leaching error: %f\n", testAccur);

% Plot variable importance
figure
bar(predictorImportance(mdlLeaching))

title("Predictor importance for leaching")
ylabel('Estimates');
xlabel('Predictors');
h = gca;
h.XTick = 1:numel(mdlLeaching.PredictorNames);
h.XTickLabel = mdlLeaching.PredictorNames;
h.XTickLabelRotation = 45;
h.TickLabelInterpreter = 'none';

