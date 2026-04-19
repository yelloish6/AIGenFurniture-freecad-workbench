# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from ..elements.board import Pfl
from ..elements.accessory import Accessory


class BackMixin:
    def remove_all_pfl(self):
        # TODO BUGFIX - scoate doar ultimul PFL, nu toate.
        index = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == "pfl":
                index = i
        if index != 0:
            self.elements_list.pop(index)


    def add_pfl(self):
        placa = Pfl(self.label + ".hdf", self.width - 4, self.height - 4)
        placa.rotate("x")
        placa.move("y", self.depth + 1 + 4)
        placa.move("x", 2)
        placa.move("z", 2)
        self.append(placa)
        self.append(Accessory("surub PFL", 2 * round(self.height / 150) + 2 * round(self.width / 150)))