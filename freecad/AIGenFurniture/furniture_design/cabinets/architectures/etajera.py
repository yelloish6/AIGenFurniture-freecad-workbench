# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.accessory import *
from ..elements.board import *
from ..cabinet import Cabinet

class Etajera(Cabinet):
    def __init__(self, label, height, width, depth, rules, shelves):
        super().__init__(label, height, width, depth, rules)

        lat1 = BoardPal(self.label + ".left_side", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab, self.cant_lab)
        lat1.rotate_cw("y")
        lat1.move("x", self.thick_pal)
        self.append(lat1)

        lat2 = BoardPal(self.label + ".right_side", self.height, self.depth, self.thick_pal, self.cant_lab, "", self.cant_lab, self.cant_lab)
        lat2.rotate_cw("y")
        lat2.move("x", width)
        self.append(lat2)

        sus = BoardPal(self.label + ".top", self.width - (2 * self.thick_pal), self.depth,
                       self.thick_pal, self.cant_lab, "", "", "")
        sus.move("z", height - self.thick_pal)
        sus.move("x", self.thick_pal)
        self.append(sus)

        jos = BoardPal(self.label + ".bottom", self.width - (2 * self.thick_pal), self.depth,
                       self.thick_pal, self.cant_lab, "", "", "")
        jos.move("x", self.thick_pal)
        self.append(jos)

        self.add_pfl()

        self.append(Accessory("eurosurub 7x50", 8))

        self.add_pol(shelves)
