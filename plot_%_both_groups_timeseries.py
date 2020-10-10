# plot the average timeseries


# the script should take a list of txt files representing timeseries of a group of subjects (aka A or B)
# the script should return a plot with the average timesreis with +/- SEM shading
# the script should have a fixed y limit
# y title should be "% BOLD change"
# time (Sec)

# second modification is pass only the frequency and genotype and the script does the rest

def plot_av_percent_change(frequency):

    import os
    import re
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    import ntpath
    import pandas as pd

    directory = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/{0}/timeseries'.format(
        frequency)
    os.chdir(directory)

# get all the names from the given directory
    filenames = list(os.listdir(directory))
    list_of_ts_A = []
    list_of_ts_B = []

# use only the files belongs to the specific genotype
    for file in filenames:
        if file[0] == 'A':
            list_of_ts_A.append(file)
        elif file[0] == 'B':
            list_of_ts_B.append(file)

    list_ts_arrays_A = []
    list_ts_arrays_B = []
    i = 0

    for ts in list_of_ts_A:
        while i < len(list_of_ts_A):
            ts = np.loadtxt(list_of_ts_A[i])
            list_ts_arrays_A.append(ts)
            i = i + 1

    i = 0
    for ts in list_of_ts_B:
        while i < len(list_of_ts_B):
            ts = np.loadtxt(list_of_ts_B[i])
            list_ts_arrays_B.append(ts)
            i = i + 1

    mean_ts_A = np.mean(list_ts_arrays_A, axis=0)
    mean_ts_df_A = pd.DataFrame(mean_ts_A)

    mean_ts_B = np.mean(list_ts_arrays_B, axis=0)
    mean_ts_df_B = pd.DataFrame(mean_ts_B)

    # smoothing for the signal
    smooth_mean_A = mean_ts_df_A.rolling(5).mean()
    # remove NaN
    smooth_mean_A = smooth_mean_A.fillna(smooth_mean_A.mean())
    smooth_mean_A = smooth_mean_A.rename(columns={0: 'timeseries'})


    # smoothing for the signal
    smooth_mean_B = mean_ts_df_B.rolling(5).mean()
    # remove NaN
    smooth_mean_B = smooth_mean_B.fillna(smooth_mean_B.mean())
    smooth_mean_B = smooth_mean_B.rename(columns={0: 'timeseries'})



    # I want to make the x by sec (0:300) rather than by volumes (0:15)
    time = np.arange(0, 300, 2)

    # add another column to smooth_mean to serve as x axis time
    smooth_mean_A['time'] = time
    smooth_mean_B['time'] = time

    sem_ts_A = stats.sem(list_ts_arrays_A, axis=0)  # sem as in standard error of the mean
    sem_ts_B = stats.sem(list_ts_arrays_B, axis=0)

    # mean plus or minus SEM
    under_line_A = smooth_mean_A['timeseries'] - sem_ts_A
    over_line_A = smooth_mean_A['timeseries'] + sem_ts_A

    # mean plus or minus SEM
    under_line_B = smooth_mean_B['timeseries'] - sem_ts_B
    over_line_B = smooth_mean_B['timeseries'] + sem_ts_B



    # you need an index as the 1st arg of fill_between to determine where to put the shading
    filling_index = list(range(0, 150))

    # TODO Do not forget to put the stimulation protocol # DONE
    # TODO one HRF

###############################################################################################################################
# the stimulation file has changed. instead of 1 in place of stimulation, 0.8125(end range of y) was put

    stim = np.loadtxt(
        '/media/amr/Amr_4TB/Dropbox/thesis/stimulation/Stimulation.txt')
###############################################################################################################################
    # plot gp A timeseries overlaid on stimulation
    ax = plt.axes()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.yticks(y_range)
    plt.ylim(0.80125, 0.8125)
    plt.xlim(0, 298)
    plt.xlabel("Time (sec)", fontsize=18, fontname='Arial')
    plt.ylabel("% BOLD change", fontsize=18, fontname='Arial')


    # create a figure of A group timeseries with sem shading over the stimulation pattern
    plt.plot(stim[:, 1], drawstyle='steps-pre', color='black', linewidth=0)
    plt.fill_between(stim[:,0], stim[:, 1], step="pre", alpha=0.2, color='gray')

    plt.plot(smooth_mean_A['time'], smooth_mean_A['timeseries'], color='#e41a1c', linewidth=1)
    plt.fill_between(smooth_mean_A['time'], under_line_A, over_line_A, color='#e41a1c', alpha=.3, linewidth=1)

    plt.savefig(
        "/media/amr/Amr_4TB/Dropbox/thesis/stimulation/perforant_A_{0}_%_change_ts.svg".format(frequency), format='svg')
    plt.close()
    print('##################### Done plotting gp A #####################')
#========================================================================================================0
    # plot gp B timeseries overlaid on stimulation
    ax = plt.axes()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.yticks(y_range)
    plt.ylim(0.80125, 0.8125)
    plt.xlim(0, 298)
    plt.xlabel("Time (sec)", fontsize=18, fontname='Arial')
    plt.ylabel("% BOLD change", fontsize=18, fontname='Arial')


    # create a figure of A group timeseries with sem shading over the stimulation pattern
    plt.plot(stim[:, 1], drawstyle='steps-pre', color='black', linewidth=0)
    plt.fill_between(stim[:,0], stim[:, 1], step="pre", alpha=0.2, color='gray')

    plt.plot(smooth_mean_B['time'], smooth_mean_B['timeseries'], color='#377eb8', linewidth=1)
    plt.fill_between(smooth_mean_B['time'], under_line_B, over_line_B, color='#377eb8', alpha=.3, linewidth=1)

    plt.savefig(
        "/media/amr/Amr_4TB/Dropbox/thesis/stimulation/perforant_B_{0}_%_change_ts.svg".format(frequency), format='svg')
    plt.close()
    print('##################### Done plotting gp B #####################')
#========================================================================================================0
    # plot both A & B timeseries overlaid on stimulation


    ax = plt.axes()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.yticks(y_range)
    plt.ylim(0.80125, 0.8125)
    plt.xlim(0, 298)
    plt.xlabel("Time (sec)", fontsize=18, fontname='Arial')
    plt.ylabel("% BOLD change", fontsize=18, fontname='Arial')



    plt.plot(stim[:, 1], drawstyle='steps-pre', color='black', linewidth=0)
    plt.fill_between(stim[:,0], stim[:, 1], step="pre", alpha=0.2, color='gray')

    plt.plot(smooth_mean_A['time'], smooth_mean_A['timeseries'], color='#e41a1c', linewidth=1)
    plt.fill_between(smooth_mean_A['time'], under_line_A, over_line_A, color='#e41a1c', alpha=.3, linewidth=1)

    plt.plot(smooth_mean_B['time'], smooth_mean_B['timeseries'], color='#377eb8', linewidth=1)
    plt.fill_between(smooth_mean_B['time'], under_line_B, over_line_B, color='#377eb8', alpha=.3, linewidth=1)

    plt.savefig(
        "/media/amr/Amr_4TB/Dropbox/thesis/stimulation/perforant_Both_{0}_%_change_ts.svg".format(frequency), format='svg')
    plt.close()
    print('##################### Done plotting combined plot #####################')
#========================================================================================================0

plot_av_percent_change('10Hz')

plot_av_percent_change('20Hz')

plot_av_percent_change('40Hz')
