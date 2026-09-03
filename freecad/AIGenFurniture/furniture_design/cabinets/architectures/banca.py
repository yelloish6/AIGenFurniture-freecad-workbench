# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.accessory import *
from ..elements.board import *
from ..cabinet import Cabinet

class Banca(Cabinet):
    def __init__(self, label, height, width, depth, rules, gap_front = 50, gap_lat = 50, height_base = 100):
        super().__init__(label, height, width, depth, rules)

        lat1 = BoardPal(self.label + ".left_side", height - self.thick_pal, depth, self.thick_pal, "1", "", "1", "")
        lat1.rotate_cw("y")
        lat1.move("x", self.thick_pal)
        #lat1.move("y", self.thick_pal)
        #lat1.rotate("z")
        self.append(lat1)

        lat2 = BoardPal(self.label + ".right_side", height - self.thick_pal, depth, self.thick_pal, "1", "", "1", "")
        lat2.rotate_cw("y")
        #lat2.rotate("z")
        lat2.move("x", self.width)
        #lat2.move("y", gap_fata)
        self.append(lat2)

        jos = BoardPal(self.label + ".bottom", width - (2 * self.thick_pal), depth, self.thick_pal, "", "", "", "")
        jos.move("z", height_base - self.thick_pal)
        jos.move("x", self.thick_pal)
        #jos.move("y", gap_fata)
        #jos.rotate("z")
        self.append(jos)

        pol1 = BoardPal(self.label + ".shelf_1", int((width - (3 * self.thick_pal)) / 2), depth, self.thick_pal,
                       "2", "", "", "")
        pol1.move("z", int(height * 2/3))
        pol1.move("x", self.thick_pal)
        #pol1.move("y", gap_fata)
        self.append(pol1)

        sep_v = BoardPal(self.label + ".vertical_separator_1", height - height_base - self.thick_pal, depth - self.cant,
                         self.thick_pal, "2", "", "", "")
        sep_v.rotate_cw("y")
        sep_v.move("z", height_base)
        sep_v.move("x", 2 * self.thick_pal + pol1.length)
        #sep_v.move("y", gap_fata)
        self.append(sep_v)

        pol2 = BoardPal(self.label + ".shelf_2", int((width - (3 * self.thick_pal)) / 2), depth - self.cant,
                        self.thick_pal, "2", "", "", "")
        pol2.move("z", int(height * 2/3))
        pol2.move("x", 2 * self.thick_pal + pol1.length)
        #pol2.move("y", gap_fata)
        self.append(pol2)

        plinta1 = BoardPal(self.label + ".plinth_1", depth, height_base, self.thick_pal, "2", "2", "", "")
        plinta1.rotate("x")
        plinta1.rotate("z")
        #plinta1.move("y", gap_fata)
        plinta1.move("x", - self.thick_pal)
        self.append(plinta1)

        plinta2 = BoardPal(self.label + ".plinth_2", depth, height_base, self.thick_pal, "2", "2", "", "")
        plinta2.rotate("x")
        plinta2.rotate("z")
        #plinta2.move("y", gap_fata)
        plinta2.move("x", width)
        self.append(plinta2)

        plinta3 = BoardPal(self.label + ".plinth_3", width + 2 * self.thick_pal, height_base, self.thick_pal, "2", "2",
                           "2", "2")
        plinta3.rotate("x")
        #plinta3.move("y", gap_fata)
        plinta3.move("x", - self.thick_pal)
        self.append(plinta3)

        blat = BoardPal(self.label + ".top", width + 2 * gap_lat, depth + gap_front, self.thick_pal, "2", "2", "2", "2")
        blat.move("z", height - self.thick_pal)
        blat.move("x", - gap_lat)
        blat.move("y", - gap_front)
        self.append(blat)

        self.add_pfl()

        self.append(Accessory("eurosurub 7x50", 10))
        self.append(Accessory("surub 3.5x30", 14))
        self.append(Accessory("demontabil cama", 6))
        self.append(Accessory("L", 2))
