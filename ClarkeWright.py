from math import sqrt, pow
import os

filespath = 'C:\\Users\\Giacomo\\Desktop\\University\\Magistrale Informatica\\1 ANNO\\DS\\I19\\Instanze simmetriche CVRPB\\Instances'
files = [(x if x[-3:] == "txt" and x != "info.txt" else None) for x in os.listdir(filespath)]


def main():
    for filename in files:
        if filename:
            with open(filespath + "\\" + filename, 'r') as file:
                n_customers = int(file.readline())
                file.readline()
                vehicles = int(file.readline())
                deposit = list(map(int, file.readline().split('   ')))
                customers = []
                backhauls = 0
                for i in range(n_customers):
                    customers.append(list(map(int, file.readline().split('   '))))
                    if customers[i][2] == 0:
                        backhauls += 1

                savings, distances = compute_savings(deposit, customers)
                """
                if filename == "A1.txt":
                    for x in distances:
                        print(x)
                        print("\n")
                        """
                if filename == "B3.txt":
                    print("cazzo")
                savings.sort(key=lambda e: e[1], reverse=True)
                routes = parallel_CVRP(vehicles, deposit, customers, distances, savings, backhauls)
                fileprint(filename, routes, deposit, customers, vehicles)


def compute_savings(deposit, customers):
    savings = [[]]
    distances = [[0 for x in range(customers.__len__()+1)] for y in range(customers.__len__()+1)]

    for i in range(1, customers.__len__()+1):
        distances[0][i] = dist(deposit[0], deposit[1], customers[i-1][0], customers[i-1][1])
        for j in range(i+1, customers.__len__()+1):
            cost1 = distances[0][i]
            cost2 = dist(deposit[0], deposit[1], customers[j-1][0], customers[j-1][1])
            cost_ij = dist(customers[i-1][0], customers[i-1][1], customers[j-1][0], customers[j-1][1])
            distances[i][j] = cost_ij
            save = cost1 + cost2 - cost_ij
            savings.append([(i, j), save])

    del savings[0]
    return savings, distances


