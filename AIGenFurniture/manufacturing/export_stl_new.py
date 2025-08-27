import math

import numpy
import tripy
import os
from copy import deepcopy
from AIGenFurniture.furniture_design.cabinets.elements.board import Board
from stl import mesh


def export_stl_order(order, output_folder, is_horizontal_layout = True):
    """
    generate STL file based on order object containing all cabinets
    :param order: input object
    :param output_folder: output folder where to store STL file
    :param is_horizontal_layout: position each cabinet with an offset next to the previous one (to be used when final positioning of cabinets is not known)
    :return: None
    """
    file_name = os.path.join(output_folder, "3D " + order.client + "_mesh")

    offset = 0
    order_mesh = None
    for cabinet in order.cabinets_list:
        cabinet_mesh = None
        for element in cabinet.elements_list:
            if isinstance(element, Board):
                board_mesh = generate_mesh_for_board(element)
                position_mesh(board_mesh, element.position_list)
                if not cabinet_mesh:
                    cabinet_mesh = board_mesh
                else:
                    cabinet_mesh = mesh.Mesh(numpy.concatenate([cabinet_mesh.data, board_mesh.data]))
        position_mesh(cabinet_mesh, cabinet.position_list)
        if cabinet_mesh is not None:
            move_mesh(cabinet_mesh, "x", offset)

        # Position each cabinet next to the other or on the same position based on "is_horizontal_layout"
        if is_horizontal_layout:
            offset += cabinet.width + 1
        if not order_mesh:
            order_mesh = cabinet_mesh
        else:
            if cabinet_mesh is not None:
                order_mesh = mesh.Mesh(numpy.concatenate([order_mesh.data, cabinet_mesh.data]))
    order_mesh.save(str(file_name) + ".stl")

    file_name = os.path.join(output_folder, "3D " + order.client)

    offset = 0
    order_mesh = None
    for cabinet in order.cabinets_list:
        cabinet_to_print = deepcopy(cabinet)  # copy the cabinet to print, to not change the original cabinet
        cabinet_to_print.move_corp("x", offset)  # add an offset to separate the cabinets when printing

        for movement in cabinet_to_print.position_list:  # run through the position list and operate all movements on the cabinet to be printed
            if movement[0] == "move":
                cabinet_move(cabinet_to_print, movement[1], movement[2])
            elif movement[0] == "rotate":
                cabinet_rotate(cabinet_to_print, movement[1])

        for element in cabinet_to_print.elements_list:  # generate the stl part for all elements in the cabinet to be printed
            if isinstance(element, Board):
                board_mesh = generate_mesh(element.position[0],
                                           element.position[1],
                                           element.position[2],
                                           element.position[3],
                                           element.position[4],
                                           element.position[5]
                                           )
                if not order_mesh:
                    order_mesh = board_mesh
                else:
                    order_mesh = mesh.Mesh(numpy.concatenate([order_mesh.data, board_mesh.data]))
        offset += cabinet_to_print.width + 1
    order_mesh.save(str(file_name) + ".stl")


