import csv, os
from AIGenFurniture.furniture_design.pricing.price_manager import PriceManager as pm

class Accessory:
    def __init__(self, name, pieces):
        self.label = name
        self.pieces = pieces
        self.type = "accessory"
        self.price = 0
        self.obs = ""

    def print(self):
        print(self.type, ": ", self.label, " Pieces:", self.pieces, " Price: ", self.price, "Obs.: ", self.obs)

    def add_pieces(self, number):
        self.pieces = self.pieces + number

    def add_obs(self, obs):
        self.obs = obs

    def get_price(self):
        return pm.get_price_for_item("accessory", self.label) * self.pieces


