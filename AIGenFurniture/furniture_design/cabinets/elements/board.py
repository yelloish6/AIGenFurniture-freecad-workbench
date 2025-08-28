import csv, os
# TODO add a method to cut-out boards, and add the effect in all output files

DEFAULT_SHEET_LENGTH = 2800
DEFAULT_SHEET_WIDTH = 2070
DEFAULT_LOSS = 0.1


class Board:
    def __init__(self, label, length, width, thick, cut_coords=None):
        """
        :param label: eticheta
        :param length: lungimea
        :param width: latimea
        :param thick: grosimea
        :param cut_coords: optional parameter for defining irregular shape boards
        """

        self.label = label
        self.length = length
        self.width = width
        self.thick = thick
        self.obs = ""
        self.position = [self.length,  # dim x
                         self.width,  # dim y
                         self.thick,  # dim z
                         0,  # offset x
                         0,  # offset y
                         0]  # offset z
        self.type = ""  # pal, pfl, front
        self.material = ""
        self.price = 0
        self.position_list = [] #
        self.cut_coords = cut_coords

        self.check_board()

    def add_obs(self, text):
        """
        append text to obs attribute
        :param text: string to be appended
        :return: n/a
        """
        self.obs = self.obs + text

    def set_material(self, material):
        self.material = material

    def rotate(self, axis):
        """
        rotate the plank by 90 deg on the specified axis. dimensions are re-set to match the rotated position
        :param axis: axis to rotate around ("x"/"y"/"z")
        :return: n/a
        """
        self.position_list.append(["rotate", axis])

        init_x = self.position[0]
        init_y = self.position[1]
        init_z = self.position[2]
        if axis == "x":
            self.position[0] = init_x
            self.position[1] = -init_z
            self.position[2] = init_y
        # TODO: rotation of a board is clockwise for X and counterclockwise for Y and Z. Make all clockwise, in line with FreeCAD
        # elif axis == "x":
        #     self.position[0] = init_x
        # elif axis == "y":
        #     self.position[0] = init_z
        #     self.position[1] = init_y
        #     self.position[2] = -init_x
        elif axis == "y":
            self.position[0] = -init_z
            self.position[1] = init_y
            self.position[2] = init_x
        # elif axis == "z":
        #     self.position[0] = -init_y
        #     self.position[1] = init_x
        #     self.position[2] = init_z
        elif axis == "z":
            self.position[0] = init_y
            self.position[1] = -init_x
            self.position[2] = init_z
        else:
            self.position[0] = init_x
            self.position[1] = init_y
            self.position[2] = init_z

    def move(self, axis, offset):
        """
        move a plank on a specified axis, by a specified amount
        :param axis: axis to move on
        :param offset: amount to move by
        :return: n/a
        """
        self.position_list.append(["move", axis, offset])
        if axis == "x":
            self.position[3] = self.position[3] + int(offset)
        if axis == "y":
            self.position[4] = self.position[4] + int(offset)
        if axis == "z":
            self.position[5] = self.position[5] + int(offset)

    def get_m2(self):
        return float(self.length * self.width / 1000000)

    def print(self):
        print(f"Board type {self.type}, {self.label}, [{self.length} x {self.width} x {self.thick}], {self.material}, "
              f"position {self.position}")

    def calculate_connection_surface(board1, board2):
        """
        Calculate the surface where board1 and board2 connect, including perpendicular assemblies.

        Parameters:
        - board1: First board object (with position and size).
        - board2: Second board object (with position and size).

        Returns:
        - A dictionary describing the connection surface:
          - 'board1_face': Which face of board1 is involved (e.g., 'top', 'bottom', 'left', etc.).
          - 'board2_face': Which face of board2 is involved (e.g., 'top', 'bottom', 'left', etc.).
          - 'board1_dim': x_min, x_max, Y_min, y_max as a rectangle of the projection of the connection area on the respective face of the board.
          - 'dimensions': The length and width of the connection surface.
          - 'offset': The (x, y, z) coordinates of the connection surface start in the global cabinet space.
        """

        # Extract position and size of board1
        length1, width1, thickness1, offset1_x, offset1_y, offset1_z = board1.position
        print(board1.position_list)

        # Extract position and size of board2
        length2, width2, thickness2, offset2_x, offset2_y, offset2_z = board2.position
        print(board2.position_list)

        # Calculate bounding boxes for each board in the global coordinate system
        box1 = {
            'x_min': min(offset1_x, offset1_x + length1),
            'x_max': max(offset1_x, offset1_x + length1),
            'y_min': min(offset1_y, offset1_y + width1),
            'y_max': max(offset1_y, offset1_y + width1),
            'z_min': min(offset1_z, offset1_z + thickness1),
            'z_max': max(offset1_z, offset1_z + thickness1),
        }

        box2 = {
            'x_min': min(offset2_x, offset2_x + length2),
            'x_max': max(offset2_x, offset2_x + length2),
            'y_min': min(offset2_y, offset2_y + width2),
            'y_max': max(offset2_y, offset2_y + width2),
            'z_min': min(offset2_z, offset2_z + thickness2),
            'z_max': max(offset2_z, offset2_z + thickness2),
        }

        # Check for perpendicular assemblies (where one board's face connects to another's edge)
        # Case A: board1's bottom connects to board2's front face
        if box1['z_min'] == box2['z_max'] and \
                (box1['x_min'] < box2['x_max'] and box1['x_max'] > box2['x_min']) and \
                (box1['y_min'] < box2['y_max'] and box1['y_max'] > box2['y_min']):
            return {
                'board1_face': 'down',  # board1's bottom face
                'board2_face': 'front',  # board2's top face
                'dimensions': (length1, width1),  # Connect along length and width of the face
                'offset': (offset1_x, offset1_y, offset1_z)  # Starting point of connection
            }

        # Case E: board1's front connects to board2's up side (perpendicular assembly)
        if box1['x_max'] == box2['x_min'] and \
                (box1['z_min'] < box2['z_max'] and box1['z_max'] > box2['z_min']) and \
                (box1['y_min'] < box2['y_max'] and box1['y_max'] > box2['y_min']):
            return {
                'board1_face': 'front',  # board1's back face
                'board1_dim': (offset2_y, offset2_y + width2, offset2_z, offset2_z + thickness2), # x min, x max, y min, y max
                'board2_face': 'up',  # board2's left face
                'board2_dim': (0, width2, 0, thickness2),
            }

        # Case G: board1's back connects to board2's down side (perpendicular assembly)
        if box1['x_min'] == box2['x_max'] and \
                (box1['z_min'] < box2['z_max'] and box1['z_max'] > box2['z_min']) and \
                (box1['y_min'] < box2['y_max'] and box1['y_max'] > box2['y_min']):
            return {
                'board1_face': 'back',  # board1's back face
                'board1_dim': (offset2_y, offset2_y + width2, offset2_z, offset2_z + thickness2), # x min, x max, y min, y max
                'board2_face': 'down',  # board2's left face
                'board2_dim': (0, width2, 0, thickness2),
            }


        # Case 3: board1's right face connects to board2's bottom face (perpendicular assembly)
        if box1['y_min'] == box2['y_max'] and \
                (box1['x_min'] < box2['x_max'] and box1['x_max'] > box2['x_min']) and \
                (box1['z_min'] < box2['z_max'] and box1['z_max'] > box2['z_min']):
            return {
                'board1_face': 'right',  # board1's right face
                'board2_face': 'down',  # board2's bottom face
                'dimensions': (length1, thickness1),  # Connect along length and thickness
                'offset': (offset1_x, offset1_y, offset1_z)  # Starting point of connection
            }

        # # Case H: board1's front face connects to board2's bottom face (perpendicular assembly)
        # if box1['x_max'] == box2['x_min'] and \
        #         (box1['z_min'] < box2['z_max'] and box1['z_max'] > box2['z_min']) and \
        #         (box1['y_min'] < box2['y_max'] and box1['y_max'] > box2['y_min']):
        #     return {
        #         'board1_face': 'front',  # board1's right face
        #         'board1_dim': (box2['z_max'], box2['y_max']),
        #         'board2_face': 'down',  # board2's bottom face
        #         'board2_dim': (box2['z_max'], box2['y_max']),
        #         'dimensions': (length1, thickness1),  # Connect along length and thickness
        #         'offset': (offset1_x, offset1_y, offset1_z)  # Starting point of connection
        #     }
        #
        # # Case 4: board1's back face connects to board2's bottom face (perpendicular assembly)
        # if box1['x_min'] == box2['x_max'] and \
        #         (box1['z_min'] < box2['z_max'] and box1['z_max'] > box2['z_min']) and \
        #         (box1['y_min'] < box2['y_max'] and box1['y_max'] > box2['y_min']):
        #     return {
        #         'board1_face': 'back',  # board1's right face
        #         'board1_dim': (box2['z_max'], box2['y_max']),
        #         'board2_face': 'down',  # board2's bottom face
        #         'board2_dim': (box2['z_max'], box2['y_max']),
        #         'dimensions': (length1, thickness1),  # Connect along length and thickness
        #         'offset': (offset1_x, offset1_y, offset1_z)  # Starting point of connection
        #     }

        # Case 4: Check if board1 and board2 are aligned face-to-face (parallel)
        # This is a basic edge-to-edge or face-to-face connection, handled similarly as before
        # Example: board1's right face aligns with board2's left face
        if abs(offset1_x + length1 - offset2_x) < 1e-5:  # Tolerance for floating-point precision
            return {
                'board1_face': 'right',  # board1's right face
                'board2_face': 'left',  # board2's left face
                'dimensions': (width1, thickness1),  # Connect along width and thickness
                'offset': (offset1_x + length1, offset1_y, offset1_z)  # Starting point of connection
            }

        # Return None if no valid connection is found
        return None



    def get_price_for_item(self, item_type, material):
        """
        this method searches the price_list.csv file for a matching accessory name and returns the matching price.
        :return: price of the accessory
        """
        price_list_path = os.path.join(os.path.dirname(__file__), "price_list.csv")
        with open(price_list_path) as price_list_file:
            price_reader = csv.DictReader(price_list_file, delimiter=',')
            found = False
            for row in price_reader:
                if row["Item"] == item_type and row["Material"] == material:
                    found = True
                    return float(row["Price"])
            if not found:
                print("ERROR: Price for " + item_type + ":" + material + " not found. Setting to 0 RON.")
                return 0

    def get_unit_for_item(self, type, material):
    # TODO wrong implementation of unit management. To be corrected
        """
        this method searches the price_list.csv file for a matching accessory name and returns the matching price.
        :return: price of the accessory
        """
        price_list_path = os.path.join(os.path.dirname(__file__), "price_list.csv")
        with open(price_list_path) as price_list_file:
            price_reader = csv.DictReader(price_list_file, delimiter=',')
            found = False
            for row in price_reader:
                if row["Item"] == type and row["Material"] == material:
                    found = True
                    return row["Unit"]
            if not found:
                print("ERROR: Unit for " + type + ":" + material + " not found.")
                return 0

    def get_price(self):
        """
        this method searches the price_list.csv file for a matching material name and returns the price of the board
        based on it's size in m2
        :return: price of the accessory
        """
        board_size = self.get_m2()
        price = self.get_price_for_item(self.type, self.material)
        unit = self.get_unit_for_item(self.type, self.material)
        if unit == "m2":
            return int(board_size * price)
        elif unit == "m":
            return int(self.length / 1000 * price)
        elif unit == "sheet":
            return int(price / ((DEFAULT_SHEET_LENGTH * DEFAULT_SHEET_WIDTH / 1000000) * (1 - DEFAULT_LOSS)) * board_size)

    def check_board(self):
        """
        this method checks for issues with how a board is defined and prints ERRORS
        :return: None
        """
        if (self.width or self.length) < 180:
            print("WARNING: Can't apply cant on " + self.label + ". Width or length < 180mm. Additional costs might apply.")
        if (self.width or self.length) > 2000:
            print("ERROR: Potential assembly issue: " + self.label + " Can't be transported and is difficult to handle. "
                                                                     "Use boards shorter than 2 meters")


