from pylab import plt
import gingivere.data


def plot_mat(data):
    # Three subplots sharing both x/y axes
    f, axarray = plt.subplots(16, sharex=True, sharey=True)
    for i, row in enumerate(data):
        axarray[i].plot(range(len(row)), row, 'g')
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes], visible=False)
    plt.setp([a.get_yticklabels() for a in f.axes], visible=False)
    axarray[0].set_title('10 minute EEG Reading for Patient')
    axarray[int(len(axarray) / 2)].set_ylabel('Magnitude')
    axarray[-1].set_xlabel('Time')
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 48}
    plt.rc('font', **font)
    plt.show()


def main():
    g = gingivere.data.generate_mat_paths('Dog_2')
    path = next(g)
    data = gingivere.data.source(path)
    plot_mat(data)


if __name__ == "__main__":
    main()
