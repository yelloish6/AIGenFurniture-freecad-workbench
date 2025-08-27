import csv, os


class Accessory:
    def __init__(self, name, pieces):
        self.label = name
        self.pieces = pieces
        self.type = "accessory"
        self.obs = ""
        self.price = 0          # default price set to 0

    def print(self):
        print(self.type, ": ", self.label, " Pieces:", self.pieces, " Price: ", self.price, "Obs.: ", self.obs)

    def add_pieces(self, number):
        self.pieces = self.pieces + number

    def add_obs(self, obs):
        self.obs = obs

    def get_price(self):
        """
        this method searches the price_list.csv file for a matching accessory name and returns the matching price.
        :return: price of the accessory
        """
        price_list_path = os.path.join(os.path.dirname(__file__), "price_list.csv")
        with open(price_list_path) as price_list_file:
            price_reader = csv.DictReader(price_list_file, delimiter=',')
            found = False
            for row in price_reader:
                if row["Item"] == self.type and row["Material"] == self.label:
                    found = True
                    return float(row["Price"]) * self.pieces
            if not found:
                print("ERROR: Price for " + self.type + ":" + self.label + " not found. Setting to 0 RON.")
                return 0