def parallel_CVRP(vehicles, deposit, customers, distances, savings, backhauls):
    routes = []

    for i in range(1, customers.__len__()+1):
        routes.append({
            "Cost": distances[0][i]*2,
            "Delivery Load": customers[i-1][2],
            "Pick-up Load": customers[i-1][3],
            "Customers in Route": 1,
            "Vertex Sequence": [0, i, 0]
        })

    print("ciao")

    for s in savings:
        if routes.__len__() == vehicles:
            break
        new_route = None
        first = False
        second = False
        for c, r in enumerate(routes):
            if r["Vertex Sequence"][1] == s[0][0] and not first:
                if new_route is None:
                    new_route = (-1, c)
                    first = True
                    continue
                # new_route[0] is a linehaul? or s[0][0] is a backhaul
                else:
                    new_route = (new_route[1], -1) if new_route[0] == -1 else new_route
                    if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or customers[s[0][0]-1][2] == 0:
                        new_route = (new_route[0], c)
                        break
                    elif customers[r["Vertex Sequence"][1]-1][2] == 0 or customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0:
                        # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                        new_route = (new_route[0], new_route[0])
                        new_route = (c, new_route[0])
                        break

            if r["Vertex Sequence"][-2] == s[0][0] and not first:
                # if customers[s[0][0]-1][2] != 0: # only if linehaul
                if not new_route:
                    new_route = (c, -1)
                    first = True
                    """
                    else:
                        new_route = (c, new_route[1])
                        break
                    """
                else:
                    new_route = (-1, new_route[0]) if new_route[1] == -1 else new_route
                    if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or customers[s[0][0]-1][2] != 0:
                        new_route = (c, new_route[1])
                        break
                    elif customers[r["Vertex Sequence"][1]-1][2] == 0 or customers[routes[new_route[1]]["Vertex Sequence"][-2]-1][2] != 0:
                        # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                        new_route = (new_route[1], new_route[1])
                        new_route = (new_route[1], c)
                        break

            if r["Vertex Sequence"][1] == s[0][1] and not second:
                if not new_route:
                    new_route = (-1, c)
                    second = True
                    continue
                # new_route[0] is a linehaul? or s[0][1] is a backhaul
                else:
                    new_route = (new_route[1], -1) if new_route[0] == -1 else new_route
                    if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or customers[s[0][1]-1][2] == 0:
                        new_route = (new_route[0], c)
                        break
                    elif customers[r["Vertex Sequence"][1]-1][2] == 0 or customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0:
                        new_route = (new_route[0], new_route[0])
                        new_route = (c, new_route[0])
                        break

            if r["Vertex Sequence"][-2] == s[0][1] and not second:
                #if customers[s[0][1]-1][2] != 0: # only if linehaul
                if not new_route:
                    new_route = (c, -1)
                    second = True
                    """
                    else:
                        new_route = (c, new_route[1])
                        break
                    """
                    # in case "if customers[s[0][1]][2] != 0" is not present
                else:
                    new_route = (-1, new_route[0]) if new_route[1] == -1 else new_route
                    if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or customers[s[0][1]-1][2] != 0:
                        new_route = (c, new_route[1])
                        break
                    elif customers[r["Vertex Sequence"][1]-1][2] == 0 or customers[routes[new_route[1]]["Vertex Sequence"][-2]-1][2] != 0:
                        # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                        new_route = (new_route[1], new_route[1])
                        new_route = (new_route[1], c)
                        break

        if new_route:
            if new_route[0] != -1 and new_route[1] != -1:
                if customers[s[0][0] - 1][2] == 0 or customers[s[0][1] - 1][2] == 0:
                    backhauls -= 1
                #elif not routes.__len__() - backhauls > vehicles:
                 #   continue

                if routes[new_route[0]]["Delivery Load"] + routes[new_route[1]]["Delivery Load"] < deposit[3] and \
                        routes[new_route[0]]["Pick-up Load"] + routes[new_route[1]]["Pick-up Load"] < deposit[3]:
                    routes[new_route[0]]["Vertex Sequence"] = routes[new_route[0]]["Vertex Sequence"][:-1] + \
                                                              routes[new_route[1]]["Vertex Sequence"][1:]
                    routes[new_route[0]]["Cost"] += routes[new_route[1]]["Cost"] - s[1]
                    routes[new_route[0]]["Delivery Load"] += routes[new_route[1]]["Delivery Load"]
                    routes[new_route[0]]["Pick-up Load"] += routes[new_route[1]]["Pick-up Load"]
                    routes[new_route[0]]["Customers in Route"] += routes[new_route[1]]["Customers in Route"]
                    del routes[new_route[1]]

    return routes


def fileprint(output, routes, deposit, customers, vehicles):
    with open(output[:-4] + "out" + output[-4:], "w") as file:
        file.write("PROBLEM DETAILS:\n")
        file.write("Customers = " + str(customers.__len__()) + '\n')
        file.write("Max Load = " +str(deposit[3]) + '\n')
        file.write("Max Cost = 999999999999999\n\n")
        file.write("SOLUTION DETAILS:\n")
        file.write("Total Cost = " + str(sum(i["Cost"] for i in routes)) + '\n')
        file.write("Routes Of the Solution = " + str(vehicles) + '\n\n')
        for c, r in enumerate(routes):
            file.write("ROUTE " + str(c) + ':\n')
            file.write("Cost = " + str(r["Cost"]) + '\n')
            file.write("Delivery Load = " + str(r["Delivery Load"]) + '\n')
            file.write("Pick-Up Load = " + str(r["Pick-up Load"]) + '\n')
            file.write("Customers in Route = " + str(r["Customers in Route"]) + '\n')
            file.write("Vertex Sequence :\n" + " ".join([str(x) for x in r["Vertex Sequence"]]) + '\n\n')


def dist(xA, yA, xB, yB):
    return sqrt( pow(xA-xB, 2) + pow(yA-yB, 2) )


if __name__ == "__main__":
    main()
