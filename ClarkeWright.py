from math import sqrt, pow
import os, time, random

filespath = 'C:\\Users\\Giacomo\\Desktop\\University\\Magistrale Informatica\\1 ANNO\\DS\\I19\\Instanze simmetriche CVRPB\\Instances'
files = [(x if x[-3:] == "txt" and x != "info.txt" else None) for x in os.listdir(filespath)]


def main():
    choice = -1
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

                while choice != 0 and choice != 1:
                    choice = int(input("0 -> Parallel Clarke & Wright\n"
                                   "1 -> Sequential Clarke & Wright\n"))
                comp_time = time.perf_counter()
                if choice == 0:
                    routes = parallel_CVRP(vehicles, deposit, customers, distances, savings, backhauls)
                else:
                    routes = sequential_CVRP(vehicles, deposit, customers, distances, savings, backhauls)

                comp_time = time.perf_counter() - comp_time

                fileprint(filename, routes, deposit, customers, vehicles, comp_time)


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
                        if r["Vertex Sequence"].__len__() != 3:
                            if routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                new_route = (new_route[1], -1)
                                if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                        customers[s[0][0]-1][2] == 0:
                                    new_route = (new_route[0], c)
                                    break
                        else:
                            if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or \
                                    customers[s[0][0] - 1][2] != 0:
                                new_route = (c, new_route[1])
                            elif routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                new_route = (new_route[1], c)
                    else:
                        if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                customers[s[0][0]-1][2] == 0:
                            new_route = (new_route[0], c)
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                            # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
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
                        if r["Vertex Sequence"].__len__() != 3:
                            if routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                new_route = (-1, new_route[0])
                                if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or \
                                        customers[s[0][0]-1][2] != 0:
                                    new_route = (c, new_route[1])
                                    break
                        else:
                            if customers[routes[new_route[0]]["Vertex Sequence"][-2] - 1][2] != 0 or \
                                    customers[s[0][0] - 1][2] == 0:
                                new_route = (new_route[0], c)
                            elif routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                new_route = (c, new_route[0])
                    else:
                        if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or \
                                customers[s[0][0]-1][2] != 0:
                            new_route = (c, new_route[1])
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                            # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
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
                        if r["Vertex Sequence"].__len__() != 3:
                            if routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                new_route = (new_route[1], -1)
                                if customers[routes[new_route[0]]["Vertex Sequence"][-2] - 1][2] != 0 or \
                                        customers[s[0][1] - 1][2] == 0:
                                    new_route = (new_route[0], c)
                                    break
                        else:
                            if customers[routes[new_route[1]]["Vertex Sequence"][1] - 1][2] == 0 or \
                                    customers[s[0][1] - 1][2] != 0:
                                new_route = (c, new_route[1])
                            elif routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                new_route = (new_route[1], c)
                    else:
                        if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                customers[s[0][1]-1][2] == 0:
                            new_route = (new_route[0], c)
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
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
                        if r["Vertex Sequence"].__len__() != 3:
                            if routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                new_route = (-1, new_route[0])
                                if customers[routes[new_route[1]]["Vertex Sequence"][1] - 1][2] == 0 or \
                                        customers[s[0][1] - 1][2] != 0:
                                    new_route = (c, new_route[1])
                                    break
                        else:
                            if customers[routes[new_route[0]]["Vertex Sequence"][-2] - 1][2] != 0 or \
                                    customers[s[0][1] - 1][2] == 0:
                                new_route = (new_route[0], c)
                            elif routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                new_route = (c, new_route[0])
                    else:
                        if customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0 or customers[s[0][1]-1][2] != 0:
                            new_route = (c, new_route[1])
                            break
                        elif r["Vertex Sequence"].__len__() == 3 and \
                                 routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                            # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                            new_route = (new_route[1], c)
                            break

        if new_route:
            if new_route[0] != -1 and new_route[1] != -1:

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
                            linehauls -= 1
                        else:
                            if less_back:
                                backhauls += 1
                            continue

                    if customers[s[0][0] - 1][2] != 0 and customers[s[0][1] - 1][2] != 0:
                        linehauls -= 1

                    merge_routes(s, new_route, routes)

    # post_processing(routes, vehicles, customers, distances, deposit)

    return routes


