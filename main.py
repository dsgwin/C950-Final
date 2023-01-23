from locations import *
from packagemgmt import *

# Import the CSV package data
# The resulting package_table is a hash table
package_table = create_package_table('data\package_data.csv')

# Import CSV distance data
# The resulting object is a graph
distance_graph = create_graph('data\distance_map.csv')

# Initialize variable for total distance traveled along route
total_route_distance = 0

# Manually load trucks with list packages and initial departure time in hours, minutes
truck_a = Truck([1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40, 19], 8, 0)
truck_c = Truck([2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33], 9, 5)

# At 10:20 the address for package 9 is updated
package_nine = package_table.look_up(9)
package_nine.address = '410 S State St'
package_nine.zip = 84111
package_table.insert(9, package_nine)

# Truck B is the last truck to leave at 10:20 after the package update
truck_b = Truck([3, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39, 9], 10, 20)

# User get_route function for each truck to determine best route
# and obtain the total distance and final time
truck_a_route = get_route(truck_a, distance_graph, package_table)
truck_b_route = get_route(truck_b, distance_graph, package_table)
truck_c_route = get_route(truck_c, distance_graph, package_table)

# Calculate total distance by adding distance traveled by each truck
total_route_distance += truck_a_route[0]
total_route_distance += truck_b_route[0]
total_route_distance += truck_c_route[0]

print('********WGUPS Package Routing System**********\n')
print("TOTAL DISTANCE TRAVELED: {distance:.2f}\n".format(
    distance = total_route_distance))

# This section determines the time the last truck returns to hub
final_delivery_time = None
if truck_a_route[1] > truck_b_route[1]:    # Compare truck_a time to truck_b
    final_delivery_time = truck_a_route[1] # Assign the greater of the two as final time
else:
    final_delivery_time = truck_b_route[1]

if truck_c_route[1] > final_delivery_time:    # Compare truck_c time to final_delivery_time
    final_delivery_time = truck_c_route[1]    # If greater, assign truck_c_time to variable

print("LAST TRUCK RETURNED TO HUB AT: {}".format(final_delivery_time))

# Method to start the command line interface
def user_interface():
    print()
    print('Please choose an option from the menu below:')
    print('1 - Look up package by ID')
    print('2 - Show status of all packages')
    print('3 - Exit\n')

    user_selection = int(input("Enter selection: ")) # Prompt user for menu input
    while user_selection != 3: # Loop exits if user inputs '3' to quite

        if user_selection == 1:
            id_to_check = int(input('Please enter package ID: '))
            time_to_check = input('Enter time in HH:MM format: ')
            package = package_table.look_up(id_to_check) # Take in user input id and look-up package
            package.update_delivery_status(time_to_check) # Modify package status based on simulated time
            print(package.package_id, package.address, package.city, package.state,
                  package.zip, package.deadline, package.mass, package.status)
            print()
            user_selection = int(input("Please choose another menu option or type 3 to quit: "))

        elif user_selection == 2:
            time_to_check = input('Enter time in HH:MM format: ')
            for package in package_table.table:    # Updates all package status based on simulated input time
                package[0][1].update_delivery_status(time_to_check) # Time complexity: O(N)
            package_table.print_all()
            print()
            user_selection = int(input("Please choose another menu option or type 3 to quit: "))

        else:
            print("\nERROR: Please select a valid option\n")
            print('1 - Look up package by ID')
            print('2 - Show status of all packages')
            print('3 - Exit\n')
            user_selection = int(input("Enter selection: "))

# Call function to begin the user interface
user_interface()
