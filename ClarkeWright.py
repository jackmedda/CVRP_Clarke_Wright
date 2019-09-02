from math import sqrt, pow

filename = 'C:\\Users\\Giacomo\\Desktop\\University\\Magistrale Informatica\\1 ANNO\\DS\\I19\\Instanze simmetriche CVRPB\\Instances\\A1.txt'
#filename = input()

def main():

    with open(filename, 'r') as file:
        n_customers = int(file.readline())
        file.readline()
        vehicles = int(file.readline())
        deposit = list(map(int, file.readline().split('   ')))
        customers = []
        for i in range(n_customers):
            customers.append(list(map(int, file.readline().split('   '))))

        savings, distances = compute_savings(deposit, customers)
        savings.sort(key=lambda e: e[1], reverse=True)


def compute_savings(deposit, customers):
    savings = [[]]
    distances = [[]]
    for i in range(1, customers.__len__()+1):
        for j in range(i+1,customers.__len__()+1):
            cost1 = dist(deposit[0], deposit[1], customers[i][0], customers[i][1])
            cost2 = dist(deposit[0], deposit[1], customers[j][0], customers[j][1])
            cost_ij = dist(customers[i][0], customers[i][1], customers[j][0], customers[j][1])
            distances[0][i] = cost1
            distances[0][j] = cost2
            distances[i][j] = cost_ij
            save = cost1 + cost2 - cost_ij
            savings.append([(i, j), save])

    return savings, distances


def parallel_CVRP(vehicles, deposit, customers, distances, savings):
    routes = []

    for i in range(1, customers.__len__()+1):
        routes.append({
            "Cost": distances[0][i]*2,
            "Delivery Load": customers[i][2],
            "Pick-up Load": customers[i][3],
            "Customers in Route": 1,
            "Vertex Sequence": [0, i, 0]
        })

    for s in savings:
        new_route = None
        first = False
        second = False
        for c, r in enumerate(routes):
            if r["Vertex Sequence"][1] == s[0][0] and not first:
                if not new_route:
                    new_route = (-1, c)
                    first = True
                    continue
                # new_route[0] is a linehaul? or s[0][0] is a backhaul
                elif customers[routes[new_route[0]]["Vertex Sequence"][-2]][2] != 0 or customers[s[0][0]][2] == 0:
                    new_route = (new_route[0], c)
                    break
                else:
                    # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                    new_route = (new_route[0], new_route[0])
                    new_route = (c, new_route[0])
                    break

            if r["Vertex Sequence"][-2] == s[0][0] and not first:
                if customers[s[0][0]][2] != 0: # only if linehaul
                    if not new_route:
                        new_route = (c, -1)
                        first = True
                    else:
                        new_route = (c, new_route[1])
                        break
                    """
                    elif customers[routes[new_route[1]]["Vertex Sequence"][1]][2] == 0 or customers[s[0][0]][2] != 0:
                        new_route = (c, new_route[1])
                        break
                    else:
                        # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                        new_route = (new_route[1], new_route[1])
                        new_route = (new_route[0], c)
                        break
                    """

            if r["Vertex Sequence"][1] == s[0][1] and not second:
                if not new_route:
                    new_route = (-1, c)
                    second = True
                    continue
                # new_route[0] is a linehaul? or s[0][1] is a backhaul
                elif customers[routes[new_route[0]]["Vertex Sequence"][-2]][2] != 0 or customers[s[0][1]][2] == 0:
                    new_route = (new_route[0], c)
                    break
                else:
                    new_route = (new_route[0], new_route[0])
                    new_route = (c, new_route[0])
                    break

            if r["Vertex Sequence"][-2] == s[0][1] and not second:
                if customers[s[0][1]][2] != 0: # only if linehaul
                    if not new_route:
                        new_route = (c, -1)
                        second = True
                    else:
                        new_route = (c, new_route[1])
                        break
                    """ in case "if customers[s[0][1]][2] != 0" is not present
                    elif customers[routes[new_route[1]]["Vertex Sequence"][1]][2] == 0 or customers[s[0][1]] != 0:
                        new_route = (c, new_route[1])
                        break
                    else:
                        # 0-backhaul-linehaul-0 --> 0-linehaul-backhaul-0
                        new_route = (new_route[1], new_route[1])
                        new_route = (new_route[0], c)
                        break
                    """

        routes[new_route[0]]["Vertex Sequence"] = routes[new_route[0]]["Vertex Sequence"][:-1] + routes[new_route[1]]["Vertex Sequence"][1:]

        [(1,2), 50000]


def dist(xA, yA, xB, yB):
    return sqrt( pow(xA-xB, 2) + pow(yA-yB, 2) )

if __name__ == "__main__":
    main()
