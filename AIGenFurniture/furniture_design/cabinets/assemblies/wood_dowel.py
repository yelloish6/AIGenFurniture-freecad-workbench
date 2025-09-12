

def assemble(board1, board2):
    """
    Assemble two boards using wood dowels.
    Hole count and placement are calculated automatically based on connection surface.
    """
    connection_surface = board1.calculate_connection_surface(board2)
    if not connection_surface:
        raise ValueError(
            f"No valid connection surface found between {board1.label} and {board2.label}."
        )

    board1_face = connection_surface['board1_face']
    board2_face = connection_surface['board2_face']
    x1_min, x1_max, y1_min, y1_max = connection_surface['board1_dim']
    x2_min, x2_max, y2_min, y2_max = connection_surface['board2_dim']
    connection_length = x1_max - x1_min
    connection_width = y1_max - y1_min

    # Decide number of dowels automatically: e.g. one dowel every ~150 mm, at least 2
    spacing = 150
    connection_count = max(2, int(connection_length // spacing))

    hole_spacing = connection_length / (connection_count + 1)

    for i in range(1, connection_count + 1):
        rel_x = hole_spacing * i
        rel_y = connection_width / 2

        # Board 1 drilling
        board1.drill(board1_face, x1_min + rel_x, y1_min + rel_y, 8)

        # Board 2 drilling
        board2.drill(board2_face, x2_min + rel_x, y2_min + rel_y, 8)