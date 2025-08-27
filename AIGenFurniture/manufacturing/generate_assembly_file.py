import fitz
import math
from AIGenFurniture.furniture_design.cabinets.elements.board import Board, BoardPal

VIEW_ANGLE = 30 # angle to use when drawing isometric (the lines that go in depth will be drawn at this angle) in deg
DRAW_AREA = [500, 700] # size of the area where to draw in pdf in pixels
DRAW_AREA_START = [50, 50] # point to start the drawing in pdf in pixels


def generate_assembly_file(order, output_path):
    doc = fitz.open() # open new PDF file
    angle_z = math.sin(math.radians(VIEW_ANGLE)) # lines that go in depth need to be multiplied by this factor on z axis
    angle_x = math.cos(math.radians(VIEW_ANGLE)) # lines that go in depth need to be multiplied by this factor on x axis
    for cabinet in order.cabinets_list:
        page = doc.new_page() # create a new page for each cabinet
        shape = page.new_shape()
        shape.insert_text(fitz.Point(DRAW_AREA_START[0], DRAW_AREA_START[1]), cabinet.label) # write the label of the cabinet on the page
        scale_factor = max((cabinet.height + cabinet.depth * angle_z)/DRAW_AREA[1], (cabinet.width + cabinet.depth * angle_x)/DRAW_AREA[0]) # scale all lines to fit in the defined drawing area

        # find the overall cabinet start position on the page on X and Y axis. for each element
        # for each axis, find the smallest position of x and y and shift the position of all elements in the cabinet
        # by that offset
        # offset_min_x = math.inf # initialize the offset to infinity
        # offset_min_y = math.inf # initialize the offset to infinity
        # for element in cabinet.elements_list:
        #     if isinstance(element, Board):
        #         if element.position[3] < offset_min_x:
        #             offset_min_x = element.position[3]
        #         if element.position[4] < offset_min_y:
        #             offset_min_y = element.position[4]

        # transform the position vector to fit in the screen. If the values in the first 3 indexes of the position
        # vector are negative, make them positive, and subtract the value from the corresponding last 3 indexes
        for element in cabinet.elements_list:
            if isinstance(element, Board):
                label = element.label
                pos = [0, 0, 0, 0, 0, 0]
                for i in range(3):
                    if element.position[i] < 0:
                        pos[i] = element.position[i] * -1
                        pos[i+3] = element.position[i+3] + element.position[i]
                    else:
                        pos[i] = element.position[i]
                        pos[i + 3] = element.position[i + 3]

                width = pos[0] / scale_factor
                depth = pos[1] / scale_factor
                height = pos[2] / scale_factor

                # set the coordinates of the drawing origin of the cabinet
                ox = DRAW_AREA_START[0] + pos[3]/scale_factor + pos[4]/scale_factor * angle_x # - offset_min_x / scale_factor
                oz = DRAW_AREA_START[1] + DRAW_AREA[1] - (pos[5] / scale_factor) - (pos[4] / scale_factor * angle_z) - height # - offset_min_y / scale_factor

                origin = fitz.Point(ox, oz)
                p1 = fitz.Point(ox + depth * angle_x, oz - depth * angle_z)
                p2 = fitz.Point(ox + depth * angle_x + width, oz - depth * angle_z)
                p3 = fitz.Point(ox + width, oz)
                p4 = fitz.Point(ox + width, oz + height)
                p5 = fitz.Point(ox + depth * angle_x + width, oz + height - depth * angle_z)
                p6_2 = fitz.Point(origin.x + (p5.x - origin.x)/2, origin.y + (p5.y - origin.y)/2)
                p6 = fitz.Point(ox, oz + height)
                # print(ox, oz, ox + depth * angle_z, oz + depth * angle_x)

                face = fitz.Rect(origin, p4)
                top = fitz.Quad(p1, p2, origin, p3)
                lateral = fitz.Quad(p3, p2, p4, p5)
                shape.draw_rect(face)
                shape.draw_quad(top)
                shape.draw_quad(lateral)
                # shape.finish(color=(0, 0, 0), fill=(1, 1, 1), width=1, fill_opacity=0.5)
                shape.insert_text(p6_2, label)
                # shape.insert_text(label)
                # print(label, pos)
        # shape.draw_rect([1, 1, 594, 841]) # the size of one page
        # shape.draw_rect([50, 50, 550, 750]) # rectangle around the drawing
        shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1, fill_opacity=1)
        shape.commit()
    doc.save(output_path + '/Assembly_file.pdf')


