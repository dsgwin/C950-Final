import csv, HashTable
from datetime import timedelta

# Implement Package Class to manage package information
# Data members of class map to CSV columns
class Package:

    # Constructor function to initialize the object with needed parameters
    def __init__(self, package_id, address, city, state, zip, deadline, mass, notes=None):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        if 'Delayed' in self.notes:
            self.status = 'Delayed'
        else:
            self.status = 'At Hub'
        self.depart_time = ''
        self.delivery_time = 'Not Delivered'

    # Update_delivery_status function updates the delivery status of a package based on time
    def update_delivery_status(self, time):
        time = time.split(":")
        h = int(time[0])
        m = int(time[1])
        time = timedelta(hours=h, minutes=m)
        if self.delivery_time < time:
            self.status = "Delivered: {}".format(self.delivery_time)
        elif self.depart_time < time:
            self.status = "En route"
        else:
            self.status = "At Hub"

# Add truck class
class Truck:
    # Constructor function to load the packages and specify the departure time of the truck
    def __init__(self,packages, start_time_hour, start_time_minutes):
        if len(packages) > 16:     # Ensures that truck capacity is not exceeded
            print("Truck capacity may not exceed 16 parcels")
        else:
            self.packages = packages
        self.packages = packages
        self.distance = 0                     # Starting distance of 0
        self.hub = '4001 South 700 East'
        self.location = self.hub              # Starting Location at WGUPS Hub
        self.start_time = timedelta(hours=start_time_hour, minutes=start_time_minutes)
        self.current_time = self.start_time
        self.avg_speed = 18

    # This function updates the current_time of the truck with a float value of hours as input.
    def update_time(self, time_hours):
       self.current_time = self.current_time + timedelta(hours = time_hours)



# This is a helper function to parse the CSV data, insert it into the hash table, and return the hash table
# Space-time complexity is O(N) as it iterates through N rows of a CSV
def create_package_table(filename):
    #Initialize empty list to hold package objects before insertion into hash table
    packages = []
    with open(filename, 'r') as packagesCSV:
        for row in csv.reader(packagesCSV, delimiter=','):
            packages.append(Package(int(row[0]),row[1],
                                    row[2],row[3],int(row[4]),row[5],int(row[6]),row[7]))

    # Create instance of hash table based on number of packages
    package_table = HashTable.HashTable(len(packages))
    for package in packages:
        package_table.insert(package.package_id, package)
    return package_table

# The get_route function will determine the best route for the packages on the truck
# This utilizes the nearest-neighbor algorithm
# Space-time complexity is O(N^2) due to nested loop
def get_route(truck, graph, package_table):
    undelivered_packages = []               # Initialize empty undelivered pacakge list
    route = []                              # Initialize empty route list that packages will be placed in
    for id in truck.packages:               # Place each package from the truck into undelivered list
        package = package_table.look_up(id)
        undelivered_packages.append(package)

    while len(undelivered_packages) > 0:    # Loop will continue until all packages have been removed
        min_distance = 500                  # Arbitrary high value for initial comparison
        next_package = None
        for package in undelivered_packages:
            # Compare distance of truck location with the address of the package
            if graph.compare_distance(truck.location, package.address) <= min_distance:
                # If the distance is the lowest, the min_distance variable is updated
                # and the next_package to be delivered is assigned
                min_distance = graph.compare_distance(truck.location, package.address)
                next_package = package

        # Add the package ID to the truck route list
        route.append(next_package.package_id)

        # Remove the package from the undelivered list
        undelivered_packages.remove(next_package)

        # Update the distance traveled by the truck
        truck.distance = truck.distance + min_distance

        # Update the truck's location to the next package address to continue loop
        truck.location = next_package.address

        # Update the time of the truck based on the start time and the distance/avg speed.
        truck.update_time(min_distance/truck.avg_speed)

        # Updates the departure time of package with start time of truck
        next_package.depart_time = truck.start_time

        # Updates the package delivery time
        next_package.delivery_time = truck.current_time

    # Add time traveled back to hub to total time
    truck.update_time(graph.compare_distance(truck.location, truck.hub)/truck.avg_speed)

    # Add distance traveled back to the hub to truck's total distance
    truck.distance = truck.distance + graph.compare_distance(truck.location, truck.hub)


    # Return the total distance and final  from the route
    return truck.distance, truck.current_time

