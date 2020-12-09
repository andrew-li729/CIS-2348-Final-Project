# Andrew Li
# 1824794
import csv


class InventorySystem:
    def __init__(self, manufacturer_filename="ManufacturerList.csv", price_list_filename="none", service_filename="none"):
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


if __name__ == '__main__':
    x = InventorySystem(manufacturer_filename="ManufacturerList.csv", price_list_filename="PriceList.csv",
                        service_filename="ServiceDatesList.csv")
    x.get_manufacturer_list()
    x.append_price_list()
    x.append_service_date_list()
    x.write_full_inv_file()
