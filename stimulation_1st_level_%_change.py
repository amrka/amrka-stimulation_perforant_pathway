# In[1]:

import re
import os
from nipype.interfaces.matlab import MatlabCommand
import matplotlib.pyplot as plt
import numpy as np
from nipype.pipeline.engine import Workflow, Node, MapNode
from nipype.interfaces.io import SelectFiles, DataSink
from os.path import join as opj
from nipype.interfaces.utility import IdentityInterface, Function, Select, Merge
import nipype.interfaces.spm as spm
import nipype.interfaces.ants as ants
import nipype.interfaces.afni as afni
import nipype.interfaces.fsl as fsl
from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)


MatlabCommand.set_default_paths('/Users/amr/Downloads/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")

# import nipype.interfaces.matlab as mlab
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
# mlab.MatlabCommand.set_default_paths('/home/amr/Documents/MATLAB/toolbox/spm8')

# ============================================================================================================================
# In[2]:
experiment_dir = '/media/amr/Amr_4TB/Work/stimulation'


subject_list = ['003', '005', '008', '011',
                '130', '018', '019', '020',
                '059', '060', '062', '063',
                '066', '126', '127', '146']


session_list = ['run001', 'run002', 'run003']


frequency_list = ['10Hz', '20Hz', '40Hz']


output_dir = 'Stimulation_1st_level_OutputDir_%_change'
working_dir = 'Stimulation_1st_level_WorkingDir_%_change'

stimulation_1st_level_percent_change = Workflow(name='stimulation_1st_level_percent_change')
stimulation_1st_level_percent_change.base_dir = opj(experiment_dir, working_dir)


# ============================================================================================================================
# In[3]:
infosource = Node(IdentityInterface(fields=['subject_id', 'session_id', 'frequency_id']),
                  name="infosource")

infosource.iterables = [('subject_id', subject_list),
                        ('session_id', session_list),
                        ('frequency_id', frequency_list)]


# ============================================================================================================================
# In[4]:
# sub-001_task-MGT_run-02_bold.nii.gz, sub-001_task-MGT_run-02_sbref.nii.gz
# /media/amr/Amr_4TB/MGT_poldrack/output_MGT_poldrack_preproc_preproc/preproc_img/run-04sub-119/afni_2d_smoothed_all_maths_filt_maths.nii.gz
# functional runs
templates = {

    'preproc_img': '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_OutputDir/preproc_img/{frequency_id}_{session_id}_subj_{subject_id}/afni_2d_smoothed_maths_filt_maths.nii.gz',
    'bold_brain': '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_OutputDir/bold_brain/{frequency_id}_{session_id}_subj_{subject_id}/Stim_{subject_id}_??_{frequency_id}_{session_id}_roi_masked.nii.gz',
    'bold_mask': '/media/amr/Amr_4TB/Work/stimulation/Data/{subject_id}/EPI_{subject_id}_Mask.nii.gz',

    'tem2anat': '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_subject_id_{subject_id}/reg_T1_2_temp/transformInverseComposite.h5',
    'ant2func': '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_frequency_id_{frequency_id}_session_id_{session_id}_subject_id_{subject_id}/coreg/bold_2_anat_sub-{subject_id}0GenericAffine.mat',
    'anat_img': '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_subject_id_{subject_id}/biasfield_correction_anat/Anat_{subject_id}_bet_corrected.nii.gz'}


selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")
# ============================================================================================================================
# In[5]:
datasink = Node(DataSink(), name='datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', '_subj_'), ('_session_id_', '_'), ('_frequency_id_', '')]

datasink.inputs.substitutions = substitutions

# ============================================================================================================================


template_brain = '/media/amr/Amr_4TB/Work/October_Acquistion/anat_temp_enhanced_3.nii.gz'
template_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/anat_template_enhanced_mask_2.nii.gz'
template_hpc_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/anat_temp_enhanced_3_hpc.nii.gz'
# ============================================================================================================================
# get mean of the final image

get_filtered_mean = Node(fsl.MeanImage(), name='filtered_img_mean')
get_filtered_mean.inputs.dimension = 'T'
get_filtered_mean.inputs.out_file = 'filtered_img_mean.nii.gz'


# ============================================================================================================================
# transform the hpc mask to each subject's space
# In[10]:
# Merge the trasnforms
merge_transforms = Node(Merge(2), name='merge_transforms')


transform_hpc_mask = Node(ants.ApplyTransforms(), name='transform_hpc_mask')
transform_hpc_mask.inputs.input_image = template_hpc_mask
transform_hpc_mask.inputs.interpolation = 'NearestNeighbor'
transform_hpc_mask.inputs.invert_transform_flags = [False, True]


# ============================================================================================================================
# scaling factor per J.Mumford's file for % change
# scale_factor = 100 * 0.8061686(PPheights from unfiltered stimulation design)/ -1 (contrast fix to make the contrast sums to +1)
# fslmaths filtered_func_data -mul scale_factor -div mean_func
# fslmeants -i output_image -m mask

# scale_factor = -80.61686
# the scale is probably off by 100x factor, because the timeseries is in hunderedth range
# it makes sense since the voxels value are scaled 100s higher than the human data, probably from the machine
# scale_factor = -.8061686
# after I looked at the end graphs, this was a mistake

scale_factor = 0.8061686


mul_by_scaling_factor = Node(fsl.BinaryMaths(), name='multiply_by_scaling_factor')
mul_by_scaling_factor.inputs.operation = 'mul'
mul_by_scaling_factor.inputs.operand_value = scale_factor
mul_by_scaling_factor.inputs.out_file = 'multiplied_by_scaling_factor.nii.gz'

# ============================================================================================================================
# divide by mean image
div_by_mean_img = Node(fsl.BinaryMaths(), name='div_by_mean_img')
div_by_mean_img.inputs.operation = 'div'
div_by_mean_img.inputs.out_file = 'divided_by_mean_img.nii.gz'

# ============================================================================================================================
# fslmeants to get the timesereis
get_percent_change_timeseries = Node(fsl.ImageMeants(), name='get_percent_change_timeseries')
get_percent_change_timeseries.inputs.out_file = 'percent_change_timeseries.txt'

# ============================================================================================================================

stimulation_1st_level_percent_change.connect([


    (infosource, selectfiles, [('subject_id', 'subject_id'),
                               ('session_id', 'session_id'),
                               ('frequency_id', 'frequency_id')]),

    (selectfiles, get_filtered_mean, [('preproc_img', 'in_file')]),

    (selectfiles, merge_transforms, [('tem2anat', 'in1')]),
    (selectfiles, merge_transforms, [('ant2func', 'in2')]),


    (selectfiles, transform_hpc_mask, [('bold_brain', 'reference_image')]),
    (merge_transforms, transform_hpc_mask, [('out', 'transforms')]),

    (selectfiles, mul_by_scaling_factor, [('preproc_img', 'in_file')]),

    (mul_by_scaling_factor, div_by_mean_img, [('out_file', 'in_file')]),
    (get_filtered_mean, div_by_mean_img, [('out_file', 'operand_file')]),

    (div_by_mean_img, get_percent_change_timeseries, [('out_file', 'in_file')]),
    (transform_hpc_mask, get_percent_change_timeseries, [('output_image', 'mask')])


])

stimulation_1st_level_percent_change.write_graph(
    graph2use='colored', format='png', simple_form=True)

stimulation_1st_level_percent_change.run('MultiProc', plugin_args={'n_procs': 8})
