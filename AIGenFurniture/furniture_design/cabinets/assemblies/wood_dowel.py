import math
from AIGenFurniture.furniture_design.cabinets.elements.board import Board

def assemble(board1, board2):
    """
    Assemble two boards using wood dowels.
    Hole count and placement are calculated automatically based on connection surface.
    """
    DOWEL_DIAMETER = 8
    connection_surface = board1.calculate_connection_surface(board2)
    if not connection_surface:
        raise ValueError(
            f"No valid connection surface found between {board1.label} and {board2.label}."
        )

    b1_face = connection_surface['board1_face']
    b2_face = connection_surface['board2_face']
    b1_u, b1_v = connection_surface['board1_dim']
    b1_u, b1_v = connection_surface['board2_dim']
    b1_u_offset, b1_v_offset = connection_surface['board1_offset']
    b2_u_offset, b2_v_offset = connection_surface['board2_offset']
    # x1_min, x1_max, y1_min, y1_max = connection_surface['board1_dim']
    # x2_min, x2_max, y2_min, y2_max = connection_surface['board2_dim']
    # connection_length = x1_max - x1_min
    # connection_width = y1_max - y1_min

    # Decide number of dowels automatically: e.g. one dowel every ~150 mm, at least 2
    spacing = 250
    # connection_count = max(2, int(connection_length // spacing))
    connection_count_u = math.ceil(b1_u / spacing)
    connection_count_v = math.ceil(b1_v / spacing)
    if connection_count_v == connection_count_u == 1:
        if b1_u > b1_v: connection_count_u = 2
        else: connection_count_v = 2
    hole_spacing_u = int(b1_u / (connection_count_u + 1))
    hole_spacing_v = int(b1_v / (connection_count_v + 1))

    for i in range(1, connection_count_u + 1):
        for j in range(1, connection_count_v + 1):
            rel_u = hole_spacing_u * i
            rel_v = hole_spacing_v * j

            # Board 1 drilling
            board1.drill(b1_face, b1_u_offset + rel_u, b1_v_offset + rel_v, DOWEL_DIAMETER)

            # Board 2 drilling
            board2.drill(b2_face, b2_u_offset + rel_u, b2_v_offset + rel_v, DOWEL_DIAMETER)

if __name__ == "__main__":
    print("=== Running assembly test scenario ===")

    # Create two boards
    b1 = Board("Bottom", 600, 500, 18)   # 600 x 500 board, 18 mm thick
    b2 = Board("Side", 800, 500, 18)     # Side panel: 720 tall, 500 deep, 18 thick

    # Move side board to sit on top of bottom board, aligned at (0,0,0)
    b2.rotate("y")
    # b2.move("z", 18)
    # b2.move("x", 18)
    # b2.move("x", 200)

    assemble(b1, b2)
    print(b1.__getattribute__("label"), b1.__getattribute__("drill_list"))
    print(b2.__getattribute__("label"), b2.__getattribute__("drill_list"))
