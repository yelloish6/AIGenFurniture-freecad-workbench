# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
import csv, os
from ...pricing.price_manager import PriceManager as pm
from ...accessory_catalog import resolve_accessory

class Accessory:
    def __init__(self, name, pieces, unit=None):
        definition = resolve_accessory(name, unit)
        self.code = definition.code
        self.label = definition.label
        self.unit = definition.unit
        self.legacy_label = name
        self.pricing_key = name
        self.pieces = pieces
        self.type = "accessory"
        self.price = 0
        self.obs = ""

    def print(self):
        print(self.type, ": ", self.label, " Pieces:", self.pieces, " Price: ", self.price, "Obs.: ", self.obs)

    def debug_print(self):
        print(self.type, ": ", self.label, " Pieces:", self.pieces, " Price: ", self.price, "Obs.: ", self.obs)

    def add_pieces(self, number):
        self.pieces = self.pieces + number

    def add_obs(self, obs):
        self.obs = obs

    def get_price(self):
        return pm.get_price_for_item("accessory", self.pricing_key) * self.pieces
