function [editedFeatures] = cleanUpFeatures(features)
%CLEANUPFEATURES Summary of this function goes here
%   Detailed explanation goes here

editedFeatures = features;

editedFeatures.total_wat_during_v6 = features.total_irr_during_v6 + features.total_precip_during_v6;
editedFeatures.total_wat_during_v7 = features.total_irr_during_v7 + features.total_precip_during_v7;
editedFeatures.total_wat_during_v8 = features.total_irr_during_v8 + features.total_precip_during_v8;
editedFeatures.total_wat_during_v9 = features.total_irr_during_v9 + features.total_precip_during_v9;
editedFeatures.total_wat_during_v10 = features.total_irr_during_v10 + features.total_precip_during_v10;
editedFeatures.total_wat_during_v11 = features.total_irr_during_v11 + features.total_precip_during_v11;
editedFeatures.total_wat_during_v12 = features.total_irr_during_v12 + features.total_precip_during_v12;
editedFeatures.total_wat_during_v13 = features.total_irr_during_v13 + features.total_precip_during_v13;
editedFeatures.total_wat_during_v14 = features.total_irr_during_v14 + features.total_precip_during_v14;
editedFeatures.total_wat_during_R1 = features.total_irr_during_R1 + features.total_precip_during_R1;
editedFeatures.total_wat_during_R2 = features.total_irr_during_R2 + features.total_precip_during_R2;
editedFeatures.total_wat_during_R3 = features.total_irr_during_R3 + features.total_precip_during_R3;
editedFeatures.total_wat_during_R4 = features.total_irr_during_R4 + features.total_precip_during_R4;

editedFeatures.freq_precip_during_v8   = [];
editedFeatures.freq_precip_during_v9   = [];
editedFeatures.freq_precip_during_v10  = [];
editedFeatures.freq_precip_during_v11  = [];
editedFeatures.freq_precip_during_v12  = [];
editedFeatures.freq_precip_during_v13  = [];
editedFeatures.freq_precip_during_v14  = [];
editedFeatures.freq_precip_during_R1   = []; 
editedFeatures.freq_precip_during_R2   = []; 
editedFeatures.freq_precip_during_R3   = []; 
editedFeatures.freq_precip_during_R4   = []; 

editedFeatures.freq_irr_during_v6   = [];
editedFeatures.freq_irr_during_v7   = [];
editedFeatures.freq_irr_during_v8   = [];
editedFeatures.freq_irr_during_v9   = [];
editedFeatures.freq_irr_during_v10  = [];
editedFeatures.freq_irr_during_v11  = [];
editedFeatures.freq_irr_during_v12  = [];
editedFeatures.freq_irr_during_v13  = [];
editedFeatures.freq_irr_during_v14  = [];
editedFeatures.freq_irr_during_R1   = []; 
editedFeatures.freq_irr_during_R2   = []; 
editedFeatures.freq_irr_during_R3   = []; 
editedFeatures.freq_irr_during_R4   = []; 

editedFeatures.total_irr_during_v6   = [];
editedFeatures.total_irr_during_v7   = [];
editedFeatures.total_irr_during_v8   = [];
editedFeatures.total_irr_during_v9   = [];
editedFeatures.total_irr_during_v10  = [];
editedFeatures.total_irr_during_v11  = [];
editedFeatures.total_irr_during_v12  = [];
editedFeatures.total_irr_during_v13  = [];
editedFeatures.total_irr_during_v14  = [];
editedFeatures.total_irr_during_R1   = []; 
editedFeatures.total_irr_during_R2   = []; 
editedFeatures.total_irr_during_R3   = []; 
editedFeatures.total_irr_during_R4   = []; 

editedFeatures.total_precip_during_v6   = [];
editedFeatures.total_precip_during_v7   = [];
editedFeatures.total_precip_during_v8   = [];
editedFeatures.total_precip_during_v9   = [];
editedFeatures.total_precip_during_v10  = [];
editedFeatures.total_precip_during_v11  = [];
editedFeatures.total_precip_during_v12  = [];
editedFeatures.total_precip_during_v13  = [];
editedFeatures.total_precip_during_v14  = [];
editedFeatures.total_precip_during_R1   = []; 
editedFeatures.total_precip_during_R2   = []; 
editedFeatures.total_precip_during_R3   = []; 
editedFeatures.total_precip_during_R4   = []; 

editedFeatures.number_of_precipitation_events = [];



end

