from FinalProject import InventorySystem


class QuerySystem(InventorySystem):
    def __init__(self, inventory):
        super().__init__()
        self.items = inventory.Serv

    def print(self):
        print(self.items)


if __name__ == '__main__':
    y = InventorySystem
    x = QuerySystem(y)
    x.print()
