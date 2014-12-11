from pylab import *
import gingivere.data

def plot_mat(data):
    num_rows = len(data)
    for i, row in enumerate(data):
        plt.subplot(num_rows, 1, i+1)
        plt.plot(range(len(row)), row, 'g')
    plt.show()


def main():
    g = gingivere.data.generate_mat_paths('Dog_2')
    path = next(g)
    data = gingivere.data.source(path)
    plot_mat(data)

if __name__ == "__main__":
    main()
