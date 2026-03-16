class Resident:
    def __init__(self, flat_number, name, apartment_type, family_members,
                 parking_slot, water_units, electricity_units,
                 gym=False, pool=False, is_senior=False):
        self.flat_number = flat_number
        self.name = name
        self.apartment_type = apartment_type
        self.family_members = family_members
        self.parking_slot = parking_slot
        self.water_units = water_units
        self.electricity_units = electricity_units
        self.gym = gym
        self.pool = pool
        self.is_senior = is_senior
        self.bill_amount = 0
        self.paid = False


class MaintenanceCalculator:
    BASE_MAINTENANCE = {"1BHK": 2000, "2BHK": 3000, "3BHK": 4000}
    PARKING_CHARGE = 500
    GYM_CHARGE = 500
    POOL_CHARGE = 300

    @staticmethod
    def calculate_electricity_charge(units):
        if units <= 100:
            return units * 5
        elif units <= 200:
            return (100 * 5) + ((units - 100) * 7)
        else:
            return (100 * 5) + (100 * 7) + ((units - 200) * 9)

    @staticmethod
    def calculate_water_charge(units):
        if units <= 50:
            return units * 20
        elif units <= 100:
            return (50 * 20) + ((units - 50) * 25)
        else:
            return (50 * 20) + (50 * 25) + ((units - 100) * 30)

    @classmethod
    def calculate_bill(cls, resident, early_payment=False):
        base = cls.BASE_MAINTENANCE[resident.apartment_type]
        water = cls.calculate_water_charge(resident.water_units)
        electricity = cls.calculate_electricity_charge(resident.electricity_units)
        parking = cls.PARKING_CHARGE
        facilities = (cls.GYM_CHARGE if resident.gym else 0) + \
                     (cls.POOL_CHARGE if resident.pool else 0)

        total = base + water + electricity + parking + facilities

        if resident.is_senior:
            total *= 0.9   # 10% discount

        if early_payment:
            total *= 0.95  # 5% discount

        return round(total, 2)


class ApartmentManagement:
    def __init__(self):
        self.residents = []

    def add_resident(self, resident):
        self.residents.append(resident)

    def generate_all_bills(self, early_payment=False):
        for r in self.residents:
            r.bill_amount = MaintenanceCalculator.calculate_bill(r, early_payment)

    def mark_paid(self, flat_number):
        for r in self.residents:
            if r.flat_number == flat_number:
                r.paid = True

    def get_pending_list(self):
        return [r for r in self.residents if not r.paid]

    def display_individual_bills(self):
        print("\nINDIVIDUAL BILLS")
        for r in self.residents:
            status = "PAID" if r.paid else "UNPAID"
            print(f"Flat {r.flat_number} | {r.name} | Rs.{r.bill_amount} | {status}")

    def generate_summary_report(self):
        total_revenue = sum(r.bill_amount for r in self.residents if r.paid)
        unpaid = len(self.get_pending_list())
        highest = max(self.residents, key=lambda r: r.bill_amount).bill_amount

        print("\nMONTHLY SUMMARY REPORT")
        print("Total Revenue Collected:", total_revenue)
        print("Unpaid Residents:", unpaid)
        print("Highest Bill:", highest)

        if unpaid > 0:
            print("Pending Payments:")
            for r in self.get_pending_list():
                print(f"Flat {r.flat_number} - {r.name}")


# ---------------- MAIN PROGRAM ----------------
management = ApartmentManagement()

n = int(input("Enter number of residents: "))

for i in range(n):
    print(f"\nEnter details for Resident {i+1}")

    flat = input("Flat Number: ")
    name = input("Name: ")
    apt = input("Apartment Type (1BHK/2BHK/3BHK): ")
    family = int(input("Family Members: "))
    parking = input("Parking Slot: ")
    water = int(input("Water Units: "))
    electricity = int(input("Electricity Units: "))

    gym = input("Gym (yes/no): ").lower() == "yes"
    pool = input("Pool (yes/no): ").lower() == "yes"
    senior = input("Senior Citizen (yes/no): ").lower() == "yes"

    resident = Resident(flat, name, apt, family, parking,
                        water, electricity, gym, pool, senior)

    management.add_resident(resident)

early = input("\nEarly payment discount? (yes/no): ").lower() == "yes"
management.generate_all_bills(early)

paid_count = int(input("\nHow many residents paid? "))
for _ in range(paid_count):
    flat_no = input("Enter flat number paid: ")
    management.mark_paid(flat_no)

management.display_individual_bills()
management.generate_summary_report()


