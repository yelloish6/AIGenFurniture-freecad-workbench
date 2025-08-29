import math

from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet
from AIGenFurniture.furniture_design.cabinets.elements.accessory import Accessory
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal, Blat

class BaseCornerShelf(Cabinet):
    def __init__(self, label, height, width, depth, shelves, rules, rounded=False):
        super().__init__(label, height, width, depth, rules)

        back1 = BoardPal(self.label + ".back1", self.height, self.width - self.thick_pal, self.thick_pal, 1, 1, 1, 0)
        back1.rotate("y")
        back1.rotate("z")
        back1.move("x", self.thick_pal)
        back1.move("y", self.depth - self.thick_pal)
        self.append(back1)

        back2 = BoardPal(self.label + ".back2", self.height, self.depth, self.thick_pal, 1, 0, 1, 0)
        back2.rotate("y")
        self.append(back2)
        back2.move("x", self.thick_pal)
        self.append(Accessory("surub", 2))

        base = BoardPal(self.label + ".base", self.width - self.thick_pal, self.depth - self.thick_pal, self.thick_pal, 0, 0, 0, 0)
        # base.add_obs("decupaj rotund cu raza de " + str(min(self.width, self.depth) - self.thick_pal))
        # round coordinates:
        # x = radius * Math.sin(Math.PI * 2 * angle / 360);
        #
        # y = radius * Math.cos(Math.PI * 2 * angle / 360);
        #
        if rounded:
            radius = min(self.width, self.depth) - self.thick_pal
            base.add_obs("decupaj rotund cu raza de " + str(radius))
            base.cut_coords = [
                [0, 0],
                [radius * math.sin(math.radians(15)), radius - (radius * math.cos(math.radians(15)))],
                [radius * math.sin(math.radians(2 * 15)), radius - (radius * math.cos(math.radians(2 * 15)))],
                [radius * math.sin(math.radians(3 * 15)), radius - (radius * math.cos(math.radians(3 * 15)))],
                [radius * math.sin(math.radians(4 * 15)), radius - (radius * math.cos(math.radians(4 * 15)))],
                [radius * math.sin(math.radians(5 * 15)), radius - (radius * math.cos(math.radians(5 * 15)))],
                [base.length, radius],
                [base.length, base.width],
                [0, base.width]
            ]
        base.move("x", self.thick_pal)
        self.append(base)
        self.append(Accessory("surub", 4))

        for i in range(shelves):
            shelf = BoardPal(self.label + ".shelf", self.width  - self.thick_pal, self.depth  - self.thick_pal, self.thick_pal, 0, 0, 0, 0)
            if rounded:
                radius = min(self.width, self.depth) - self.thick_pal
                shelf.add_obs("decupaj rotund cu raza de " + str(radius))
                shelf.cut_coords = [
                    [0, 0],
                    [radius * math.sin(math.radians(15)), radius - (radius * math.cos(math.radians(15)))],
                    [radius * math.sin(math.radians(2 * 15)), radius - (radius * math.cos(math.radians(2 * 15)))],
                    [radius * math.sin(math.radians(3 * 15)), radius - (radius * math.cos(math.radians(3 * 15)))],
                    [radius * math.sin(math.radians(4 * 15)), radius - (radius * math.cos(math.radians(4 * 15)))],
                    [radius * math.sin(math.radians(5 * 15)), radius - (radius * math.cos(math.radians(5 * 15)))],
                    [shelf.length, radius],
                    [shelf.length, shelf.width],
                    [0, shelf.width]
                ]
            # shelf.add_obs("decupaj rotund cu raza de " + str(min(self.width, self.depth) - self.thick_pal))
            shelf.move("z", ((self.height - ((shelves + 1) * self.thick_pal))/(shelves+1))*(i+1) + self.thick_pal)
            shelf.move("x", self.thick_pal)
            self.append(shelf)
            self.append(Accessory("surub", 4))
