from AIGenFurniture.furniture_design.cabinets.Kitchen.base_box import BaseBox
from AIGenFurniture.furniture_design.cabinets.elements.board import BoardPal


class SinkBox(BaseBox):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)
        self.remove_all_pfl()
        # for i in self.getPFLOO():
        #    if self.getPFLOO()[i].__getattribute__("label") == self.label + ".pfl":
        #        self.getPFLOO().pop()
        # self.getPFLOO().pop(self.getPFLOO()[0])
        leg_width = 100
        legatura = BoardPal(self.label + ".leg", self.width - (2 * self.thick_pal), leg_width, self.thick_pal,
                            self.cant_lab, "", "", "")
        legatura.move("x", self.thick_pal)
        legatura.move("z", self.thick_pal)
        legatura.move("y", self.depth - self.thick_pal)
        legatura.rotate("x")
        legatura.move("y", legatura.thick)
        self.append(legatura)

        leg1 = self.get_item_by_type_label("pal", self.label + ".leg1")
        leg1.rotate("x")
        leg1.move("y", leg1.thick)
        leg1.move("z", self.thick_pal - leg1.width)

        leg2 = self.get_item_by_type_label("pal", self.label + ".leg2")
        leg2.rotate("x")
        leg2.move("y", leg2.thick)
        leg2.move("z", self.thick_pal - leg2.width)
        leg2.move("y", leg2.width - self.thick_pal)