class BoardPal(Board):

    def __init__(self, label, length, width, thick, cant_L1, cant_L2, cant_l1, cant_l2):
        super().__init__(label, length, width, thick)
        self.cant_list = [cant_L1, cant_L2, cant_l1, cant_l2]
        self.drill_list = [] # diameter, surface, pos_X, pos_Y
        self.type = "pal"
        self.material = ""

        self.check_board()

    def drill(self, surface, x, y, diameter=6):
        """
        adds a list of parameters of a hole in the board's drill list
        :param surface: front, back, up, down, left, right
        :param x: the x coordinate of the hole center
        :param y: the y coordinate of the hole center
        :param diameter: diameter of the hole in mm
        :return: none
        """
        self.drill_list.append([diameter, surface, int(x), int(y)])
        print("DEBUG: Drilling " + self.label, diameter, surface, int(x), int(y))

    def get_m_cant(self, cant_type):
        """
        :param cant_type: "0.4" sau "2"
        :return: length of selected cant
        """
        length_cant04 = 0
        length_cant2 = 0
        for i in range(2):
            if self.cant_list[i] == 0.4 or self.cant_list[i] == 1 or self.cant_list[i] == "0.4" or \
                    self.cant_list[i] == "1":
                length_cant04 = length_cant04 + self.length
            if self.cant_list[i] == 2 or self.cant_list[i] == "2":
                length_cant2 = length_cant2 + self.length
            if self.cant_list[i + 2] == 0.4 or self.cant_list[i + 2] == 1 or self.cant_list[i + 2] == "0.4" or \
                    self.cant_list[i + 2] == "1":
                length_cant04 = length_cant04 + self.width
            if self.cant_list[i + 2] == 2 or self.cant_list[i + 2] == "2":
                length_cant2 = length_cant2 + self.width
        cant_length = [['0.4', length_cant04], ['2', length_cant2]]

        if cant_type == "0.4":
            return float(cant_length[0][1] / 1000)
        elif cant_type == "2":
            return float(cant_length[1][1] / 1000)
        else:
            raise Exception("ERROR: Unknown cant type!")

    def get_price(self):
        """
        gets the board price and adds the cant price
        :return:
        """
        price = super().get_price()
        m_cant_1 = self.get_m_cant("0.4")
        price_cant1 = self.get_price_for_item("cant", "0.4")
        m_cant_2 = self.get_m_cant("2")
        price_cant2 = self.get_price_for_item("cant", "2")
        return price + (m_cant_1 * price_cant1) + (m_cant_2 * price_cant2)


class Front(Board):
    def __init__(self, label, length, width, thick):
        super().__init__(label, length, width, thick)
        self.type = "front"
        self.material = ""


class Pfl(Board):
    def __init__(self, label, length, width):
        super().__init__(label, length, width, 4)
        self.type = "pfl"
        self.material = ""


class Blat(Board):
    def __init__(self, label, length, width, thick):
        super().__init__(label, length, width, thick)
        self.type = "blat"
        self.material = ""

    def get_length(self):
        return self.length/1000