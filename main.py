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
            self.items[row[0]] = {'Item Manufacturer': row[1], 'Item Type': row[2]}
        print(self.items)
        f.close()

    def append_price_list(self):
        f = open(self.price_filename, 'r')
        reader = csv.reader(f)
        for row in reader:
            for key in self.items:
                if key == row[0]:
                    print("match")
                    self.items[row[0]].update({'Price': row[1]})
        print(self.items)


if __name__ == '__main__':
    x = InventorySystem(manufacturer_filename="ManufacturerList.csv", price_list_filename="PriceList.csv")
    x.get_manufacturer_list()
    x.append_price_list()
