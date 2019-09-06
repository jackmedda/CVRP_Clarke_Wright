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
    linehauls = customers.__len__() - backhauls
    line_back = 0

    for i in range(1, customers.__len__()+1):
        routes.append({
            "Cost": distances[0][i]*2,
            "Delivery Load": customers[i-1][2],
            "Pick-up Load": customers[i-1][3],
            "Customers in Route": 1,
            "Vertex Sequence": [0, i, 0]
        })

    for x, s in enumerate(savings):
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
                    if new_route[0] == -1:
                        if r["Vertex Sequence"].__len__() != 3 and \
                                routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                            new_route = (new_route[1], -1)
                            if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                    customers[s[0][0]-1][2] == 0:
                                new_route = (new_route[0], c)
                                break
                    else:
                        if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                customers[s[0][0]-1][2] == 0:
                            new_route = (new_route[0], c)
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                            # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                            new_route = (new_route[0], new_route[0])
                            new_route = (c, new_route[0])
                            break

            if r["Vertex Sequence"][-2] == s[0][0] and not first:
                # if customers[s[0][0]-1][2] != 0: # only if linehaul
                if not new_route:
                    new_route = (c, -1)
                    first = True
                    continue
                else:
                    if new_route[1] == -1:
                        if r["Vertex Sequence"].__len__() != 3 and \
                                routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                            new_route = (-1, new_route[0])
                            if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or \
                                    customers[s[0][0]-1][2] != 0:
                                new_route = (c, new_route[1])
                                break
                    else:
                        if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or \
                                customers[s[0][0]-1][2] != 0:
                            new_route = (c, new_route[1])
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
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
                    if new_route[0] == -1:
                        if r["Vertex Sequence"].__len__() != 3 and \
                                routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                            new_route = (new_route[1], -1)
                            if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                    customers[s[0][1]-1][2] == 0:
                                new_route = (new_route[0], c)
                                break
                    else:
                        if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                customers[s[0][1]-1][2] == 0:
                            new_route = (new_route[0], c)
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                            new_route = (new_route[0], new_route[0])
                            new_route = (c, new_route[0])
                            break

            if r["Vertex Sequence"][-2] == s[0][1] and not second:
                # if customers[s[0][1]-1][2] != 0: # only if linehaul
                if not new_route:
                    new_route = (c, -1)
                    second = True
                    continue
                    # in case "if customers[s[0][1]][2] != 0" is not present
                else:
                    if new_route[1] == -1:
                        if r["Vertex Sequence"].__len__() != 3 and \
                                routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                            new_route = (-1, new_route[0])
                            if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or \
                                    customers[s[0][1]-1][2] != 0:
                                new_route = (c, new_route[1])
                                break
                    else:
                        if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or customers[s[0][1]-1][2] != 0:
                            new_route = (c, new_route[1])
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                 routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                            # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                            new_route = (new_route[1], new_route[1])
                            new_route = (new_route[1], c)
                            break

        if new_route:
            if new_route[0] != -1 and new_route[1] != -1:

                def merge_routes(s, new_route, routes):
                    routes[new_route[0]]["Vertex Sequence"] = routes[new_route[0]]["Vertex Sequence"][:-1] + \
                                                              routes[new_route[1]]["Vertex Sequence"][1:]
                    routes[new_route[0]]["Cost"] += routes[new_route[1]]["Cost"] - s[1]
                    routes[new_route[0]]["Delivery Load"] += routes[new_route[1]]["Delivery Load"]
                    routes[new_route[0]]["Pick-up Load"] += routes[new_route[1]]["Pick-up Load"]
                    routes[new_route[0]]["Customers in Route"] += routes[new_route[1]]["Customers in Route"]
                    del routes[new_route[1]]

                if routes[new_route[0]]["Delivery Load"] + routes[new_route[1]]["Delivery Load"] <= deposit[3] and \
                        routes[new_route[0]]["Pick-up Load"] + routes[new_route[1]]["Pick-up Load"] <= deposit[3]:
                    # if one of savings contains a pick up
                    less_back = False
                    if customers[s[0][0] - 1][2] == 0 or customers[s[0][1] - 1][2] == 0:
                        backhauls -= 1
                        less_back = True
                    elif routes.__len__() - backhauls == vehicles:
                        continue

                    # in case new_route is (0-3-....-linehaul, backhaul-7-....-0)
                    if (customers[s[0][0]-1][2] == 0 and customers[s[0][1]-1][2] != 0) or \
                            (customers[s[0][0]-1][2] != 0 and customers[s[0][1]-1][2] == 0):
                        if line_back < vehicles:
                            line_back += 1
                        else:
                            if less_back:
                                backhauls += 1
                            savings.append(savings.pop(x))
                            continue

                    if customers[s[0][0] - 1][2] != 0 and customers[s[0][1] - 1][2] != 0:
                        linehauls -= 1

                    merge_routes(s, new_route, routes)

    while routes.__len__() != vehicles:
        only_back = None
        only_line = None
        min_del_load = (0, 0)
        min_pick_up_load = (0, 0)
        for c, r in enumerate(routes):
            min_del_load = (c, r["Delivery Load"]) if r["Delivery Load"] < min_del_load[1] and \
                                                      r["Delivery Load"] != 0 and r["Pick-up Load"] != 0 \
                                                      or (min_del_load[1] == 0 and r["Pick-up Load"] != 0) \
                                                      else min_del_load
            min_pick_up_load = (c, r["Pick-up Load"]) if r["Pick-up Load"] < min_pick_up_load[1] and \
                                                         r["Pick-up Load"] != 0 and r["Delivery Load"] != 0 \
                                                         or (min_pick_up_load[1] == 0 and r["Delivery Load"] != 0) \
                                                         else min_pick_up_load
            if r["Delivery Load"] == 0:
                only_back = (c, r)
            if r["Pick-up Load"] == 0:
                only_line = (c, r)

        if only_line:
            c, line = only_line
            cost = 0
            delivery = 0
            for i, v in enumerate(line["Vertex Sequence"][1:-1]):
                cost += distances[line["Vertex Sequence"][i]][v] if line["Vertex Sequence"][i] < v \
                        else distances[v][line["Vertex Sequence"][i]]
                if customers[v - 1][2] + delivery + min_del_load[1] <= deposit[3]:
                    delivery += customers[v-1][2]
                else:
                    break

            # add values to min delivery route
            min_head = routes[min_del_load[0]]["Vertex Sequence"][1]
            min_head_cost = distances[min_head][line["Vertex Sequence"][i]] \
                                                       if min_head < line["Vertex Sequence"][i] \
                                                       else distances[line["Vertex Sequence"][i]][min_head]
            routes[min_del_load[0]]["Cost"] += (cost + min_head_cost -
                                                distances[0][routes[min_del_load[0]]["Vertex Sequence"][1]])
            routes[min_del_load[0]]["Delivery Load"] += delivery
            routes[min_del_load[0]]["Vertex Sequence"] = line["Vertex Sequence"][:(i+1)] + \
                                                         routes[min_del_load[0]]["Vertex Sequence"][1:]
            routes[min_del_load[0]]["Customers in Route"] += line["Vertex Sequence"][:(i+1)].__len__() - 1

            # remove values from delivery only route
            if routes[c]["Customers in Route"] - i < 3:
                if c < min_pick_up_load[0]:
                    min_pick_up_load = (min_pick_up_load[0] - 1, min_pick_up_load[1])
                del routes[c]
            else:
                routes[c]["Cost"] += distances[0][routes[c]["Vertex Sequence"][i + 1]] - cost
                routes[c]["Delivery Load"] -= delivery
                routes[c]["Vertex Sequence"] = [0] + routes[c]["Vertex Sequence"][(i + 1):]
                routes[c]["Customers in Route"] -= i

        if only_back:
            c, line = only_back
            cost = 0
            pick_up = 0
            pick_up_line = line["Vertex Sequence"].copy()
            pick_up_line.reverse()
            pick_up_line = pick_up_line[1:-1]
            for i, v in enumerate(pick_up_line):
                cost += distances[line["Vertex Sequence"][-i - 1]][v] if line["Vertex Sequence"][-i - 1] < v \
                    else distances[v][line["Vertex Sequence"][-i - 2]]
                if customers[v-1][2] + pick_up + min_pick_up_load[1] <= deposit[3]:
                    pick_up += customers[v-1][2]
                else:
                    break

            # add values to min distance route (min distance from tail of pick_up only route)
            min_tail = routes[min_pick_up_load[0]]["Vertex Sequence"][-2]
            min_head_cost = distances[min_tail][line["Vertex Sequence"][-i - 2]] \
                                                       if min_tail < line["Vertex Sequence"][-i - 2] \
                                                       else distances[line["Vertex Sequence"][-i - 2]][min_tail]
            routes[min_pick_up_load[0]]["Cost"] += (cost + min_head_cost -
                                                    distances[0][routes[min_pick_up_load[0]]["Vertex Sequence"][-2]])
            routes[min_pick_up_load[0]]["Pick-up Load"] += pick_up
            routes[min_pick_up_load[0]]["Vertex Sequence"] = routes[min_pick_up_load[0]]["Vertex Sequence"][:-1] + \
                                                        line["Vertex Sequence"][(-i - 2):]
            routes[min_pick_up_load[0]]["Customers in Route"] += line["Vertex Sequence"][(-i - 2):].__len__() - 1

            # remove values from pick-up only route
            if routes[c]["Customers in Route"] - i < 3:
                del routes[c]
            else:
                routes[c]["Cost"] += distances[0][routes[c]["Vertex Sequence"][-i - 3]] - cost
                routes[c]["Pick-up Load"] -= pick_up
                routes[c]["Vertex Sequence"] = routes[c]["Vertex Sequence"][:(-i - 2)] + [0]
                routes[c]["Customers in Route"] -= (i + 1)

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
