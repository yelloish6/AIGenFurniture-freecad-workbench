import math
from AIGenFurniture.furniture_design.cabinets.elements.board import Board

def assemble(board1, board2):
    """
    Assemble two boards using one or 2 Hettich Rastex connections and 2 wood dowel connections.
    The hole spacing is calculated considering the Kraft&Dele drilling jig for edge drilling.
        Kraft&Dele sizes:
            109.5 mm distance between centering pin and first drill hole
            32.5 mm distance between drill holes
        For boards 100 mm - center alignment
            1. Center the middle hole of the jig at the middle of the board
            2. Add fixation pin in the middle hole and drill in left and right drill holes
        For boards 200 mm - center alignment
            1. Center the middle hole of the jig at the middle of the board
            2. Add fixation pin in one of the outer drill holes and use the other one to drill
            3. Repeat on the other side
        For boards 300 mm - edge alignment
            1. Add the fixation pin in the diam 8 hole of the KnD and align to the edge of the board.
            2. Drill in the closest fixation hole (109,5 - 4 = 105.5)
            3. Put the fixation pin in the drilled hole and drill in the next one (105,5 + 109,5 = 215)
    	    300 edge		300 center		400 edge		    500 edge		600 edge
	        Hole X	dist	Hole X	dist 	Hole X	dist	    Hole X	dist	Hole X	dist
1st hole	105.5	105.5	85	    85	    105.5	105.5	    105.5	105.5	105.5	105.5
2nd hole	170.5	65	    150	    65	    170.5	65	        215	    109.5	215	    109.5
3rd hole	235.5	65	    215	    65	    235.5	65	        324.5 	109.5	324.5	109.5
4th hole	300	    64.5	300	    85	    300.5	65	        434	    109.5	434	    109.5
5th hole					                400	    99.5	    500	    66	    543.5	109.5
									                                            600	    56.5
    """
    RASTEX_EDGE_DIAMETER = 5
    DOWEL_DIAMETER = 8

    connection_surface = board1.calculate_connection_surface(board2)
    if not connection_surface:
        raise ValueError(
            f"No valid connection surface found between {board1.label} and {board2.label}."
        )

    b1_face = connection_surface['board1_face']
    b2_face = connection_surface['board2_face']
    b1_u, b1_v = connection_surface['board1_dim']
    b2_u, b2_v = connection_surface['board2_dim']
    b1_u_offset, b1_v_offset = connection_surface['board1_offset']
    b2_u_offset, b2_v_offset = connection_surface['board2_offset']

    length = max(b1_u, b1_v)  # pick U-axis as drilling direction

    # Predefined jig hole tables (values from docstring)
    hole_tables = {
            100: [17, 50, 82],
            200: [35, 100, 165],
            300: [105, 170, 235],
            400: [105, 215, 324],
            500: [105, 215, 324, 434],
            600: [105, 215, 324, 434, 543],
    }

    # Pick the next defined jig size
    chosen_size = min([s for s in hole_tables.keys() if s >= length], default=600)
    hole_positions = hole_tables[chosen_size]

    # Assign dowel/rastex sequence
    hole_count = len(hole_positions)
    hole_types = []

    for i in range(hole_count):
        if i == 0 or i == hole_count - 1:
            hole_types.append("dowel")
        elif hole_count % 2 == 1 and i == hole_count // 2:
            hole_types.append("dowel")
        else:
            hole_types.append("rastex")

    # Drill according to sequence
    for pos, htype in zip(hole_positions, hole_types):
        diameter = DOWEL_DIAMETER if htype == "dowel" else RASTEX_EDGE_DIAMETER

        # Drill in both boards
        board1.drill(b1_face, b1_u_offset + pos, b1_v_offset, diameter)
        board2.drill(b2_face, b2_u_offset + pos, b2_v_offset, diameter)

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
    b1.debug_print("  ")
    b2.debug_print("  ")
