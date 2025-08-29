from AIGenFurniture.furniture_design.cabinets.elements.accessory import *
from AIGenFurniture.furniture_design.cabinets.elements.board import *
from AIGenFurniture.furniture_design.cabinets.cabinet import Cabinet

class Banca(Cabinet):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)

        gap_fata = 50
        gap_spate = 0
        gap_lat = 50
        height_baza = 100

        lat1 = BoardPal(self.label + ".lat1", height - self.thick_pal, depth, self.thick_pal, "1", "", "1", "")
        lat1.rotate("y")
        lat1.move("x", self.thick_pal)
        #lat1.move("y", self.thick_pal)
        #lat1.rotate("z")
        self.append(lat1)

        lat2 = BoardPal(self.label + ".lat2", height - self.thick_pal, depth, self.thick_pal, "1", "", "1", "")
        lat2.rotate("y")
        #lat2.rotate("z")
        lat2.move("x", self.width)
        #lat2.move("y", gap_fata)
        self.append(lat2)

        jos = BoardPal(self.label + ".jos", width - (2 * self.thick_pal), depth, self.thick_pal, "", "", "", "")
        jos.move("z", height_baza - self.thick_pal)
        jos.move("x", self.thick_pal)
        #jos.move("y", gap_fata)
        #jos.rotate("z")
        self.append(jos)

        pol1 = BoardPal(self.label + ".pol1", int((width - (3 * self.thick_pal)) / 2), depth, self.thick_pal,
                       "2", "", "", "")
        pol1.move("z", int(height * 2/3))
        pol1.move("x", self.thick_pal)
        #pol1.move("y", gap_fata)
        self.append(pol1)

        sep_v = BoardPal(self.label + ".sep_v", height - height_baza - self.thick_pal, depth - self.cant,
                         self.thick_pal, "2", "", "", "")
        sep_v.rotate("y")
        sep_v.move("z", height_baza)
        sep_v.move("x", 2 * self.thick_pal + pol1.length)
        #sep_v.move("y", gap_fata)
        self.append(sep_v)

        pol2 = BoardPal(self.label + ".pol2", int((width - (3 * self.thick_pal)) / 2), depth - self.cant,
                        self.thick_pal, "2", "", "", "")
        pol2.move("z", int(height * 2/3))
        pol2.move("x", 2 * self.thick_pal + pol1.length)
        #pol2.move("y", gap_fata)
        self.append(pol2)

        plinta1 = BoardPal(self.label + ".plinta1", depth, height_baza, self.thick_pal, "2", "2", "", "")
        plinta1.rotate("x")
        plinta1.rotate("z")
        plinta1.rotate("z")
        plinta1.rotate("z")
        #plinta1.move("y", gap_fata)
        plinta1.move("x", - self.thick_pal)
        self.append(plinta1)

        plinta2 = BoardPal(self.label + ".plinta2", depth, height_baza, self.thick_pal, "2", "2", "", "")
        plinta2.rotate("x")
        plinta2.rotate("z")
        plinta2.rotate("z")
        plinta2.rotate("z")
        #plinta2.move("y", gap_fata)
        plinta2.move("x", width)
        self.append(plinta2)

        plinta3 = BoardPal(self.label + ".plinta3", width + 2 * self.thick_pal, height_baza, self.thick_pal, "2", "2",
                           "2", "2")
        plinta3.rotate("x")
        #plinta3.move("y", gap_fata)
        plinta3.move("x", - self.thick_pal)
        self.append(plinta3)

        blat = BoardPal(self.label + ".blat", width + 2 * gap_lat, depth + gap_fata, self.thick_pal, "2", "2", "2", "2")
        blat.move("z", height - self.thick_pal)
        blat.move("x", - gap_lat)
        blat.move("y", - gap_fata)
        self.append(blat)

        self.add_pfl()

        self.append(Accessory("eurosurub 7x50", 10))
        self.append(Accessory("surub 3.5x30", 14))
        self.append(Accessory("demontabil cama", 6))
        self.append(Accessory("L", 2))