def generate_mesh(x, y, z, ox, oy, oz, cut_coords=None):
    """
    generates a mesh object containing one board with given dimensions (x,y,z) and offset (ox, oy, oz)
    can be used in a loop.
    The new version includes also cut_coords as optional parameters, for cut-out boards.

    :param x: size on x-axis
    :param y: size on y-axis
    :param z: size on z-axis
    :param ox: orientation on x-axis
    :param oy: orientation on y-axis
    :param oz: orientation on x-axis
    :param cut_coords: list of coordinate pairs for all points on the top side of the board, all points must be within x, y, z
    :return: mesh object
    """

    # if cut_coords is None:
    #     cut_coords = []
    if not cut_coords:
        cut_coords = [
            [ox, oy],
            [ox + x, oy],
            [ox + x, oy + y],
            [ox, oy + y]
        ]
    height = oz + z

    top_vertices = numpy.zeros([len(cut_coords), 3], dtype=int)
    bottom_vertices = numpy.zeros([len(cut_coords), 3], dtype=int)

    for i, coord in enumerate(cut_coords):
        top_vertices[i] = numpy.array([coord[0], coord[1], height])
        bottom_vertices[i] = numpy.array([coord[0], coord[1], height - z])

    vertices = numpy.concatenate([top_vertices, bottom_vertices])

    # get top triangles using tripy
    top_triangles = tripy.earclip(cut_coords)

    # convert triangles from coordinates to indexes in the coords vector
    top_triangles_index = numpy.zeros([len(top_triangles), 3], dtype=int)
    for i in range(len(top_triangles)):
        for j in range(3):
            lookup_value = list(top_triangles[i][j])
            top_triangles_index[i][j] = cut_coords.index(lookup_value)

    # concatenate bottom triangles indexes by adding the length of the top coords vector to the top coords indexes
    bottom_triangles_index = numpy.zeros([len(top_triangles), 3], dtype=int)
    for i in range(len(top_triangles_index)):
        for j in range(3):
            bottom_triangles_index[i][j] = top_triangles_index[i][j] + len(cut_coords)

    # define faces vector
    faces = numpy.concatenate([top_triangles_index, bottom_triangles_index])

    # concatenate lateral faces
    # lateral_faces = numpy.zeros([len(cut_coords) * 2, 3])
    offset = len(cut_coords)
    for i in range(len(cut_coords) - 1):
        triangles = [[i, i+1, i+offset], [i + offset, i + 1, i + offset + 1]]
        faces = numpy.concatenate([faces, triangles])

    # concatenate the final face that closes the complete board
    final_face = [[len(cut_coords) - 1, 0, len(cut_coords) + offset - 1],
                  [len(cut_coords) + offset - 1, 0, len(cut_coords)]] # [[7, 0, 16], [16, 0 ,8]]

    faces = numpy.concatenate([faces, final_face])

    # print(faces)
    #
    # print(vertices)

    meshes = mesh.Mesh(numpy.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            meshes.vectors[i][j] = vertices[f[j], :]
            # print(meshes.vectors)

    # meshes.save('my_board.stl')
    return meshes


def generate_mesh_for_board(board):

    # use the length width and thick of the board to generate the mesh (to ignore the movements recorded in the postion list)
    x = board.length
    y = board.width
    z = board.thick
    ox = 0
    oy = 0
    oz = 0

    # use the position list to generate the mesh
    # x = board.position[0]
    # y = board.position[1]
    # z = board.position[2]
    # ox = board.position[3]
    # oy = board.position[4]
    # oz = board.position[5]

    cut_coords = board.cut_coords
    return generate_mesh(x, y, z, ox, oy, oz, cut_coords)

# test the code
# my_stl_board = export_stl_new("3D_board_to_test", "test_board", 600, 500, 18, 100, 200, 50,
#                cut_coords=[[0, 0], [600, 0], [600, 500], [400, 500], [400, 300], [200, 300], [200, 500], [0, 500]])
#
# plot_board(my_stl_board)


def position_mesh(input_mesh, position_list):
    """
    method to apply the movements in a position list on a mesh and returns the modified mesh
    :param input_mesh: the initial mesh object
    :param position_list: the list of movements
    :return: the modified mesh object
    """
    for movement in position_list:
        if movement[0] == "move":
            move_mesh(input_mesh, movement[1], movement[2])
        elif movement[0] == "rotate":
            rotate_mesh(input_mesh, movement[1])
    return input_mesh


def rotate_mesh(my_mesh, axis):
    if axis == "x":
        my_mesh.rotate([0.5, 0.0, 0.0], math.radians(-90))
    elif axis == "y":
        my_mesh.rotate([0.0, 0.5, 0.0], math.radians(90))
    elif axis == "z":
        my_mesh.rotate([0.0, 0.0, 0.5], math.radians(90))
    else:
        print(f"ERROR: Unknown axis {axis}. Value must be x, y or z.")


def move_mesh(my_mesh, axis, offset):
    if axis == "x":
        my_mesh.x += offset
    elif axis == "y":
        my_mesh.y += offset
    elif axis == "z":
        my_mesh.z += offset
    else:
        print(f"ERROR: Unknown axis {axis}. Value must be x, y or z.")


def cabinet_rotate(cabinet, axis):
    for i in range(len(cabinet.elements_list)):
        if isinstance(cabinet.elements_list[i], Board):
            cabinet.elements_list[i].rotate(axis)
            initial_position = cabinet.elements_list[i].position
            final_position = initial_position
            offset_x = initial_position[3]
            offset_y = initial_position[4]
            offset_z = initial_position[5]
            if axis == "x":
                final_position[3] = offset_x
                final_position[4] = -offset_z
                final_position[5] = offset_y
            elif axis == "y":
                final_position[3] = -offset_z
                final_position[4] = offset_y
                final_position[5] = offset_x
            elif axis == "z":
                final_position[3] = offset_y
                final_position[4] = -offset_x
                final_position[5] = offset_z
            cabinet.elements_list[i].position = final_position


def cabinet_move(cabinet, axis, offset):
    for i in range(len(cabinet.elements_list)):
        if isinstance(cabinet.elements_list[i], Board):
            cabinet.elements_list[i].move(axis, offset)
