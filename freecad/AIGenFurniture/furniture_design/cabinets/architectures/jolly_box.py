# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the AIGenFurniture addon.
from .base_box import BaseBox
from ..elements.accessory import Accessory

class JollyBox(BaseBox):
    def __init__(self, label, height, width, depth, rules):
        super().__init__(label, height, width, depth, rules)
        self.append(Accessory("surub 3.5x16", 8))  # prentu glisiere
        self.append(Accessory("surub 3.5x16", 8))  # pentru front
        if width < 150:
            raise NameError("ERROR: Jolly basket for cabinet ", self.label, "not available!")
        elif width < 200:
            self.append(Accessory("Joly150500", 1))
        elif width < 300:
            self.append(Accessory("Joly240500", 1))
        else:
            self.append(Accessory("Joly300500", 1))

        self.add_front([[100, 100]], "door")