def sequential_CVRP(vehicles, deposit, customers, distances, savings, backhauls):
    routes = []
    linehauls = customers.__len__() - backhauls
    line_back = 0

    for i in range(1, customers.__len__() + 1):
        routes.append({
            "Cost": distances[0][i] * 2,
            "Delivery Load": customers[i - 1][2],
            "Pick-up Load": customers[i - 1][3],
            "Customers in Route": 1,
            "Vertex Sequence": [0, i, 0]
        })
    random.shuffle(routes)

    for c, rout in enumerate(routes):
        r = rout
        i = 0
        while i != savings.__len__():
            s = savings[i]
            i += 1

            new_route = None
            snd_sav = -1

            if r["Vertex Sequence"][1] == s[0][0]:
                snd_sav = s[0][1]
                new_route = (-1, c)
            elif r["Vertex Sequence"][-2] == s[0][0]:
                snd_sav = s[0][1]
                new_route = (c, -1)
            elif r["Vertex Sequence"][1] == s[0][1]:
                snd_sav = s[0][0]
                new_route = (-1, c)
            elif r["Vertex Sequence"][-2] == s[0][1]:
                snd_sav = s[0][0]
                new_route = (c, -1)

            if new_route:
                for n, r2_idx in enumerate(range(c+1, routes.__len__())):
                    r2 = routes[r2_idx]
                    if r2["Vertex Sequence"][1] == snd_sav:
                        if new_route[0] == -1:
                            if r2["Vertex Sequence"].__len__() != 3:
                                if routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                    new_route = (new_route[1], -1)
                                    if customers[routes[new_route[0]]["Vertex Sequence"][-2]-1][2] != 0 or \
                                            customers[snd_sav-1][2] == 0:
                                        new_route = (new_route[0], c+n+1)
                                        break
                            else:
                                if customers[snd_sav-1][2] != 0 or \
                                        customers[routes[new_route[1]]["Vertex Sequence"][1]-1][2] == 0:
                                    new_route = (c+n+1, new_route[1])
                                    break
                                elif routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                    new_route = (new_route[1], c+n+1)
                                    break

                        else:
                            if customers[routes[new_route[0]]["Vertex Sequence"][-2] - 1][2] != 0 or \
                                    customers[snd_sav-1][2] == 0:
                                new_route = (new_route[0], c+n+1)
                                break
                            elif r2["Vertex Sequence"].__len__() == 3 and \
                                    routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                new_route = (c+n+1, new_route[0])
                                break

                    elif r2["Vertex Sequence"][-2] == snd_sav:
                        if new_route[1] == -1:
                            if r2["Vertex Sequence"].__len__() != 3:
                                if routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                    new_route = (-1, new_route[0])
                                    if customers[routes[new_route[1]]["Vertex Sequence"][1] - 1][2] == 0 or \
                                            customers[snd_sav - 1][2] != 0:
                                        new_route = (c+n+1, new_route[1])
                                        break
                            else:
                                if customers[routes[new_route[0]]["Vertex Sequence"][-2] - 1][2] != 0 or \
                                        customers[snd_sav - 1][2] == 0:
                                    new_route = (new_route[0], c+n+1)
                                    break
                                elif routes[new_route[0]]["Vertex Sequence"].__len__() == 3:
                                    new_route = (c+n+1, new_route[0])
                                    break
                        else:
                            if customers[routes[new_route[1]]["Vertex Sequence"][1] - 1][2] == 0 or \
                                    customers[snd_sav - 1][2] != 0:
                                new_route = (c+n+1, new_route[1])
                                break
                            elif r2["Vertex Sequence"].__len__() == 3 and \
                                    routes[new_route[1]]["Vertex Sequence"].__len__() == 3:
                                new_route = (new_route[1], c+n+1)
                                break

                if new_route:
                    if new_route[0] != -1 and new_route[1] != -1:

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
                                    linehauls -= 1
                                else:
                                    if less_back:
                                        backhauls += 1
                                    continue

                            if customers[s[0][0] - 1][2] != 0 and customers[s[0][1] - 1][2] != 0:
                                linehauls -= 1

                            merge_routes(s, new_route, routes)
                            if new_route[0] > new_route[1]:
                                routes.insert(new_route[1], routes[new_route[0]-1])
                                del routes[new_route[0]]
                                r = routes[new_route[1]]
                            del savings[i-1]
                            i = 0

    # post_processing(routes, vehicles, customers, distances, deposit)

    return routes


