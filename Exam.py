# Write a complete Python program for a Smart City Parking Management System using Object-Oriented Programming.
# The program must:
# Use classes and constructors.
# Define appropriate classes (for example, ParkingZone and Vehicle).
# Include methods for vehicle entry, vehicle exit, fee calculation, and checking available slots.
# Create parking zones such as Mall, Hospital, and Railway Station.
# Each zone should have limited slots for two-wheelers and cars.
# On vehicle entry:
# Accept vehicle number, vehicle type (two-wheeler or car), and zone name.

# Check slot availability.

# Assign an available slot.

# On vehicle exit:

# Record exit time.

# Calculate parking duration.
# Apply a fixed charge for the first hour and an additional charge for every extra hour.
# Free the slot.
# Use a loop-based menu system that repeatedly shows:
# Vehicle Entry
# Vehicle Exit
# Check Available Slots
# Exit System
# Maintain total number of vehicles parked and total revenue collected.
# Display a summary report at the end.
# Use conditional statements, loops, lists or dictionaries where required.
# Write clean, well-structured, fully working Python code with proper comments.
# Smart City Parking Management System
# Using Object-Oriented Programming

from datetime import datetime
import math

# Class to represent a parking zone
class ParkingZone:
    def __init__(self, name, car_slots, bike_slots):
        # Initialize zone details
        self.name = name
        self.car_slots = car_slots
        self.bike_slots = bike_slots
        
        # Track available slots
        self.available_car_slots = car_slots
        self.available_bike_slots = bike_slots
        
        # Dictionary to store parked vehicles (vehicle_number : Vehicle object)
        self.parked_vehicles = {}


# Class to represent a vehicle
class Vehicle:
    def __init__(self, number, vehicle_type, zone):
        # Initialize vehicle details
        self.number = number
        self.vehicle_type = vehicle_type
        self.zone = zone
        
        # Record entry time automatically
        self.entry_time = datetime.now()


# Function to calculate parking fee
def calculate_fee(hours):
    # First hour charge = ₹20
    # Additional hour charge = ₹10 per hour
    if hours <= 1:
        return 20
    else:
        return 20 + (hours - 1) * 10


# Create parking zones with limited slots
zones = {
    "Mall": ParkingZone("Mall", 10, 15),
    "Hospital": ParkingZone("Hospital", 8, 12),
    "Railway": ParkingZone("Railway", 12, 20)
}

# Variables to track total vehicles and revenue
total_vehicles = 0
total_revenue = 0


# Main menu loop
while True:
    print("\n----- Smart City Parking System -----")
    print("1. Vehicle Entry")
    print("2. Vehicle Exit")
    print("3. Check Available Slots")
    print("4. Exit")

    # Take user choice
    choice = input("Enter your choice: ")

    # ---------------- VEHICLE ENTRY ----------------
    if choice == "1":
        number = input("Enter Vehicle Number: ")
        vehicle_type = input("Enter Vehicle Type (car/two-wheeler): ")
        zone_name = input("Enter Zone (Mall/Hospital/Railway): ")

        # Check if zone exists
        if zone_name in zones:
            zone = zones[zone_name]

            # Check slot availability for car
            if vehicle_type == "car" and zone.available_car_slots > 0:
                vehicle = Vehicle(number, vehicle_type, zone_name)
                zone.parked_vehicles[number] = vehicle  # Store vehicle
                zone.available_car_slots -= 1           # Reduce slot
                total_vehicles += 1
                print("Car parked successfully.")

            # Check slot availability for two-wheeler
            elif vehicle_type == "two-wheeler" and zone.available_bike_slots > 0:
                vehicle = Vehicle(number, vehicle_type, zone_name)
                zone.parked_vehicles[number] = vehicle
                zone.available_bike_slots -= 1
                total_vehicles += 1
                print("Two-wheeler parked successfully.")

            else:
                print("No slots available for this vehicle type.")
        else:
            print("Invalid Zone Name.")

    # ---------------- VEHICLE EXIT ----------------
    elif choice == "2":
        number = input("Enter Vehicle Number: ")

        found = False  # Flag to check if vehicle exists

        # Search vehicle in all zones
        for zone in zones.values():
            if number in zone.parked_vehicles:
                vehicle = zone.parked_vehicles[number]
                exit_time = datetime.now()

                # Calculate parking duration in hours
                duration = exit_time - vehicle.entry_time
                hours = math.ceil(duration.total_seconds() / 3600)

                # Calculate fee
                fee = calculate_fee(hours)
                total_revenue += fee

                # Free slot based on vehicle type
                if vehicle.vehicle_type == "car":
                    zone.available_car_slots += 1
                else:
                    zone.available_bike_slots += 1

                # Remove vehicle from parked list
                del zone.parked_vehicles[number]

                print("Parking Duration:", hours, "hours")
                print("Parking Fee: ₹", fee)
                print("Vehicle exited successfully.")

                found = True
                break

        if not found:
            print("Vehicle not found.")

    # ---------------- CHECK AVAILABLE SLOTS ----------------
    elif choice == "3":
        for zone in zones.values():
            print(f"{zone.name} - Cars: {zone.available_car_slots}, "
                  f"Two-wheelers: {zone.available_bike_slots}")

    # ---------------- EXIT SYSTEM ----------------
    elif choice == "4":
        print("\n----- Summary Report -----")
        print("Total Vehicles Parked:", total_vehicles)
        print("Total Revenue Collected: ₹", total_revenue)
        print("Thank you for using Smart City Parking System!")
        break

    else:
        print("Invalid Choice. Please try again.")
 




    
