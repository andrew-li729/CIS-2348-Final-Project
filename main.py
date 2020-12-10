# Andrew Li
# 1824794
import csv
from datetime import datetime


class InventorySystem:
    def __init__(self, manufacturer_filename="ManufacturerList.csv", price_list_filename="none",
                 service_filename="none"):
        self.manufacturer_filename = manufacturer_filename
        self.price_filename = price_list_filename
        self.service_filename = service_filename
        self.items = {}

    def get_manufacturer_list(self):
        f = open(self.manufacturer_filename, 'r')
        reader = csv.reader(f)
        for row in reader:
            self.items[row[0]] = {'Item Manufacturer': row[1], 'Item Type': row[2], 'Damage Indicator': row[3]}
        # print(self.items)
        f.close()

    def append_price_list(self):
        f = open(self.price_filename, 'r')
        reader = csv.reader(f)
        for row in reader:
            for key in self.items:
                if key == row[0]:
                    self.items[row[0]].update({'Price': row[1]})
        # print(self.items)
        f.close()

    def append_service_date_list(self):
        f = open(self.service_filename, 'r')
        reader = csv.reader(f)
        for row in reader:
            for key in self.items:
                if key == row[0]:
                    self.items[row[0]].update({'Service Date': row[1]})
        # print(self.items)
        f.close()

    def write_full_inv_file(self):
        # returns a list containing each item id from items dict
        item_ids = self.items.keys()
        # creates a blank manufacturers list to sort later
        manufacturers_list = []

        # gets manufacturers from items dict and puts them in previously created list
        for key in item_ids:  # iterates through each key in item_ids list
            if self.items[key]['Item Manufacturer'] not in manufacturers_list:
                manufacturers_list.append(self.items[key]['Item Manufacturer'])

        # sorts manufacturers list alphabetically
        manufacturers_list.sort()
        # print(manufacturers_list)
        with open("FullInventory.csv", 'w') as f:
            w = csv.writer(f, lineterminator='\n')
            for manu in manufacturers_list:
                for key in self.items:
                    if self.items[key]["Item Manufacturer"] == manu:
                        t = [key, self.items[key]["Item Manufacturer"], self.items[key]["Item Type"],
                             self.items[key]["Price"], self.items[key]["Service Date"],
                             self.items[key]["Damage Indicator"]]
                        w.writerow(t)

    def item_type_inventory_file(self):
        # get item ids and sort
        item_ids = self.items.keys()
        item_ids_sorted = []
        for item_id in item_ids:
            item_ids_sorted.append(item_id)
        item_ids_sorted.sort()
        # print(item_ids_sorted)

        # get item types and store in list
        item_types_list = []
        for key in item_ids_sorted:
            if self.items[key]['Item Type'] not in item_types_list:
                item_types_list.append(self.items[key]['Item Type'])
        # print(item_types_list)

        for item_type in item_types_list:  # for each item type create an accordingly named csv file
            with open(item_type + "Inventory.csv", 'w') as f:  # takes item type from list to name file
                w = csv.writer(f, lineterminator='\n')
                for item_id in item_ids_sorted:  # iterates thru sorted list of item ids
                    if self.items[item_id]["Item Type"] == item_type:  # if item type of item id matches item type list
                        t = [item_id, self.items[item_id]["Item Manufacturer"],
                             self.items[item_id]["Price"], self.items[item_id]["Service Date"],
                             self.items[item_id]["Damage Indicator"]]
                        w.writerow(t)

    def write_past_service_date_file(self):
        # gets current date
        now = datetime.now()

        # get item ids from items dict
        item_ids = self.items.keys()
        dates_list = []

        # populates dates_list with dates from items dict without duplicates
        for key in item_ids:
            if self.items[key]['Service Date'] not in dates_list:
                dates_list.append(self.items[key]['Service Date'])

        # removes service date from dates_list if it has passed when program is executed
        for date in dates_list:
            date_compare = datetime.strptime(date, '%m/%d/%Y')
            if date_compare > now:
                dates_list.remove(date)

        # sorts dates list
        dates_list.sort(key=lambda date: datetime.strptime(date, '%m/%d/%Y'))

        # writes to file if date from items dict is in dates_list
        with open("PastServiceDateInventory.csv", 'w') as f:
            w = csv.writer(f, lineterminator='\n')
            for date in dates_list:
                for key in self.items:
                    if self.items[key]["Service Date"] == date:
                        t = [key, self.items[key]["Item Manufacturer"], self.items[key]["Item Type"],
                             self.items[key]["Price"], self.items[key]["Service Date"],
                             self.items[key]["Damage Indicator"]]
                        w.writerow(t)

    def write_damaged_inventory_file(self):
        item_ids = self.items.keys()
        damaged_list = []
        price_list = []

        for key in item_ids:
            if self.items[key]['Damage Indicator'] == 'damaged':
                damaged_list.append(key)

        for item in damaged_list:
            price_list.append(self.items[item]["Price"])
        print(damaged_list)
        price_list.sort(reverse=True)
        print(price_list)

        with open("DamagedInventory.csv", 'w') as f:
            w = csv.writer(f, lineterminator="\n")
            for price in price_list:
                for item in damaged_list:
                    if self.items[item]['Price'] == price:
                        t = [item, self.items[item]['Item Manufacturer'], self.items[item]['Item Type'],
                             self.items[item]['Price'], self.items[item]['Service Date']]
                        w.writerow(t)


if __name__ == '__main__':
    x = InventorySystem(manufacturer_filename="ManufacturerList.csv", price_list_filename="PriceList.csv",
                        service_filename="ServiceDatesList.csv")
    x.get_manufacturer_list()
    x.append_price_list()
    x.append_service_date_list()
    x.write_full_inv_file()
    x.item_type_inventory_file()
    x.write_past_service_date_file()
    x.write_damaged_inventory_file()
