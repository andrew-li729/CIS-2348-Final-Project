# Andrew Li
# 1824794
import csv
from datetime import datetime


class InventorySystem:
    def __init__(self, manufacturer_filename="none", price_list_filename="none",
                 service_filename="none"):
        self.manufacturer_filename = manufacturer_filename
        self.price_filename = price_list_filename
        self.service_filename = service_filename
        self.items = {}

    def get_manufacturer_list(self):
        # initiates dictionary for items in manufacturerList.csv
        # item IDs will be keys and its attributes will be its value in a nested dictionary
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
        return manufacturers_list

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
        return item_ids_sorted

    def write_past_service_date_file(self):
        # gets current date from system
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
            date_compare = datetime.strptime(date, '%m/%d/%Y')  # converts item service date from str to date format
            if date_compare > now:  # compares item service date and system date
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
        return dates_list

    def write_damaged_inventory_file(self):
        item_ids = self.items.keys()
        damaged_list = []
        price_list = []

        for key in item_ids:
            if self.items[key]['Damage Indicator'] == 'damaged':
                damaged_list.append(key)

        for item in damaged_list:
            price_list.append(self.items[item]["Price"])
        # print(damaged_list)
        price_list.sort(reverse=True)
        # print(price_list)

        with open("DamagedInventory.csv", 'w') as f:
            w = csv.writer(f, lineterminator="\n")
            for price in price_list:
                for item in damaged_list:
                    if self.items[item]['Price'] == price:
                        t = [item, self.items[item]['Item Manufacturer'], self.items[item]['Item Type'],
                             self.items[item]['Price'], self.items[item]['Service Date']]
                        w.writerow(t)
        return damaged_list

    def valid_items(self):
        # this function takes full list of item ids and removes ids that are past service date or damaged
        # gets relevant lists from previous functions
        full_item_ids = self.item_type_inventory_file()
        past_service_date_list = self.write_past_service_date_file()
        damaged_item_ids = self.write_damaged_inventory_file()

        # remove damaged ids from list
        for item_id in damaged_item_ids:
            if item_id in full_item_ids:
                full_item_ids.remove(item_id)

        # remove past service date ids
        for date in past_service_date_list:
            for key in full_item_ids:
                if self.items[key]["Service Date"] == date:
                    # print(self.items[key]["Service Date"])
                    full_item_ids.remove(key)
        return full_item_ids

    def query_system(self):
        # get user input to search dict with
        search = input("Enter Item: ")

        # splits search string into a list
        search_split = search.split()

        # gets manufacturers list and item_ids list from previous functions
        manufacturers_list = self.write_full_inv_file()
        item_ids = self.valid_items()

        # creates list without duplicates of all item types from full inventory
        item_types = []
        for key in self.items:
            if self.items[key]["Item Type"] not in item_types:
                item_types.append(self.items[key]["Item Type"])

        # initialize variables used for manufacturer name user input validation
        manufacturer_keyword = None
        manu_flag = False
        count = 0

        # checks if user input has matching value in manufacturers list
        for manufacturer in manufacturers_list:
            if manufacturer in search_split:
                manu_flag = True
                manufacturer_keyword = manufacturer
                count += 1
                if count > 1:
                    print("ERROR: Please enter only 1 manufacturer\n")
                    manu_flag = False
                    manufacturer_keyword = None
                    break

        # initializes variables used for item type user input validation
        type_keyword = None
        item_flag = False
        count = 0

        # checks if user input has matching value in item types list
        for item in item_types:
            if item in search_split:
                item_flag = True
                type_keyword = item
                count += 1
                if count > 1:
                    print("ERROR: Please enter only 1 item type")
                    item_flag = False
                    type_keyword = None
                    break

        # print(manufacturer_keyword, manu_flag)  # for debugging
        # print(type_keyword, item_flag)

        # if both manufacturer and item input checks are true, take user input and find valid matching item from
        # remaining valid item ids (not damaged or past service date)
        if manu_flag and item_flag:
            for key in item_ids:
                if self.items[key]["Item Manufacturer"] == manufacturer_keyword \
                        and self.items[key]["Item Type"] == type_keyword:
                    print("Your item is: {} {} {} ${} \n".format(key,
                                                                 self.items[key]["Item Manufacturer"],
                                                                 self.items[key]["Item Type"],
                                                                 self.items[key]["Price"]))

                    for key2 in item_ids:  # checks item ids for similar items within price range of 20%
                        # print(key2)
                        if type_keyword == self.items[key2]["Item Type"] and key != key2:
                            item_price = float(self.items[key]["Price"])
                            alt_item_price = float(self.items[key2]["Price"])
                            # print(item_price, alt_item_price)

                            item_price_low = item_price - item_price * 0.2
                            item_price_hi = item_price + item_price * 0.2
                            # print(item_price_low, item_price_hi)

                            if item_price_low <= alt_item_price <= item_price_hi:
                                print("You may also consider: {} {} {} ${}\n".
                                      format(key2, self.items[key2]["Item Manufacturer"], self.items[key2]["Item Type"],
                                             self.items[key2]["Price"]))

        else:
            print("Item not found in stock.\n")


if __name__ == '__main__':
    x = InventorySystem(manufacturer_filename="ManufacturerList.csv", price_list_filename="PriceList.csv",
                        service_filename="ServiceDatesList.csv")

    # this part combines the three input files into one output FullInventory.csv file
    x.get_manufacturer_list()
    x.append_price_list()
    x.append_service_date_list()
    x.write_full_inv_file()

    # this part outputs item type files, past service file, and damaged inventory file
    x.item_type_inventory_file()
    x.write_past_service_date_file()
    x.write_damaged_inventory_file()

    x.valid_items()

    option = ""

    while option != "q":
        print("MENU")
        print("a - Query Item")
        print("q - Quit")
        option = input("Choose an option: \n")

        if option == "a":
            x.query_system()
