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

# ==========================================================================================================================================================
# In[2]:

experiment_dir = '/media/amr/Amr_4TB/Work/stimulation'


frequency_list = ['10Hz',
                  '20Hz',
                  '40Hz']


subject_list = ['003', '005', '008', '011',
                '130', '018', '019', '020',
                '059', '060', '062', '063',
                '066', '126', '127', '146']


output_dir = 'output_stimulation_no_voxels'
working_dir = 'workingdir_stimulation_no_voxels'


no_voxels = Workflow(name='no_voxels')
no_voxels.base_dir = opj(experiment_dir, working_dir)


# ==========================================================================================================================================================
# In[3]:
# to prevent nipype from iterating over the anat image with each func run-, you need seperate
# nodes to select the files
# and this will solve the problem I have for almost 6 months
# but notice that in the sessions, you have to iterate also over subject_id to get the {subject_id} var


# Infosource - a function free node to iterate over the list of subject names

infosource = Node(IdentityInterface(fields=['frequencies', 'subjects']),
                  name="infosource")
infosource.iterables = [('frequencies', frequency_list),
                        ('subjects', subject_list)]


# ==========================================================================================================================================================
# In[4]:

template_brain = '/media/amr/Amr_4TB/Work/October_Acquistion/anat_temp_enhanced_3.nii.gz'
template_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/anat_template_enhanced_mask_2.nii.gz'
left_side_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/left_anat_tem_3_enh_mask.nii.gz'

templates = {

    'thresh_zstat':  '/media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_{frequencies}/stimulation_2nd_level_{frequencies}/_subject_id_{subjects}/cluster_copes1/thresh_zstat1.nii.gz',
    'anat_2_temp': '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_subject_id_{subjects}/reg_T1_2_temp/transformComposite.h5'
}


selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir),
                   name="selectfiles")
# ==========================================================================================================================================================
# In[5]:

datasink = Node(DataSink(), name='datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_frequencies_', ''), ('_subjects_', '_')]

datasink.inputs.substitutions = substitutions

# ==========================================================================================================================================================
# Smooth estimation
thresh_zstats_2_template = Node(ants.ApplyTransforms(), name='thresh_zstats_2_template')
thresh_zstats_2_template.inputs.dimension = 3
thresh_zstats_2_template.inputs.reference_image = template_brain
thresh_zstats_2_template.inputs.output_image = 'thresh_zstats_2_template_brain.nii.gz'


# ==========================================================================================================================================================
# get total number of voxels
# better to get the number of active voxels after applying transformations to compenstae for different head sizes
total_no_voxels = Node(fsl.ImageStats(), name='total_no_voxels')
total_no_voxels.inputs.op_string = '-V > total_no_voxels.txt'

# ==========================================================================================================================================================
# apply left side mask
extract_left_side = Node(fsl.ExtractROI(), name='extract_left_side')
extract_left_side.inputs.x_min = 105
extract_left_side.inputs.x_size = -1
extract_left_side.inputs.y_min = 0
extract_left_side.inputs.y_size = -1
extract_left_side.inputs.z_min = 0
extract_left_side.inputs.z_size = -1


# ==========================================================================================================================================================
# get total number of voxels

left_no_voxels = Node(fsl.ImageStats(), name='left_no_voxels')
left_no_voxels.inputs.op_string = '-V  > left_no_voxels.txt'

# ==========================================================================================================================================================
# generate pics thresh_zstat1

no_voxels.connect([


    (infosource, selectfiles, [('frequencies', 'frequencies'),
                               ('subjects', 'subjects')]),



    (selectfiles, thresh_zstats_2_template, [('anat_2_temp', 'transforms'),
                                             ('thresh_zstat', 'input_image')]),




    (thresh_zstats_2_template, total_no_voxels, [('output_image', 'in_file')]),




    (thresh_zstats_2_template, extract_left_side, [('output_image', 'in_file')]),


    (extract_left_side, left_no_voxels, [('roi_file', 'in_file')]),


])

no_voxels.write_graph(graph2use='colored', format='png', simple_form=True)

# no_voxels.run(plugin='SLURM', plugin_args={
#     'dont_resubmit_completed_jobs': True, 'max_jobs': 50})

no_voxels.run(plugin='MultiProc', plugin_args={'n_procs': 16})
