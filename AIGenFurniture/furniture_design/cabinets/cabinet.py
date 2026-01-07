
from AIGenFurniture.furniture_design.cabinets.assemblies import ASSEMBLIES
from AIGenFurniture.furniture_design.cabinets.features.drawers import DrawersMixin
from AIGenFurniture.furniture_design.cabinets.features.shelves import ShelvesMixin
from AIGenFurniture.furniture_design.cabinets.features.fronts import FrontMixin
from AIGenFurniture.furniture_design.cabinets.features.backs import BackMixin

# TODO default rules must be moved on cabinet level and they don't need to be an argument for the init method.
#  Replace rules with "cabinet_data" as a dictionary for all generic parameters of a cabinet.
# TODO: assembly type to be given as parameter of the cabinet, also directly in FreeCAD, as drop-down

class Cabinet(DrawersMixin, ShelvesMixin, FrontMixin, BackMixin):
    def __init__(self, label, height, width, depth, rules, assembly_type = "euro_screw"):
        """
        collection of boards forming one cabinet
        all items collected in "self.material_list[]"
        :param label: eticheta
        :param height: inaltimea
        :param width: latimea
        :param depth: adancimea
        :param rules: lista de reguli
        """
        self.label = label
        self.height = height
        self.width = width
        self.depth = depth
        self.thick_pal = rules["thick_pal"]
        self.thick_front = rules["thick_front"]
        self.thick_blat = rules["thick_blat"]
        self.width_blat = rules["width_blat"]
        self.cant_lab = rules["cant_general"]
        self.cant = round(rules["cant_general"])
        self.front_gap = float(rules["gap_front"])
        self.pol_depth = rules["pol_depth"]
        self.cant_pol = rules["cant_pol"]
        self.cant_separator = rules["cant_separator"]
        self.elements_list = []
        self.position_list = [] # list of movements for the cabinet to position it in the order
        # self.pal = []
        # self.palOO = []
        # self.pfl = []
        # self.pflOO = []
        # self.front = []
        # self.frontOO = []
        # self.blat = 0
        # self.acc = []
        self.sep_space_h = self.height - (2 * self.thick_pal)
        self.sep_space_w = self.width - (2 * self.thick_pal)
        self.sep_max_depth = depth - self.cant
        self.sep_prev = ""
        # self.arch = []  # matricea de arhitectura care contine elementele corpului orientate si cu offset
        self.cant_length = [['0.4', 0], ['2', 0]]
        self.assembly_type = assembly_type

    def append(self, obj):
        self.elements_list.append(obj)

    def remove_element(self, item_type, label):
        index = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == item_type and self.elements_list[i].label == label:
                index = i
        self.elements_list.pop(index)

    def get_element_list_by_type(self, element_type):
        sub_list = []
        for element in self.elements_list:
            if element.type == element_type:
                sub_list.append(element)
        return sub_list

    def generate_connection_list(self):
        pal_list = self.get_element_list_by_type("pal")
        for i in range(len(pal_list)):
            for j in range(i + 1, len(pal_list)):
                board1 = pal_list[i]
                board2 = pal_list[j]
                
    def auto_assemble(self):
        """
        Go through all elements of the cabinet.
        If both are 'pal' boards and have a valid connection surface,
        assemble them using the cabinet's assembly_type.
        """
        pal_list = self.get_element_list_by_type("pal")
        assembly_func = ASSEMBLIES.get(self.assembly_type)

        if not assembly_func:
            raise ValueError(f"Unknown assembly type: {self.assembly_type}")

        for i in range(len(pal_list)):
            for j in range(i + 1, len(pal_list)):
                b1 = pal_list[i]
                b2 = pal_list[j]
                connection = b1.calculate_connection_surface(b2)
                if connection:  # valid connection
                    try:
                        assembly_func(b1, b2)
                    except Exception as e:
                        print(f"[WARN] Could not assemble {b1.label} with {b2.label}: {e}")

    # def assemble_pal(self, board1, board2, assembly_type, diameter=0, connection_count=2):
    #     """
    #         Calculate the positions where holes should be drilled for assembling two boards and modifies each boards
    #         drill list.
    #
    #         Parameters:
    #         - board1: First board object (with position and size).
    #         - board2: Second board object (with position and size).
    #         - connection_method: Type of connection ("wood_dowel", "eccentric", "euro_screw")
    #         - diameter: Diameter of the drill for the connection method.
    #         - connection_count: The number of holes to drill (default is 2).
    #
    #         Returns: None
    #         """
    #     connection_surface = board1.calculate_connection_surface(board2)
    #     board1_label = board1.__getattribute__("label")
    #     board2_label = board2.__getattribute__("label")
    #
    #     if not connection_surface:
    #         raise ValueError(f"No valid connection surface found between {board1_label} and {board2_label}.")
    #     board1_face = connection_surface['board1_face']
    #     board2_face = connection_surface['board2_face']
    #     x1_min, x1_max, y1_min, y1_max = connection_surface['board1_dim']
    #     x2_min, x2_max, y2_min, y2_max = connection_surface['board2_dim']
    #     connection_length = x1_max - x1_min
    #     connection_width = y1_max - y1_min
    #
    #     if connection_count > 1:
    #         hole_spacing = connection_length / (connection_count + 1) # Uniformly spaced along the connection length
    #     else:
    #         hole_spacing = connection_length / 2 # If only one hole, place it in the middle
    #
    #     if assembly_type == "wood_dowel":
    #
    #         for i in range(1, connection_count + 1):
    #             # Calculate positions for both boards using the same spacing and relative alignment
    #
    #             # For board1
    #             hole_x1 = x1_min + (hole_spacing * i)  # Along the length of the connection
    #             hole_y1 = y1_min + (connection_width / 2) # - (diameter / 2)  # Centered in width
    #             # hole_z1 = offset1_z  # Adjust the z-coordinate based on the face
    #
    #             board1.drill(board1_face, hole_x1, hole_y1, diameter)
    #
    #             hole_x2 = x2_min + (hole_spacing * i)  # Along the length of the connection
    #             hole_y2 = y2_min + (connection_width / 2) # - (diameter / 2)  # Centered in width
    #
    #             board2.drill(board2_face, hole_x2, hole_y2, diameter)
    #
    #     if assembly_type == "eccentric":
    #
    #         for i in range(1, connection_count + 1):
    #             # Calculate positions for both boards using the same spacing and relative alignment
    #
    #             # For board1
    #             hole_x1 = x1_min + (hole_spacing * i)  # Along the length of the connection
    #             hole_y1 = y1_min + (connection_width / 2) + 8 # Centered in width + 8 mm (standard for eccentric)
    #             # hole_z1 = offset1_z  # Adjust the z-coordinate based on the face
    #
    #             board1.drill(board1_face, hole_x1, hole_y1, 25)
    #
    #             hole_x2 = x2_min + (hole_spacing * i)  # Along the length of the connection
    #             hole_y2 = y2_min + (connection_width / 2) # - (diameter / 2)  # Centered in width
    #
    #             board2.drill(board2_face, hole_x2, hole_y2, 5)
    #
    #     else:
    #         print("Assembly type not valid.")

    def get_item_by_type_label(self, typ, lab):
        """

        :param typ: type of item to be returned
        :param lab: label of item to be returned
        :return: index of item found in material_list vector
        """
        index = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == typ and self.elements_list[i].label == lab:
                index = i
        if 'index' in locals():
            return self.elements_list.__getitem__(index)
        else:
            raise NameError("ERROR: element ", lab, " of type ", typ, " not found.")

    def print(self):
        print(f"[cabinet.py] Printing cabinet:")
        print(f"Label: {self.label}")
        print(f"Dimensions: height {self.height}, width {self.width}, depth {self.depth}")
        print(f"Elements list:")
        for element in self.elements_list:
            element.debug_print()

    def get_m2_pal(self):

        m2pal = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == "pal":
                m2pal = m2pal + self.elements_list[i].get_m2()
        return m2pal

    def get_m2_pfl(self):

        m2pfl = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == "pfl":
                m2pfl = m2pfl + self.elements_list[i].get_m2()
        return m2pfl

    def get_m2_front(self):

        m2 = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == "front":
                m2 = m2 + self.elements_list[i].get_m2()
        return m2

    def get_m_cant(self, cant_type):
        """
        :param cant_type: "0.4" sau "2"
        :return: lungimea cantului selectat din tot corpul
        """

        m = 0
        for i in range(len(self.elements_list)):
            if self.elements_list[i].type == "pal":
                m = m + self.elements_list[i].get_m_cant(cant_type)
        return m

    def rotate_corp(self, axis):
        self.position_list.append(["rotate", axis])
        # for i in range(len(self.elements_list)):
        #     if isinstance(self.elements_list[i], Board):
        #         self.elements_list[i].rotate(axis)
        #         initial_position = self.elements_list[i].position
        #         final_position = initial_position
        #         offset_x = initial_position[3]
        #         offset_y = initial_position[4]
        #         offset_z = initial_position[5]
        #         if axis == "x":
        #             final_position[3] = offset_x
        #             final_position[4] = -offset_z
        #             final_position[5] = offset_y
        #         elif axis == "y":
        #             final_position[3] = -offset_z
        #             final_position[4] = offset_y
        #             final_position[5] = offset_x
        #         elif axis == "z":
        #             final_position[3] = offset_y
        #             final_position[4] = -offset_x
        #             final_position[5] = offset_z
        #         self.elements_list[i].position = final_position

    def move_corp(self, axis, offset):
        self.position_list.append(["move", axis, offset])
        # for i in range(len(self.elements_list)):
        #     if isinstance(self.elements_list[i], Board):
        #         self.elements_list[i].move(axis, offset)
