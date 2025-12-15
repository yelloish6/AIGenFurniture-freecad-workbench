import csv, os, math
from AIGenFurniture.furniture_design.pricing.price_manager import PriceManager as pm
# TODO add a method to cut-out boards, and add the effect in all output files

DEFAULT_SHEET_LENGTH = 2800
DEFAULT_SHEET_WIDTH = 2070
DEFAULT_LOSS = 0.1


class Board:
    def __init__(self, label, length, width, thick, cut_coords=None):
        """
        :param label: label of the board
        :param length: length
        :param width: width
        :param thick: thickness
        :param cut_coords: optional parameter for defining irregular shape boards
        """

        self.label = label
        self.type = ""  # pal, pfl, front
        self.material = ""
        self.length = length
        self.width = width
        self.thick = thick
        self.position = [self.length,  # dim x
                         self.width,  # dim y
                         self.thick,  # dim z
                         0,  # offset x
                         0,  # offset y
                         0]  # offset z
        self.placement = {
            "Base": {"x": 0.0, "y": 0.0, "z": 0.0},
            "Rotation": {"Axis": (0.0, 0.0, 1.0), "Angle": 0.0}
        }
        self.price = 0
        self.position_list = [] #
        self.cut_coords = cut_coords
        self.drill_list = []
        self.obs = ""
        # self.check_board() # disabled for MVP, to be reactivated once check board feature is implemented

    def add_obs(self, text):
        """
        append text to obs attribute
        :param text: string to be appended
        :return: n/a
        """
        self.obs = self.obs + text

    def set_material(self, material):
        self.material = material

    def _normalize(self, v):
        mag = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
        if mag == 0:
            return (0.0, 0.0, 0.0)
        return (v[0] / mag, v[1] / mag, v[2] / mag)

    def _rotation_matrix(self, axis, angle_rad):
        """Return 3x3 rotation matrix for axis-angle."""
        x, y, z = self._normalize(axis)
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        C = 1 - c
        return [
            [x * x * C + c, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, y * y * C + c, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, z * z * C + c]
        ]

    def _apply_rotation(self, v, M):
        """Apply 3x3 rotation matrix M to vector v."""
        return (
            M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
            M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
            M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2],
        )

    def _compose_rotations(self, axis1, angle1, axis2, angle2):
        """Compose two rotations (axis-angle) into one."""
        # Convert both to matrices
        R1 = self._rotation_matrix(axis1, angle1)
        R2 = self._rotation_matrix(axis2, angle2)
        # Matrix multiply: R = R2 * R1
        R = [[sum(a * b for a, b in zip(R2_row, R1_col)) for R1_col in zip(*R1)] for R2_row in R2]
        # Extract new axis-angle from R
        trace = R[0][0] + R[1][1] + R[2][2]
        angle = math.acos(max(-1.0, min(1.0, (trace - 1) / 2)))
        if abs(angle) < 1e-8:
            return ((0, 0, 1), 0.0)
        x = (R[2][1] - R[1][2]) / (2 * math.sin(angle))
        y = (R[0][2] - R[2][0]) / (2 * math.sin(angle))
        z = (R[1][0] - R[0][1]) / (2 * math.sin(angle))
        return (self._normalize((x, y, z)), angle)


    def rotate(self, axis, angle=90):
        """
        rotate the board by 90 deg on the specified axis. dimensions are re-set to match the rotated position
        :param axis: axis to rotate around ("x"/"y"/"z")
        :param angle: angle in degrees for rotation (default 90 deg)
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
        elif axis == "x":
            self.position[0] = init_x
        elif axis == "y":
            self.position[0] = init_z
            self.position[1] = init_y
            self.position[2] = -init_x
        # elif axis == "y":
        #     self.position[0] = -init_z
        #     self.position[1] = init_y
        #     self.position[2] = init_x
        elif axis == "z":
            self.position[0] = -init_y
            self.position[1] = init_x
            self.position[2] = init_z
        # elif axis == "z":
        #     self.position[0] = init_y
        #     self.position[1] = -init_x
        #     self.position[2] = init_z
        else:
            self.position[0] = init_x
            self.position[1] = init_y
            self.position[2] = init_z

        angle_rad = math.radians(angle)

        if isinstance(axis, str):
            axis_map = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
            axis_vec = axis_map.get(axis.lower(), (0, 0, 1))
        else:
            axis_vec = axis

        cur_axis = self.placement["Rotation"]["Axis"]
        cur_angle = self.placement["Rotation"]["Angle"]
        new_axis, new_angle = self._compose_rotations(cur_axis, cur_angle, axis_vec, angle_rad)

        self.placement["Rotation"]["Axis"] = new_axis
        self.placement["Rotation"]["Angle"] = new_angle

    def rotate_cw(self, axis):
        self.rotate(axis)
        self.rotate(axis)
        self.rotate(axis)

    def move(self, axis, offset):
        """
        Move board along an axis (string or vector) by offset (mm).
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

        if isinstance(axis, str):
            dir_map = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
            dx, dy, dz = [c * offset for c in dir_map.get(axis.lower(), (0, 0, 0))]
        else:
            n = self._normalize(axis)
            dx, dy, dz = [c * offset for c in n]

        self.placement["Base"]["x"] += dx
        self.placement["Base"]["y"] += dy
        self.placement["Base"]["z"] += dz

    def get_m2(self):
        return float(self.length * self.width / 1000000)

    def print(self):
        print(f"Board type {self.type}, {self.label}, [{self.length} x {self.width} x {self.thick}], {self.material}, "
              f"position {self.position}")
        print(f"Cut coordinates: {self.cut_coords}")

    def debug_print(self, prefix=""):
        """
        Detailed debug print of the board state.
        Useful for diagnosing connection/assembly issues.
        """
        print(f"{prefix}=== DEBUG Board {self.label} ===")
        print(f"{prefix}Type       : {self.type}")
        print(f"{prefix}Material   : {self.material}")
        print(f"{prefix}Dims (LxWxT): {self.length} x {self.width} x {self.thick}")
        print(f"{prefix}Position   : {self.position} (x,y,z,ox,oy,oz)")
        print(f"{prefix}Placement   : {self.placement} (Base, Rotation)")
        print(f"{prefix}Obs        : {self.obs}")
        print(f"{prefix}Cut Coords : {self.cut_coords if self.cut_coords else 'None'}")
        print(f"{prefix}Drill List : {self.drill_list if self.drill_list else '[]'}")
        print(f"{prefix}Transform history:")
        if self.position_list:
            for step in self.position_list:
                print(f"{prefix}  - {step}")
        else:
            print(f"{prefix}  (none)")
        print(f"{prefix}==============================")

    def get_box(board):
        length, width, thickness, ox, oy, oz = board.position
        return {
            'x_min': min(ox, ox + length),
            'x_max': max(ox, ox + length),
            'y_min': min(oy, oy + width),
            'y_max': max(oy, oy + width),
            'z_min': min(oz, oz + thickness),
            'z_max': max(oz, oz + thickness),
        }

    def calculate_connection_surface(board1, board2, tol=1e-6):
        """
        Return a dict with:
          board1_face, board1_dim (u,v), board1_offset (u0,v0),
          board2_face, board2_dim (u,v), board2_offset (u0,v0)
        All dims/offsets are in the *local* coordinates of each board.
        """
        # print(f"Checking connection between {board1.label} and {board2.label}")
        # board1.debug_print("  ")
        # board2.debug_print("  ")
        FACE_MAP = {
            ("x", +1): "right",
            ("x", -1): "left",
            ("y", +1): "up",
            ("y", -1): "down",
            ("z", +1): "front",
            ("z", -1): "back",
        }

        # helper: interval with tolerance (returns (min,max) even for zero-length touch)
        def interval(a_min, a_max, b_min, b_max):
            lo = max(a_min, b_min)
            hi = min(a_max, b_max)
            if hi + tol < lo:
                return None
            return (lo, hi)

        # get bounding boxes (uses your class get_box)
        box1 = board1.get_box()
        box2 = board2.get_box()

        ix = interval(box1["x_min"], box1["x_max"], box2["x_min"], box2["x_max"])
        iy = interval(box1["y_min"], box1["y_max"], box2["y_min"], box2["y_max"])
        iz = interval(box1["z_min"], box1["z_max"], box2["z_min"], box2["z_max"])

        # decide which axis is the contact plane (one interval must be zero-length / touching)
        contact_axis = None
        side1 = side2 = None
        if iz is not None and abs(iz[1] - iz[0]) <= tol and ix is not None and (
                ix[1] - ix[0]) > tol and iy is not None and (iy[1] - iy[0]) > tol:
            contact_axis = "z"
            side1 = +1 if abs(box1["z_max"] - box2["z_min"]) <= tol else -1
            side2 = -side1
            overlap_u = ix
            overlap_v = iy
        elif ix is not None and abs(ix[1] - ix[0]) <= tol and iy is not None and (
                iy[1] - iy[0]) > tol and iz is not None and (iz[1] - iz[0]) > tol:
            contact_axis = "x"
            side1 = +1 if abs(box1["x_max"] - box2["x_min"]) <= tol else -1
            side2 = -side1
            overlap_u = iy
            overlap_v = iz
        elif iy is not None and abs(iy[1] - iy[0]) <= tol and ix is not None and (
                ix[1] - ix[0]) > tol and iz is not None and (iz[1] - iz[0]) > tol:
            contact_axis = "y"
            side1 = +1 if abs(box1["y_max"] - box2["y_min"]) <= tol else -1
            side2 = -side1
            overlap_u = ix
            overlap_v = iz
        else:
            # not a clean face-to-face contact (either volume overlap or no contact)
            return None

        # build local->global mapping from board.position[:3]
        # mapping: local_axis ('x','y','z') -> (global_axis 'x'/'y'/'z', sign)
        def build_local_map(board):
            px, py, pz = board.position[:3]
            mapping = {"x": None, "y": None, "z": None}
            # global x (px) holds one of the local dims
            if abs(px) == board.length:
                mapping["x"] = ("x", 1 if px > 0 else -1)
            elif abs(px) == board.width:
                mapping["y"] = ("x", 1 if px > 0 else -1)
            elif abs(px) == board.thick:
                mapping["z"] = ("x", 1 if px > 0 else -1)
            # global y (py)
            if abs(py) == board.length:
                mapping["x"] = ("y", 1 if py > 0 else -1)
            elif abs(py) == board.width:
                mapping["y"] = ("y", 1 if py > 0 else -1)
            elif abs(py) == board.thick:
                mapping["z"] = ("y", 1 if py > 0 else -1)
            # global z (pz)
            if abs(pz) == board.length:
                mapping["x"] = ("z", 1 if pz > 0 else -1)
            elif abs(pz) == board.width:
                mapping["y"] = ("z", 1 if pz > 0 else -1)
            elif abs(pz) == board.thick:
                mapping["z"] = ("z", 1 if pz > 0 else -1)

            # DEBUG print
            if None in mapping.values():
                print(
                    f"[DEBUG] build_local_map incomplete for {board.label}: pos={board.position}, len={board.length}, width={board.width}, thick={board.thick}, mapping={mapping}")

            return mapping

        # For each contact_local axis, which local axes span the face and in which order (u,v)
        plane_axes_for_local = {
            "x": ("z", "y"),  # left/right face -> (local z, local y) -> (thickness, width)
            "y": ("x", "z"),  # up/down face    -> (local x, local z) -> (length, thickness)
            "z": ("x", "y"),  # front/back face -> (local x, local y) -> (length, width)
        }

        # Convert a board overlap to (face, (u_size,v_size), (u0,v0)) in local coords
        def compute_board_result(board, contact_axis, side, overlap_u, overlap_v):
            mapping = build_local_map(board)
            origin = {"x": board.position[3], "y": board.position[4], "z": board.position[5]}

            # find which local axis corresponds to the contact_axis
            contact_local = None
            for local_axis, mapping_val in mapping.items():
                if mapping_val is None:
                    continue
                g_axis, sign = mapping_val
                if g_axis == contact_axis:
                    contact_local = local_axis
                    sign_local = sign
                    break
            if contact_local is None:
                return None

            effective_sign = sign_local * side
            face = FACE_MAP[(contact_local, 1 if effective_sign > 0 else -1)]

            # plane axes in local coords (order u,v)
            u_local_axis, v_local_axis = plane_axes_for_local[contact_local]

            # helper: determine global axis & sign for a local axis
            def local_to_global(local_ax):
                g_axis, sign = mapping[local_ax]
                return g_axis, sign

            # get the relevant global intervals (overlap_u and overlap_v were chosen in earlier detection,
            # but we must map them to the correct global axes depending on contact_axis)
            # overlap_u and overlap_v are provided in global axis order determined above:
            # - for contact z: overlap_u=ix (global x interval), overlap_v=iy (global y interval)
            # - for contact x: overlap_u=iy (global y interval), overlap_v=iz (global z interval)
            # - for contact y: overlap_u=ix (global x interval), overlap_v=iz (global z interval)
            # We'll create a dict for fast lookup:
            global_intervals = {
                "x": ix,
                "y": iy,
                "z": iz
            }

            # function to get local interval (min,max) for a local axis
            def get_local_interval(local_ax):
                g_axis, sign = local_to_global(local_ax)
                interval = global_intervals[g_axis]
                if interval is None:
                    return (0.0, 0.0)  # no overlap on that axis
                g_min, g_max = interval
                # convert to local coords: local = sign * (global - origin_global)
                origin_val = origin[g_axis]
                l_min = sign * (g_min - origin_val)
                l_max = sign * (g_max - origin_val)
                # ensure ordering ascending
                return (min(l_min, l_max), max(l_min, l_max))

            u_min, u_max = get_local_interval(u_local_axis)
            v_min, v_max = get_local_interval(v_local_axis)

            u0 = u_min
            v0 = v_min
            u_size = u_max - u_min
            v_size = v_max - v_min

            return {
                "face": face,
                "dim": (u_size, v_size),
                "offset": (u0, v0)
            }

        res1 = compute_board_result(board1, contact_axis, side1, overlap_u, overlap_v)
        res2 = compute_board_result(board2, contact_axis, side2, overlap_u, overlap_v)

        if res1 is None or res2 is None:
            return None

        return {
            "board1_face": res1["face"],
            "board1_dim": (round(res1["dim"][0], 6), round(res1["dim"][1], 6)),
            "board1_offset": (round(res1["offset"][0], 6), round(res1["offset"][1], 6)),
            "board2_face": res2["face"],
            "board2_dim": (round(res2["dim"][0], 6), round(res2["dim"][1], 6)),
            "board2_offset": (round(res2["offset"][0], 6), round(res2["offset"][1], 6)),
        }

    def drill(self, face, x, y, diameter=6):
        """
        adds a list of parameters of a hole in the board's drill list
        :param face: front, back, up, down, left, right
        :param x: the x coordinate of the hole center
        :param y: the y coordinate of the hole center
        :param diameter: diameter of the hole in mm
        :return: none
        """
        self.drill_list.append([diameter, face, int(x), int(y)])


    # def get_price_for_item(self, item_type, material):
    #     """
    #     this method searches the price_list.csv file for a matching accessory name and returns the matching price.
    #     :return: price of the accessory
    #     """
    #     # print(f"DEBUG board.py(get_price_for_item): {self.label}, {item_type}, {material}")
    #     price_list_path = os.path.join(os.path.dirname(__file__), "price_list.csv")
    #     with open(price_list_path) as price_list_file:
    #         price_reader = csv.DictReader(price_list_file, delimiter=',')
    #         found = False
    #         for row in price_reader:
    #             if row["Item"] == str(item_type) and row["Material"] == str(material):
    #                 found = True
    #                 return float(row["Price"])
    #         if not found:
    #             print("ERROR: Price for " + item_type + ": " + material + " not found. Setting to 0 RON.")
    #             return 0

    # def get_unit_for_item(self, type, material):
    #       # TODO wrong implementation of unit management. To be corrected
    #     """
    #     this method searches the price_list.csv file for a matching accessory name and returns the matching price.
    #     :return: price of the accessory
    #     """
    #     price_list_path = os.path.join(os.path.dirname(__file__), "price_list.csv")
    #     with open(price_list_path) as price_list_file:
    #         price_reader = csv.DictReader(price_list_file, delimiter=',')
    #         found = False
    #         for row in price_reader:
    #             if row["Item"] == type and row["Material"] == material:
    #                 found = True
    #                 return row["Unit"]
    #         if not found:
    #             print("ERROR: Unit for " + type + ":" + material + " not found.")
    #             return 0

    def get_price(self):
        """
        this method searches the price_list.csv file for a matching material name and returns the price of the board
        based on it's size in m2
        :return: price of the accessory
        """
        board_size = self.get_m2()
        price = pm.get_price_for_item(self.type, self.material)
        unit = pm.get_unit_for_item(self.type, self.material)
        if unit == "m2":
            return int(board_size * price)
        elif unit == "m":
            return int(self.length / 1000 * price)
        elif unit == "sheet":
            return int(price / ((DEFAULT_SHEET_LENGTH * DEFAULT_SHEET_WIDTH / 1000000) * (1 - DEFAULT_LOSS)) * board_size)
        elif unit == "piece":
            return price
        else:
            print(f"WARNING [board.py]: Unknown unit '{unit}' for {self.type}/{self.material}. Returning 0.")
            return 0

    def get_unit(self):
        return pm.get_unit_for_item(self.type, self.material)

    def check_board(self):
        """
        this method checks for issues with how a board is defined and prints ERRORS
        :return: None
        """
        if (self.width or self.length) > 2000:
            print(f"WARNING [board.py/check_board()]: Potential assembly issue: {self.label} Can't be transported and is difficult to handle. "
                                                                     "Use boards shorter than 2 meters")


