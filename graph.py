import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

def create_graph(best_costs, worst_costs):
    labels = [x[:2] for x in os.listdir("0")]

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(30, 20))
    rects1 = ax.bar(x - width/2, best_costs, width, label='Best')
    rects2 = ax.bar(x + width/2, worst_costs, width, label='Worst')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = plt.gca().get_xticklabels()


    #autolabel(ax, rects1)
    #autolabel(ax, rects2)

    plt.savefig("graph" + ".png")
    plt.show()


def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
