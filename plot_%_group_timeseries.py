# plot the average timeseries


# the script should take a list of txt files representing timeseries of a group of subjects (aka A or B)
# the script should return a plot with the average timesreis with +/- SEM shading
# the script should have a fixed y limit
# y title should be "% BOLD change"
# time (Sec)


def plot_av_percent_change(list_of_ts):

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats

    list_ts_arrays = []
    i = 0

    for ts in list_of_ts:
        while i < len(list_of_ts):
            ts = np.loadtxt(list_of_ts[i])
            list_ts_arrays.append(ts)
            i = i + 1

    mean_ts = np.mean(list_ts_arrays, axis=0)
    sem_ts = stats.sem(list_ts_arrays, axis=0)  # sem as in standard error of the mean

    # mean plus or minus SEM
    under_line = mean_ts - sem_ts
    over_line = mean_ts + sem_ts

    # you need an index as the 1st arg of fill_between to determine where to put the shading
    filling_index = list(range(0, 150))

    # TODO Do not forget to put the stimulation protocol
    # TODO limit the y axis, titles
    # TODO cluster branch and CA3 scripts
    # TODO different color for genotypes based on the first letter of the filenames (A or B)
    # TODO save as svg
    # TODO one HRF
    # A -> #377eb899
    # B -> e41a1c99
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(0.5, -0.5)
    plt.xlim(0, 150)
    plt.xlabel("Time (sec)", fontsize=18, fontname='Arial')
    plt.ylabel("% BOLD change", fontsize=18, fontname='Arial')
    plt.plot(mean_ts, color='#377eb899')
    plt.fill_between(filling_index, under_line, over_line, color='b', alpha=.1)
    plt.savefig("/Users/amr/Dropbox/thesis/stimulation/meants.svg", format='svg')