def generate_drill_file(order, output_path):
    doc = fitz.open()
    for cabinet in order.cabinets_list:
        for element in cabinet.elements_list:
            if isinstance(element, BoardPal):
                scale_factor = max(element.width / DRAW_AREA[0], element.length / DRAW_AREA[1])
                page = doc.new_page()
                shape = page.new_shape()
                shape.insert_text(fitz.Point(DRAW_AREA_START[0], DRAW_AREA_START[1]), element.label)
                # shape.insert_text(fitz.Point(DRAW_AREA_START[0] + 60, DRAW_AREA_START[1]), str(element.length) + "X" + str(element.width))
                p1 = fitz.Point(DRAW_AREA_START[0] + 0, DRAW_AREA_START[1] + 50)
                p2 = fitz.Point(p1.x + element.width/scale_factor,
                                p1.y + element.length/scale_factor)
                board = fitz.Rect(p1, p2)
                shape.insert_text(fitz.Point(p1.x + ((p2.x - p1.x)/2), p1.y - 5), str(element.width))
                shape.insert_text(fitz.Point(p1.x - 30, p1.y + ((p2.y - p1.y) / 2)), str(element.length))
                shape.draw_rect(board)
                for i in range(len(element.drill_list)):

                    # shape.insert_text(fitz.Point(DRAW_AREA_START[0], DRAW_AREA_START[1] + 20 * (i+1)),
                    #                   "diameter " + str(element.drill_list[i][0]) +
                    #                   " side " + str(element.drill_list[i][1]) +
                    #                   " x:" + str(element.drill_list[i][2]) +
                    #                   " y:" + str(element.drill_list[i][3]))
                    if str(element.drill_list[i][1]) == "front":
                        pos = fitz.Point(p1.x + (element.drill_list[i][2] / scale_factor),
                                                     p2.y - (element.drill_list[i][3] / scale_factor))
                        shape.draw_circle(pos, 1)

                        rect = (pos.x, pos.y - 7, pos.x + 30, pos.y + 7)
                        # shape.draw_rect(rect)
                        shape.insert_textbox(rect, str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3])
                                             + " #" + str(element.drill_list[i][0]), fontsize=5)

                    if str(element.drill_list[i][1]) == "back":
                        pos = fitz.Point(p1.x + (element.drill_list[i][2] / scale_factor),
                                                     p2.y - (element.drill_list[i][3] / scale_factor))

                        rect = (pos.x, pos.y - 7, pos.x + 30, pos.y + 7)
                        # shape.draw_rect(rect)
                        shape.insert_textbox(rect, "x|" + str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3])
                                             + " #" + str(element.drill_list[i][0]), fontsize=5)
                        # shape.insert_text(fitz.Point(p1.x + (element.drill_list[i][2] / scale_factor),
                        #                              p2.y - (element.drill_list[i][3] / scale_factor)),
                        #                   str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3]))
                    elif str(element.drill_list[i][1]) == "right":
                        shape.insert_text(fitz.Point(p2.x - 10, p2.y - (element.drill_list[i][2] / scale_factor)),
                                          "> |" + str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3])
                                          + " #" + str(element.drill_list[i][0]), fontsize=5)
                    elif str(element.drill_list[i][1]) == "left":
                        shape.insert_text(fitz.Point(p1.x + 10, p2.y - (element.drill_list[i][2] / scale_factor)),
                                          "< |" + str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3])
                                          + " #" + str(element.drill_list[i][0]), fontsize=5)
                    elif str(element.drill_list[i][1]) == "up":
                        shape.insert_text(fitz.Point(p1.x + (element.drill_list[i][2] / scale_factor), p1.y + 5),
                                          "^ |" + str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3])
                                          + " #" + str(element.drill_list[i][0]), fontsize=5)
                    elif str(element.drill_list[i][1]) == "down":
                        shape.insert_text(fitz.Point(p1.x + (element.drill_list[i][2] / scale_factor), p2.y - 2),
                                          "v |" + str(element.drill_list[i][2]) + "X" + str(element.drill_list[i][3])
                                          + " #" + str(element.drill_list[i][0]), fontsize=5)

                shape.finish(color=(0, 0, 0), fill=(0.9, 0.9, 0.9), width=1, fill_opacity=1)
                shape.commit()
    doc.save(output_path + '/Drill_file.pdf')
