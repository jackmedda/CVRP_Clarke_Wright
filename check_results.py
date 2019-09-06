import os

files = [x if x[-3:] == "txt" else None for x in os.listdir()]
errors = 0
for f in files:
    if f:
        with open(f, "r") as file:
            vehicles = 0
            route = 0
            ok = False
            for line in file:

                if line.startswith("Routes"):
                    vehicles = int(line[25])
                    if line[26] != "\n":
                        vehicles = vehicles*10 + int(line[26])
                if line.startswith("ROUTE "):
                    route = int(line[6])
                    if line[7] != ":":
                        route = route*10 + int(line[7])
                if line.startswith("Delivery"):
                    if line[16] == "0":
                        print(f + " route " + str(route) + " Delivery = 0\n")
                if route >= vehicles > 0 and not ok:
                    print(f + " too many routes\n\n")
                    ok = True
                    errors += 1

print("\nErrors = " + str(errors))
