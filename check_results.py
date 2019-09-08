import os
from math import sqrt

files = [x if x[-3:] == "txt" else None for x in os.listdir()]
errors = 0
counter = 0

filespath = 'C:\\Users\\Giacomo\\Desktop\\University\\Magistrale Informatica\\1 ANNO\\DS\\I19\\Instanze simmetriche CVRPB\\Instances'
files_inst = [(x if x[-3:] == "txt" and x != "info.txt" else None) for x in os.listdir(filespath)]

def dist(xA, yA, xB, yB):
    return sqrt( pow(xA-xB, 2) + pow(yA-yB, 2) )

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

for filename in files_inst:
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

for f in files:
    if f:
        with open(f, "r") as file:
            vehicles = 0
            route = 0
            max_load = 0
            delivery_load = 0
            pickup_load = 0
            num_customers = 0
            customers = []
            ok = False
            for line in file:

                if line.startswith("Customers = "):
                    tmp = line.split(' = ')
                    num_customers = int(tmp[1])

                if line.startswith("Max Load"):
                    tmp = line.split(' = ')
                    max_load = int(tmp[1])

                if line.startswith("Routes"):
                    vehicles = int(line[25])
                    if line[26] != "\n":
                        vehicles = vehicles*10 + int(line[26])

                if line.startswith("ROUTE "):
                    route = int(line[6])
                    if line[7] != ":":
                        route = route*10 + int(line[7])

                if line.startswith("0"):
                    tmp = line.split(" ")
                    for cust in tmp:
                        customers.append(int(cust))
                    customers = list(dict.fromkeys(customers))
                    customers.sort()
                    customers.remove(0)
                # if customers.__len__() == num_customers:
                #     print (f + " Number Of Customers -> " + str(customers.__len__()))

                if line.startswith("Delivery"):
                    tmp = line.split(' = ')
                    delivery_load = int(tmp[1])
                    if line[16] == "0":
                        print(f + " route " + str(route) + " Delivery = 0\n")
                    elif delivery_load > max_load:
                        print(f + "route " + str(route) + "Delivery EXCEED -> " + str(max_load) + "<" + str(delivery_load))

                if line.startswith("Pick-Up"):
                    tmp = line.split(' = ')
                    pickup_load = int(tmp[1])
                    if pickup_load > max_load:
                        print(f + "route " + str(route) + "Delivery EXCEED -> " + str(max_load) + "<" + str(pickup_load))

                if route >= vehicles > 0 and not ok:
                    print(f + " too many routes\n\n")
                    ok = True
                    errors += 1
            else:
                if (customers.__len__() != num_customers):
                    counter = counter + 1
                    print (f + "  Missing customer ->" + str(customers.__len__()) + " -> Number of missing: " + \
                           str(num_customers - customers.__len__()))
                    print ("\n")
                    print (customers)
                    print ("\n")

print("\nErrors = " + str(errors))
print("\nElements missing in # istances = " + str(counter))
