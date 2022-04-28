


% FEATURE_TABLE_PATH = "/mnt/nas/kroppian/agovization_results/mlearning/features.xlsx";
% TARGET_TABLE_PATH = "/mnt/nas/kroppian/agovization_results/mlearning/targets.xlsx";
% 
FEATURE_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.xlsx";
TARGET_TABLE_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.xlsx";
TARGET_TABLE_BOOLD_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets_boold.mat";

% FEATURE_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\features.xlsx";
% TARGET_TABLE_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets.xlsx";
% TARGET_TABLE_BOOLD_PATH = "Z:\Gilgamesh\kroppian\agovization_results\mlearning\targets_boold.mat";


%% Load data
if ~exist("features", 'var')
    features = readtable(FEATURE_TABLE_PATH);
end

if ~exist("targets", 'var')
    targets = readtable(TARGET_TABLE_PATH);
end

targets_boold = load(TARGET_TABLE_BOOLD_PATH);
targets_boold = targets_boold.targets;


optimal_by_front = targets.front == 0;

features_po = features(optimal_by_front, :);

%% Yield and R1 R2

max_yield = max(targets.yield_);
yields = targets(optimal_by_front,:).yield_;

c = int64((yields ./ max_yield)*1000);

scatter(features_po.total_irr_during_R1, features_po.total_irr_during_R4, 50, c, 'filled');
colormap(gca,'parula')

%% Leaching and R1 R2
figure
max_leach = max(targets.leaching);
leachings = targets(optimal_by_front,:).leaching;

c = int64((leachings ./ max_leach)*1000);

scatter(features_po.total_irr_during_R1, features_po.total_irr_during_R4, 50, c, 'filled');
colormap(gca,'parula')


%% Water use and R1 R2

figure
max_irr = max(targets.total_irrigation);
total_irr = targets(optimal_by_front,:).total_irrigation;

c = int64((total_irr ./ max_irr)*1000);

scatter(features_po.total_irr_during_R1, features_po.total_irr_during_R4, 50, c, 'filled');
colormap(gca,'parula')


%% Plot features
feature_names = {'application_count','total_irrigation','minimum_irr','maximum_irr','number_of_precipitation_events','growth_period_of_second_N_app','total_irr_during_v6','total_irr_during_v7','total_irr_during_v8','total_irr_during_v9','total_irr_during_v10','total_irr_during_v11','total_irr_during_v12','total_irr_during_v13','total_irr_during_v14','total_irr_during_R1','total_irr_during_R2','total_irr_during_R3','total_irr_during_R4','total_precip_during_v6','total_precip_during_v7','total_precip_during_v8','total_precip_during_v9','total_precip_during_v10','total_precip_during_v11','total_precip_during_v12','total_precip_during_v13','total_precip_during_v14','total_precip_during_R1','total_precip_during_R2','total_precip_during_R3','total_precip_during_R4','freq_irr_during_v6','freq_irr_during_v7','freq_irr_during_v8','freq_irr_during_v9','freq_irr_during_v10','freq_irr_during_v11','freq_irr_during_v12','freq_irr_during_v13','freq_irr_during_v14','freq_irr_during_R1','freq_irr_during_R2','freq_irr_during_R3','freq_irr_during_R4','freq_precip_during_v8','freq_precip_during_v9','freq_precip_during_v10','freq_precip_during_v11','freq_precip_during_v12','freq_precip_during_v13','freq_precip_during_v14','freq_precip_during_R1','freq_precip_during_R2','freq_precip_during_R3','freq_precip_during_R4','climate','total_p'};

feat_count = size(feature_names,2);

square_dim = ceil(sqrt(feat_count));
s = 1;
% for f1 = 1:feat_count
%     for f2 = 1:feat_count
%         
%         if f1 > f2
%             continue
%         end
%         
%         fprintf("Plotting %d %d\n", f1, f2);
%         
%         feature1 = feature_names{f1};
%         feature2 = feature_names{f2};
%         
%         x = features(optimal_by_front,:).(feature1);f
%         y = features(optimal_by_front,:).(feature2);
% 
%         subplot(feat_count, feat_count, s);
%         scatter(x,y);
%         
%         s = s + 1;
%         
%         xlabel(feature1);
%         ylabel(feature2);
%         
% %         subplot(feat_count, feat_count, f1 + f2);
% %         scatter(,)
%     
%     end
% end
% 
% 
% 