class BoardPal(Board):

    def __init__(self, label, length, width, thick, cant_L1, cant_L2, cant_l1, cant_l2):
        super().__init__(label, length, width, thick)
        self.cant_list = [cant_L1, cant_L2, cant_l1, cant_l2]
        self.drill_list = [] # diameter, surface, pos_X, pos_Y
        self.type = "pal"
        self.material = ""

        # self.check_board_pal() # disabled in MVP, to be added once feature is implemented

    def check_board_pal(self):
        # additionally check if edge is applied on a board that has dimensions smaller than 180 mm
        if self.length <= 180 and (self.cant_list[0] or self.cant_list[1]) != "":
            print(f"WARNING [board.py/check_board_pal()]: Can't apply edge on {self.label} length. Length < 180mm. Additional costs might apply.")
        elif self.width <= 180 and (self.cant_list[2] or self.cant_list[3]) != "":
            print(f"WARNING: Can't apply cant on {self.label} width. Width < 180mm. Additional costs might apply.")

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
        price_cant1 = pm.get_price_for_item("cant", "0.4")
        m_cant_2 = self.get_m_cant("2")
        price_cant2 = pm.get_price_for_item("cant", "2")
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


if __name__ == "__main__":
    print("=== Running Board test scenario ===")

    # Create two boards
    b1 = Board("Bottom", 600, 500, 18)   # 600 x 500 board, 18 mm thick
    b2 = Board("Side", 800, 500, 18)     # Side panel: 720 tall, 500 deep, 18 thick

    # Move side board to sit on top of bottom board, aligned at (0,0,0)
    b2.rotate_cw("y")
    # b2.move("z", 18)
    # b2.move("x", 18)
    # b2.move("x", 200)

    print("\nBoard positions:")
    b1.debug_print()
    b2.debug_print()

    # Check connection surface
    conn = Board.calculate_connection_surface(b1, b2)
    print("\nCalculated connection surface:")
    print(conn)

    # Test some methods
    print("\nExtra tests:")
    b1.set_material("PAL white")
    b1.add_obs("Cutout for sink.")
    print("Obs for b1:", b1.obs)

    # Rotate and move board
    b2.rotate("z")
    print("After rotating b2 around Z:")
    b2.print()

    # Check m2 calculation
    print(f"Surface area b1: {b1.get_m2():.3f} m²")

    print("=== Test scenario complete ===")