def merge_routes(s, new_route, routes):
    routes[new_route[0]]["Vertex Sequence"] = routes[new_route[0]]["Vertex Sequence"][:-1] + \
                                              routes[new_route[1]]["Vertex Sequence"][1:]
    routes[new_route[0]]["Cost"] += routes[new_route[1]]["Cost"] - s[1]
    routes[new_route[0]]["Delivery Load"] += routes[new_route[1]]["Delivery Load"]
    routes[new_route[0]]["Pick-up Load"] += routes[new_route[1]]["Pick-up Load"]
    routes[new_route[0]]["Customers in Route"] += routes[new_route[1]]["Customers in Route"]
    del routes[new_route[1]]


"""
def post_processing(routes, vehicles, customers, distances, deposit):
    while routes.__len__() != vehicles:
        cap_err = True
        always_empty_line = True
        always_empty_back = True
        line_skip = []
        back_skip = []
        while cap_err:
            init_len = routes.__len__()
            cap_err = False
            only_back = None
            only_line = None
            min_del_load = (-1, deposit[3])
            min_pick_up_load = (-1, deposit[3])
            for c, r in enumerate(routes):
                if r["Delivery Load"] == 0:
                    if not only_back:
                        only_back = (c, r)
                    elif routes[only_back[0]]["Customers in Route"] < r["Customers in Route"]:
                        only_back = (c, r) if routes[only_back[0]]["Pick-up Load"] > r["Pick-up Load"] else only_back

                if r["Pick-up Load"] == 0:
                    if not only_line:
                        only_line = (c, r)
                    elif routes[only_line[0]]["Customers in Route"] < r["Customers in Route"]:
                        only_line = (c, r) if routes[only_line[0]]["Delivery Load"] > r["Delivery Load"] else only_line

            for c, r in enumerate(routes):

                if only_line:
                    min_del_load = (c, r["Delivery Load"]) if r["Delivery Load"] < min_del_load[1] and \
                                                          r["Delivery Load"] != 0 and c != only_line[0] \
                                                          and c not in line_skip else min_del_load

                if only_back:
                    min_pick_up_load = (c, r["Pick-up Load"]) if r["Pick-up Load"] < min_pick_up_load[1] and \
                                                             r["Pick-up Load"] != 0 and c != only_back[0] \
                                                             and c not in back_skip else min_pick_up_load

            min_del_space = deposit[3]
            min_pick_up_space = deposit[3]
            for c, r in enumerate(routes):
                if only_line:
                    min_del_space = r["Delivery Load"] if r["Delivery Load"] < min_del_space and \
                                                      c != min_del_load[0] and c != only_line[0] else min_del_space

                if only_back:
                    min_pick_up_space = r["Pick-up Load"] if r["Pick-up Load"] < min_pick_up_space and \
                                                c != min_pick_up_load[0] and c != only_back[0] else min_pick_up_space

            if only_line:
                c, line = only_line
                cost = 0
                delivery = 0
                valid = False
                sacrifice = False
                i = 0
                for i, v in enumerate(line["Vertex Sequence"][1:-1]):
                    valid = False
                    if customers[v - 1][2] + delivery + min_del_load[1] <= deposit[3]:
                        delivery += customers[v-1][2]
                        valid = True
                    else:
                        break
                    cost += distances[line["Vertex Sequence"][i]][v] if line["Vertex Sequence"][i] < v \
                            else distances[v][line["Vertex Sequence"][i]]

                if line["Vertex Sequence"][1:-1].__len__() == i+1 and valid:
                    i += 1

                next_cust = line["Vertex Sequence"][i+1]
                if i != 0 and next_cust != 0 and customers[next_cust-1][2] > deposit[3]-min_del_space:
                    cap_err = True
                    always_empty_line = False
                    line_skip.append(min_del_load[0])
                    continue
                elif i == 0:
                    sacrifice = True
                    i += 1
                    delivery = customers[line["Vertex Sequence"][i]-1][2]
                    if not always_empty_line:
                        min_del_load = (line_skip[-1], routes[line_skip[-1]]["Delivery Load"])

                line_skip = []
                back_skip = []

                if not sacrifice or not always_empty_line:
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
                    routes[min_del_load[0]]["Customers in Route"] += i

                    # remove values from delivery only route
                    if routes[c]["Customers in Route"] - i == 0:
                        del routes[c]
                    else:
                        distance_i_next = distances[routes[c]["Vertex Sequence"][i+1]][routes[c]["Vertex Sequence"][i]] \
                            if routes[c]["Vertex Sequence"][i+1] < routes[c]["Vertex Sequence"][i] \
                                else distances[routes[c]["Vertex Sequence"][i]][routes[c]["Vertex Sequence"][i + 1]]

                        routes[c]["Cost"] += distances[0][routes[c]["Vertex Sequence"][i + 1]] - cost - distance_i_next
                        routes[c]["Delivery Load"] -= delivery
                        routes[c]["Vertex Sequence"] = [0] + routes[c]["Vertex Sequence"][(i + 1):]
                        routes[c]["Customers in Route"] -= i

                else:
                    last_del = routes[c]["Vertex Sequence"][1]
                    last_del_load = customers[last_del-1][2]
                    min_sacr = (-1, customers[last_del-1][2])
                    for x, r in enumerate(routes):
                        if deposit[3] > r["Delivery Load"] - customers[r["Vertex Sequence"][1]-1][2] + last_del_load:
                            if customers[r["Vertex Sequence"][1]-1][2] < min_sacr[1]:
                                min_sacr = (x, customers[r["Vertex Sequence"][1]-1][2])

                    # finire lo scambio delle teste con calcolo costi e delivery
                    routes[c]["Delivery Load"] -= (customers[last_del-1][2] - min_sacr[1])
                    routes[min_sacr[0]]["Delivery Load"] -= (min_sacr[1] - customers[last_del-1][2])
                    min_sacr_seq = routes[min_sacr[0]]["Vertex Sequence"]
                    dist_x_next = distances[min_sacr_seq[1]][min_sacr_seq[2]] \
                        if min_sacr_seq[1] < min_sacr_seq[2] else distances[min_sacr_seq[2]][min_sacr_seq[1]]
                    dist_c_next = distances[last_del][routes[c]["Vertex Sequence"][2]] \
                        if last_del < routes[c]["Vertex Sequence"][2] \
                        else distances[routes[c]["Vertex Sequence"][2]][last_del]
                    routes[min_sacr[0]]["Cost"] += (distances[0][last_del] + dist_c_next -
                        distances[0][min_sacr_seq[1]] - dist_x_next)
                    routes[c]["Cost"] += (- distances[0][last_del] - dist_c_next +
                        distances[0][min_sacr_seq[1]] + dist_x_next)
                    routes[c]["Vertex Sequence"][1] = routes[min_sacr[0]]["Vertex Sequence"][1]
                    routes[min_sacr[0]]["Vertex Sequence"][1] = last_del

            if only_back:
                if routes.__len__() != init_len:
                    if only_line[0] < min_pick_up_load[0]:
                        min_pick_up_load = (min_pick_up_load[0] - 1, min_pick_up_load[1])

                d, line = only_back
                cost = 0
                pick_up = 0
                pick_up_line = [x for x in line["Vertex Sequence"]]
                pick_up_line.reverse()
                sacrifice = False
                valid = False
                j = 0
                for j, v in enumerate(pick_up_line[1:-1]):
                    valid = False
                    if customers[v-1][3] + pick_up + min_pick_up_load[1] <= deposit[3]:
                        pick_up += customers[v-1][3]
                        valid = True
                    else:
                        break
                    cost += distances[line["Vertex Sequence"][-j - 1]][v] if line["Vertex Sequence"][-j - 1] < v \
                        else distances[v][line["Vertex Sequence"][-j - 1]]

                if line["Vertex Sequence"][1:-1].__len__() == j+1 and valid:
                    j += 1

                next_cust = line["Vertex Sequence"][-j - 2]
                if next_cust != 0 and customers[next_cust - 1][3] > deposit[3] - min_pick_up_space:
                    cap_err = True
                    back_skip.append(min_pick_up_load[0])
                    continue
                elif j == 0:
                    sacrifice = True
                    j += 1
                    pick_up = customers[line["Vertex Sequence"][-j -1]][3]
                    if not always_empty_back:
                        min_pick_up_load = (back_skip[-1], routes[back_skip[-1]]["Pick-up Load"])

                line_skip = []
                back_skip = []

                if not sacrifice or not always_empty_back:
                    # add values to min distance route (min distance from tail of pick_up only route)
                    min_tail = routes[min_pick_up_load[0]]["Vertex Sequence"][-2]
                    min_head_cost = distances[min_tail][line["Vertex Sequence"][-j - 1]] \
                                                               if min_tail < line["Vertex Sequence"][-j - 1] \
                                                               else distances[line["Vertex Sequence"][-j - 1]][min_tail]
                    routes[min_pick_up_load[0]]["Cost"] += (cost + min_head_cost -
                                                            distances[0][routes[min_pick_up_load[0]]["Vertex Sequence"][-2]])
                    routes[min_pick_up_load[0]]["Pick-up Load"] += pick_up
                    routes[min_pick_up_load[0]]["Vertex Sequence"] = routes[min_pick_up_load[0]]["Vertex Sequence"][:-1] + \
                                                                line["Vertex Sequence"][(-j - 1):]
                    routes[min_pick_up_load[0]]["Customers in Route"] += line["Vertex Sequence"][(-j - 1):].__len__() - 1

                    # remove values from pick-up only route
                    if routes[d]["Customers in Route"] - j == 0:
                        del routes[d]
                    else:
                        distance_j_next = distances[routes[d]["Vertex Sequence"][-j-1]][routes[d]["Vertex Sequence"][-j-2]]\
                            if routes[d]["Vertex Sequence"][-j - 1] < routes[d]["Vertex Sequence"][-j - 2] \
                            else distances[routes[d]["Vertex Sequence"][-j - 2]][routes[d]["Vertex Sequence"][-j - 1]]

                        routes[d]["Cost"] += distances[0][routes[d]["Vertex Sequence"][-j - 2]] - cost - distance_j_next
                        routes[d]["Pick-up Load"] -= pick_up
                        routes[d]["Vertex Sequence"] = routes[d]["Vertex Sequence"][:(-j - 1)] + [0]
                        routes[d]["Customers in Route"] -= j

                else:
                    last_pick_up = routes[d]["Vertex Sequence"][1]
                    last_pick_up_load = customers[last_pick_up-1][3]
                    min_sacr = (-1, customers[last_pick_up-1][3])
                    for x, r in enumerate(routes):
                        if deposit[3] > r["Pick-up Load"] - customers[r["Vertex Sequence"][1]-1][3] + last_pick_up_load:
                            if customers[r["Vertex Sequence"][1]-1][3] < min_sacr[1]:
                                min_sacr = (x, customers[r["Vertex Sequence"][1]-1][3])

                    # finire lo scambio delle teste con calcolo costi e delivery
                    routes[d]["Pick-up Load"] -= (customers[last_pick_up-1][3] - min_sacr[1])
                    routes[min_sacr[0]]["Pick-up Load"] -= (min_sacr[1] - customers[last_pick_up-1][3])
                    min_sacr_seq = routes[min_sacr[0]]["Vertex Sequence"]
                    dist_x_next = distances[min_sacr_seq[1]][min_sacr_seq[2]] \
                        if min_sacr_seq[1] < min_sacr_seq[2] else distances[min_sacr_seq[2]][min_sacr_seq[1]]
                    dist_c_next = distances[last_pick_up][routes[d]["Vertex Sequence"][2]] \
                        if last_pick_up < routes[d]["Vertex Sequence"][2] \
                        else distances[routes[d]["Vertex Sequence"][2]][last_pick_up]
                    routes[min_sacr[0]]["Cost"] += (distances[0][last_pick_up] + dist_c_next -
                        distances[0][min_sacr_seq[1]] - dist_x_next)
                    routes[d]["Cost"] += (- distances[0][last_pick_up] - dist_c_next +
                        distances[0][min_sacr_seq[1]] + dist_x_next)
                    routes[d]["Vertex Sequence"][1] = routes[min_sacr[0]]["Vertex Sequence"][1]
                    routes[min_sacr[0]]["Vertex Sequence"][1] = last_pick_up
"""


def fileprint(output, routes, deposit, customers, vehicles, comp_time):
    with open(output[:-4] + "out" + output[-4:], "w") as file:
        file.write("PROBLEM DETAILS:\n")
        file.write("Customers = " + str(customers.__len__()) + '\n')
        file.write("Max Load = " +str(deposit[3]) + '\n')
        file.write("Max Cost = 999999999999999\n\n")
        file.write("SOLUTION DETAILS:\n")
        file.write("Total Cost = " + str(sum(i["Cost"] for i in routes)) + '\n')
        file.write("Routes Of the Solution = " + str(vehicles) + '\n')
        file.write("Computational Time = " + str(comp_time) + " s" '\n\n')
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
