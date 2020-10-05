#!/bin/bash

#combine the copes from the 2nd level for 10,20 and 40 Hz



mkdir -p /home/in/aeed/Work/stimulation/stimulation_3rd_level/{10Hz,20Hz,40Hz}

cd /home/in/aeed/Work/stimulation/Data/


for folder in *;do

	imcp /home/in/aeed/Work/stimulation/Stimulation_2nd_level_WorkingDir_40Hz/stimulation_2nd_level_40Hz/_subject_id_${folder}/cope1_2ndlevel_2_template/cope1_2ndlevel_2_template_brain.nii.gz \
	/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/cope1_${folder}

	imcp /home/in/aeed/Work/stimulation/Stimulation_2nd_level_WorkingDir_40Hz/stimulation_2nd_level_40Hz/_subject_id_${folder}/varcope1_2ndlevel_2_template/varcope1_2ndlevel_2_template_brain.nii.gz \
	/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_${folder}



	imcp /home/in/aeed/Work/stimulation/Stimulation_2nd_level_WorkingDir_20Hz/stimulation_2nd_level_20Hz/_subject_id_${folder}/cope1_2ndlevel_2_template/cope1_2ndlevel_2_template_brain.nii.gz \
	/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/cope1_${folder}

	imcp /home/in/aeed/Work/stimulation/Stimulation_2nd_level_WorkingDir_20Hz/stimulation_2nd_level_20Hz/_subject_id_${folder}/varcope1_2ndlevel_2_template/varcope1_2ndlevel_2_template_brain.nii.gz \
	/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_${folder}



	imcp /home/in/aeed/Work/stimulation/Stimulation_2nd_level_WorkingDir_10Hz/stimulation_2nd_level_10Hz/_subject_id_${folder}/cope1_2ndlevel_2_template/cope1_2ndlevel_2_template_brain.nii.gz \
	/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/cope1_${folder}

	imcp /home/in/aeed/Work/stimulation/Stimulation_2nd_level_WorkingDir_10Hz/stimulation_2nd_level_10Hz/_subject_id_${folder}/varcope1_2ndlevel_2_template/varcope1_2ndlevel_2_template_brain.nii.gz \
	/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_${folder}



done

#======================================================================================================================

change file names to contain gp name


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name_perforant.py \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz -10 -7


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name_perforant.py \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz -10 -7


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name_perforant.py \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz -10 -7



#======================================================================================================================
#merge copes and varcopes for each frequency seperately


fslmerge -t /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii.gz \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/*_cope1_*.nii.gz


gunzip /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii.gz

fslmerge -t /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_10Hz.nii.gz \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/*_varcope1_*.nii.gz


gunzip /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_10Hz.nii.gz



#======================================================================================================================

fslmerge -t /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii.gz \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/*_cope1_*.nii.gz



gunzip /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii.gz

fslmerge -t /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_20Hz.nii.gz \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/*_varcope1_*.nii.gz


gunzip /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_20Hz.nii.gz


#======================================================================================================================


fslmerge -t /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii.gz \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/*_cope1_*.nii.gz


gunzip /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii.gz

fslmerge -t /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_40Hz.nii.gz \
/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/*_varcope1_*.nii.gz



gunzip /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_40Hz.nii.gz


#======================================================================================================================


# mkdir media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/palm

# palm \
# -i /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii \
# -o /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz//palm/10Hz_ \
# -m /home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.mat \
# -t /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.con \
# -f /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.fts \
# -vg /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.grp \
# -n 5000 -T -C 3.1 -ise -corrcon -save1-p



# mkdir media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/palm

# palm \
# -i /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii \
# -o /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/palm/20Hz_ \
# -m /home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.mat \
# -t /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.con \
# -f /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.fts \
# -vg /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.grp \
# -n 5000 -T -C 3.1 -ise -corrcon -save1-p


# mkdir media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/palm

# palm \
# -i /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii \
# -o /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/palm/40Hz_ \
# -m /home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.mat \
# -t /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.con \
# -f /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.fts \
# -vg /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.grp \
# -n 5000 -T -C 3.1 -ise -corrcon -save1-p



#======================================================================================================================



flameo \
--cope=/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii \
--vc=/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_10Hz.nii \
--mask=/home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
--ld=/home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/flameo/ \
--dm=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.mat \
--cs=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.grp \
--tc=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.con \
--runmode=flame12






flameo \
--cope=/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii \
--vc=/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_20Hz.nii \
--mask=/home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
--ld=/home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/flameo/ \
--dm=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.mat \
--cs=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.grp \
--tc=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.con \
--runmode=flame12






flameo \
--cope=/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii \
--vc=/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_40Hz.nii \
--mask=/home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
--ld=/home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/flameo/ \
--dm=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.mat \
--cs=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.grp \
--tc=/home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.con \
--runmode=flame12




#================================================================================================================================
#
# mkdir /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/randomise
#
# randomise \
# -i /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii \
# -o /home/in/aeed/Work/stimulation/stimulation_3rd_level/10Hz/randomise/10Hz_ \
# -m /home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.mat \
# -t /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.con \
# -n 5000 -x -T --uncorrp
#
#
# mkdir /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/randomise
#
#
#
# randomise \
# -i /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii \
# -o /home/in/aeed/Work/stimulation/stimulation_3rd_level/20Hz/randomise/20Hz_ \
# -m /home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.mat \
# -t /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.con \
# -n 5000 -x -T --uncorrp
#
#
# mkdir /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/randomise
#
#
#
# randomise \
# -i /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii \
# -o /home/in/aeed/Work/stimulation/stimulation_3rd_level/40Hz/randomise/40Hz_ \
# -m /home/in/aeed/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.mat \
# -t /home/in/aeed/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.con \
# -n 5000 -x -T --uncorrp
#
#
#
#
#
#
#
#
#
#
#
#
