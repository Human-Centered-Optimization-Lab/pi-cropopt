%% Constants

% FEATURE_TABLE_PATH = "/mnt/nas/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/mnt/nas/kroppian/agovization_results/mlearning/targets.xlsx";
% 
% FEATURE_TABLE_PATH = "/Volumes/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/Volumes/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";

FEATURE_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features.xlsx";
TARGET_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets.xlsx";
TARGET_TABLE_BOOLD_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets_boold.mat";


%% Load data
if ~exist("features", 'var')
    features = readtable(FEATURE_TABLE_PATH);
end

if ~exist("targets", 'var')
    targets = readtable(TARGET_TABLE_PATH);
end

targets_boold = load(TARGET_TABLE_BOOLD_PATH);
targets_boold = targets_boold.targets;

%% Extract optimal indices

optimal_by_front = targets.front == 0;


feature_names = {'total_irrigation', 'application_count', 'growth_period_of_second_N_app'};

pretty_feature_names = {'total irrigation', 'application count', 'growth period of second N app'};
pretty_target_names = {'Yield', 'Leaching'};


%% Extract and plot histogram of features
for f=1:numel(feature_names)
    
    figure 
    
    feature = feature_names{f};
    pretty_feature = pretty_feature_names{f};

    total_opt_feat = features(optimal_by_front & targets_boold.yield, :).(feature);

    subplot(2, 1,1);
    histogram(total_opt_feat);
    xlabel(pretty_feature);
    ylabel("Frequency");
    
    title("Distribution of optimal solutions for total " + pretty_feature);

    subplot(2,1,2);
    histogram(rmoutliers(total_opt_feat));
    title("Distribution of optimal solutions for " + pretty_feature + " (without outliers)");
    xlabel(pretty_feature);
    ylabel("Frequency");
    
end

%% Plot relationships 

feature_names = {'total_irrigation', 'application_count', 'growth_period_of_second_N_app'};
pretty_feature_names = {'total irrigation', 'application count', 'growth period of second N app'};

targert_names = {'yield_', 'leaching'};


for f=1:numel(feature_names)
    
    for t=1:numel(targert_names)

    
        figure 
        
        target = targert_names{t};
        pretty_target = pretty_target_names{t};
        
        feature = feature_names{f};
        pretty_feature = pretty_feature_names{f};

        dry_mask = features.climate == 0;
        normal_mask = features.climate == 1;
        wet_mask = features.climate == 2;

%         dry_mask = dry_mask & targets_boold.yield;
%         normal_mask = normal_mask & targets_boold.yield;
%         wet_mask = wet_mask & targets_boold.yield;
        
        
        % Plot for dry, normal, and wet years
        independentVar = features(dry_mask & optimal_by_front, :).(feature);
        yield = targets(dry_mask & optimal_by_front, :).(target);
        scatter(independentVar, yield);

        hold on

        independentVar = features(normal_mask & optimal_by_front, :).(feature);
        yield = targets(normal_mask & optimal_by_front, :).(target);
        scatter(independentVar, yield);

        hold on

        independentVar = features(wet_mask & optimal_by_front, :).(feature);
        yield = targets(wet_mask & optimal_by_front, :).(target);
        scatter(independentVar, yield);

        xlabel(pretty_feature);
        ylabel(pretty_target)
        legend("Dry year", "Normal year", "Wet year");
        title("Optimal solutions across all climatology");
    
    end
    
end
