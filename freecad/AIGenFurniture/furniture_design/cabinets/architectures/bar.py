# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.accessory import Accessory
from ..elements.board import BoardPal, Blat
from ..cabinet import Cabinet

class Bar(Cabinet):
    def __init__(self, label, height, width, depth, rules, front_clearance=50, back_clearance=0):
        super().__init__(label, height, width, depth, rules)
        self.front_clearance = front_clearance
        self.back_clearance = back_clearance
        inner_depth = self.depth - self.front_clearance - self.back_clearance
        if inner_depth <= 0:
            raise ValueError("Bar clearances must be smaller than cabinet depth.")
        self.append(Accessory("surub", 14))

        # arhitectura
        lat1 = BoardPal(self.label + ".lat1", self.height, inner_depth,
                        self.thick_pal, self.cant_lab, self.cant_lab, self.cant_lab, "")
        lat1.rotate_cw("y")
        lat1.move("x", self.thick_pal)
        lat1.move("y", self.front_clearance)
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat2", self.height, inner_depth,
                        self.thick_pal, self.cant_lab, self.cant_lab, self.cant_lab, "")
        lat2.rotate_cw("y")
        lat2.move("x", self.width)
        lat2.move("y", self.front_clearance)
        self.append(lat2)

        leg1 = BoardPal(self.label + ".leg1", self.width - (2 * self.thick_pal), 100, self.thick_pal,
                        self.cant_lab, self.cant_lab, "", "")
        leg1.move("z", lat1.length - leg1.thick)
        leg1.move("x", lat1.thick)
        leg1.move("y", self.front_clearance)
        self.append(leg1)

        leg2 = BoardPal(self.label + ".leg2", self.width - (2 * self.thick_pal), 100, self.thick_pal,
                        self.cant_lab, self.cant_lab, "", "")
        leg2.move("z", lat1.length - leg2.thick)
        leg2.move("y", self.depth - self.back_clearance - leg2.width)
        leg2.move("x", lat1.thick)
        self.append(leg2)

        spate = BoardPal(self.label + ".spate", self.height, self.width - 2 * self.thick_pal,
                         self.thick_pal, self.cant_lab, "", "", "")
        spate.rotate("x")
        spate.rotate_cw("y")
        spate.rotate_cw("y")
        spate.rotate_cw("y")
        spate.move("z", self.height)
        spate.move("y", self.depth - self.back_clearance)  # - self.thick_pal
        spate.move("x", self.thick_pal)
        self.append(spate)

        bl = Blat(self.label + ".blat", self.width, self.depth, self.thick_blat)
        bl.move("z", self.height)
        self.append(bl)
