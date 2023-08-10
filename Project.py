# Cynthia Meadows
# UH id 2143325
# CIS 2348

import csv
import datetime
# csv module is mentioned on zyBooks 9.7
# datetime module research is documented on line 106


class Item:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged


class Manufacturer:
    def __init__(self, name):
        self.name = name
        self.items = []


def read_csv_file(filename):
    with open(filename, newline='') as csvfile:
        return list(csv.reader(csvfile))


def create_inventory():
    # To read the input files
    manufacturer_data = read_csv_file("ManufacturerList.csv")[1:]  # Skipping the header row
    price_data = read_csv_file("PriceList.csv")[1:]
    service_data = read_csv_file("ServiceDatesList.csv")[1:]

    # First create a dictionary to store manufacturers
    manufacturers = {}

    # Then populate the manufacturer dictionary with items from the ManufacturerList
    for row in manufacturer_data:
        item_id, manufacturer_name, item_type, damaged = row
        item = Item(item_id, manufacturer_name, item_type, None, None, damaged)
        manufacturers.setdefault(manufacturer_name, Manufacturer(manufacturer_name)).items.append(item)

    # Populate the item price from the PriceList
    for row in price_data:
        item_id, item_price = row
        for manufacturer in manufacturers.values():
            for item in manufacturer.items:
                if item.item_id == item_id:
                    item.price = item_price
                    break

    # Populate the service date from the ServiceDatesList
    for row in service_data:
        item_id, service_date = row
        for manufacturer in manufacturers.values():
            for item in manufacturer.items:
                if item.item_id == item_id:
                    item.service_date = service_date
                    break

    return manufacturers


def generate_full_inventory(manufacturers):
    # First sort the inventory alphabetically by manufacturer
    sorted_manufacturers = sorted(manufacturers.values(), key=lambda x: x.name)
    # I researched for a way to sort dictionaries, and found this website
    # https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/
    # the website also mentions itemgetter but I didn't want to import another module

    # Then generate the FullInventory.csv file
    with open('FullInventory.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Damaged'])
        for manufacturer in sorted_manufacturers:
            for item in manufacturer.items:
                writer.writerow(
                    [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date, item.damaged])


def generate_device_inventory(manufacturers):
    # First generate inventory files for each device type
    devices = set(item.item_type for manufacturer in manufacturers.values() for item in manufacturer.items)

    for item_type in devices:
        file_name = f'{item_type}Inventory.csv'
        device_type = []
        for manufacturer in manufacturers.values():
            for item in manufacturer.items:
                if item.item_type == devices:
                    device_type.append(item)
        # Then sort devices by Id
        device_type.sort(key=lambda x: x.item_id)
        # Finally generate device inventory file
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Item Id', 'Manufacturer', 'Price', 'Service Date', 'Damaged'])
            for item in device_type:
                writer.writerow([item.item_id, item.manufacturer, item.price, item.service_date.strftime('%m/%d/%Y'), item.damaged])


def generate_past_service_date_inventory(manufacturers):
    # Get current date first, I used this website to research how to do it
    # https://www.geeksforgeeks.org/get-current-date-using-python/
    # *NOTE* the datetime module had to be imported!
    current_date = datetime.now()

    # To generate the PastServiceDataInventory.csv file
    with open('PastServiceDateInventory.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writenow(['Item Id', 'Manufacturer', 'Item Type', 'Price', 'service Date', 'Damaged'])
        for manufacturer in manufacturers.values():
            for item in manufacturer.items:
                if item.service_date < current_date:
                    writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y'), item.damaged])
                    # datetime module also includes strftime() for easier string representation
                    # https://www.geeksforgeeks.org/python-strftime-function/ used to research the correct syntax


def generate_damaged_inventory(manufacturers):
    # To generate the DamagedInventory.csv file
    with open('DamagedInventory.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item Id', 'Manufacturer', 'Item Type', 'Price', 'service Date', 'Damaged'])
        # Then create a list for the damaged items
        damaged_items = []
        for manufacturer in manufacturers.values():
            for item in manufacturer.items:
                if item.damaged == 'damaged':
                    damaged_items.append(item)
        # Then to sort by price from most expensive to least
        damaged_items.sort(key=lambda x: float(x.price), reverse=True)
        # Now write the items into the csv file
        for item in damaged_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime('%m/%d/%Y')])


manufacturers = create_inventory()
generate_full_inventory(manufacturers)
generate_device_inventory(manufacturers)
generate_past_service_date_inventory(manufacturers)
generate_damaged_inventory(manufacturers)
