import os
import graph

files = [x if x[-3:] == "txt" else None for x in os.listdir()]
files = list(filter(None.__ne__, files))

filespath = 'C:\\Users\\Giacomo\\Desktop\\University\\Magistrale Informatica\\1 ANNO\\DS\\I19\\Best__Solutions\\RPA_Solutions'
files_sol = [(x if x[-3:] == "txt" and x != "info.txt" else None) for x in os.listdir(filespath)]
files_sol = list(filter(None.__ne__, files_sol))


def best_to_ours():
    i = 0
    cost_sol = []
    cost_ours = []
    while i != files.__len__():
        with open(filespath + '\\' + files_sol[i], "r") as f:
            cost_sol.append(float(f.readlines()[8].split(" = ")[1]))
        with open(files[i], "r") as f:
            cost_ours.append(float(f.readlines()[6].split(" = ")[1]))
        i += 1

    i = 0
    sum_error = 0
    while i != cost_ours.__len__():
        sum_error += cost_ours[i] - cost_sol[i]
        print(cost_sol[i], cost_ours[i], cost_ours[i] - cost_sol[i])
        print("\n")
        i += 1
    print(sum_error/cost_sol.__len__())

    with open("risultatiSequenzialeSenzaMischiare.txt", "w") as r:
        r.write("File     Costo nostro           Costo ottimale     Differenza\n")
        i = 0
        while i != cost_ours.__len__():
            r.write(files[i][:2] + "       " + str(cost_ours[i]) + "     " + str(cost_sol[i]) + "             " + str(cost_ours[i] - cost_sol[i]) + "\n")
            i += 1


def sequential_comp():
    costs = []
    for test in range(100):
        costs.append([])
        files = [x if x[-3:] == "txt" else None for x in os.listdir(str(test))]
        files = list(filter(None.__ne__, files))
        for file in files:
            with open(str(test) + "\\" + file) as f:
                costs[test].append(float(f.readlines()[6].split(" = ")[1]))

    best_costs = [x for x in costs[0]]
    worst_costs = [x for x in costs[0]]
    for subcosts in costs:
        for i, sub in enumerate(subcosts):
            if sub < best_costs[i]:
                best_costs[i] = sub
            if sub > worst_costs[i]:
                worst_costs[i] = sub
    with open("seq_compare.txt", "w") as seq:
        seq.write("Best Costs\n")
        seq.write(" ".join(format(x, "10.2f") for x in best_costs))
        seq.write("\nWorst Costs\n")
        seq.write(" ".join(format(x, "10.2f") for x in worst_costs))

    graph.create_graph(best_costs, worst_costs)
