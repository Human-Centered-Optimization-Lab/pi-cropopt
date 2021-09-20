

%% Constants



%% Load data

if ~exist("features", 'var')
    features = readtable("Z:\Gilgamesh\kroppian\agovization_results\mlearning\features.xlsx");
end

if ~exist("targets_raw", 'var')
    targets_raw = readtable("Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets.xlsx");
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
% For the optimization and plots, the objective function is 
% log(1 + cross-validation loss) for regression and the misclassification 
% rate for classification.

% ------------------
% params = hyperparameters('fitctree',features, targets.front);
% params(1).Range = [1,20];
% 
% res = fitctree(features, targets.front, 'OptimizeHyperparameters',params );
% 
% trainingOptions = res.ModelParameters;
% ------------------

% front
%mdl20 = fitctree(features, targets.front, 'MaxNumSplits', 20, 'CrossVal', 'on');

% yield
mdl20 = fitctree(features, targets.yield, 'MaxNumSplits', 15, 'CrossVal', 'on');
view(mdl20.Trained{1},'Mode','graph')

% leaching

mdl20 = fitctree(features, targets.leaching, 'MaxNumSplits', 10, 'CrossVal', 'on');
view(mdl20.Trained{1},'Mode','graph')




%rs = evaluateTraining(treeModel)

%% Functions

% function rs = evaluateTraining(model, x, y_obs)
%         
% end
