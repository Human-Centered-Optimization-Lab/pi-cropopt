%% Constants

% FEATURE_TABLE_PATH = "/mnt/nas/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/mnt/nas/kroppian/agovization_results/mlearning/targets.xlsx";

FEATURE_TABLE_PATH = "/Volumes/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
TARGET_TABLE_PATH = "/Volumes/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";

%% Load data
if ~exist("features", 'var')
    features = readtable(FEATURE_TABLE_PATH);
end

if ~exist("targets", 'var')
    targets = readtable(TARGET_TABLE_PATH);
end

%% Extract optimal indices

optimal_by_front = targets.front == 0;


feature_names = {'total_irrigation', 'application_count'};

pretty_feature_names = {'total irrigation', 'application count'};


%% Extract and plot histogram of features
for f=1:numel(feature_names)
    
    figure 
    
    feature = feature_names{f};
    pretty_feature = pretty_feature_names{f};

    total_opt_irr = features(optimal_by_front, :).(feature);

    subplot(2, 1,1);
    histogram(total_opt_irr);

    title("Distribution of optimal solutiosn for total " + pretty_feature);

    subplot(2,1,2);
    histogram(rmoutliers(total_opt_irr));
    title("Distribution of optimal solutiosn for " + pretty_feature + " (without outliers)");
    
    
end

%% Plot relationships 

feature_names = {'total_irrigation'};

for f=1:numel(feature_names)
    
    figure 
    
    feature = feature_names{f};
    pretty_feature = pretty_feature_names{f};

    independentVar = features(optimal_by_front, :).(feature);
    yield = targets(optimal_by_front, :).yield_;

    scatter(independentVar, yield);
    
    
end
