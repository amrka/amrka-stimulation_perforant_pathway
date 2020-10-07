#!/bin/bash

#combine the copes from the 2nd level for 10,20 and 40 Hz



cd /media/amr/Amr_4TB/Work/stimulation/Data/

mkdir /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/timeseries
mkdir /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/timeseries
mkdir /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/timeseries

for folder in *;do

	if [[ -d $folder ]];then
		cp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_40Hz/stimulation_2nd_level_40Hz/_subject_id_${folder}/mean_timeseries_2nd_level/mean_ts_40Hz_2nd_level.txt \
		/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/timeseries/percent_change_40Hz_${folder}.txt



		cp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_20Hz/stimulation_2nd_level_20Hz/_subject_id_${folder}/mean_timeseries_2nd_level/mean_ts_20Hz_2nd_level.txt \
		/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/timeseries/percent_change_20Hz_${folder}.txt


		cp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_10Hz/stimulation_2nd_level_10Hz/_subject_id_${folder}/mean_timeseries_2nd_level/mean_ts_10Hz_2nd_level.txt \
		/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/timeseries/percent_change_10Hz_${folder}.txt
	fi



done

#======================================================================================================================

# change file names to contain gp name


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name_perforant.py \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/timeseries -7 -4


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name_perforant.py \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/timeseries -7 -4


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name_perforant.py \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/timeseries -7 -4
