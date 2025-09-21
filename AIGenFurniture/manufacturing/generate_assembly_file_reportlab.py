import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

MARGIN_MM = 20
HEADER_HEIGHT_MM = 20


def normalize_face_code(face):
    if not face:
        return None
    s = str(face).lower()
    if s in ("+x", "right", "r"): return "+x"
    if s in ("-x", "left", "l"): return "-x"
    if s in ("+y", "up", "u", "top"): return "+y"
    if s in ("-y", "down", "d", "bottom"): return "-y"
    if s in ("+z", "front", "f"): return "+z"
    if s in ("-z", "back", "b"): return "-z"
    return face


def parse_drill_entry(entry):
    if isinstance(entry, dict):
        return {
            "diameter": float(entry.get("diameter", 0)),
            "face": normalize_face_code(entry.get("face")),
            "a": float(entry.get("a", entry.get("x", 0))),
            "b": float(entry.get("b", entry.get("y", 0))),
            "depth": entry.get("depth"),
            "note": entry.get("note", "")
        }
    elif isinstance(entry, (list, tuple)):
        return {
            "diameter": float(entry[0]) if len(entry) > 0 else 0,
            "face": normalize_face_code(entry[1]) if len(entry) > 1 else None,
            "a": float(entry[2]) if len(entry) > 2 else 0,
            "b": float(entry[3]) if len(entry) > 3 else 0,
            "depth": entry[4] if len(entry) > 4 else None,
            "note": entry[5] if len(entry) > 5 else ""
        }
    else:
        raise ValueError("Unsupported drill entry type")


def draw_board(c, board, page_w, page_h, margin, header_h):
    """
    Draw board front (LxW) and extrude thickness bottom-left.
    Returns: front_rect, extruded_rect, scale, ox, oy
    rects are lists of 4 (x,y) points ordered: p0 (BL), p1 (BR), p2 (TR), p3 (TL)
    """
    L, W, T = float(board.length), float(board.width), float(board.thick)

    draw_w = page_w - 2 * margin
    draw_h = page_h - 2 * margin - header_h

    # origin
    # reserve extra space for header/title at top and table at bottom
    reserved_top = header_h + 40 * mm
    reserved_bottom = 40 * mm + 90
    draw_h = page_h - reserved_top - reserved_bottom
    scale = min(draw_w / ((L + T) * mm), draw_h / ((W + T) * mm), 1.0)

    ox = margin + 40
    oy = reserved_bottom

    # better iso extrusion (balanced)
    dx = -T * mm * scale * 0.7071
    dy = -T * mm * scale * 0.7071

    front = [
        (ox, oy),
        (ox + L * mm * scale, oy),
        (ox + L * mm * scale, oy + W * mm * scale),
        (ox, oy + W * mm * scale),
    ]
    extruded = [(x + dx, y + dy) for (x, y) in front]

    def draw_face(points, fill_color):
        path = c.beginPath()
        x0, y0 = points[0]
        path.moveTo(x0, y0)
        for (x, y) in points[1:]:
            path.lineTo(x, y)
        path.close()
        c.setFillColor(fill_color)
        c.setStrokeColor(colors.black)
        c.drawPath(path, stroke=1, fill=1)

    # visible faces
    draw_face(front, colors.white)
    draw_face([front[0], extruded[0], extruded[3], front[3]], colors.whitesmoke)  # left
    draw_face([front[0], front[1], extruded[1], extruded[0]], colors.whitesmoke)  # bottom

    # hidden edges (dashed)
    c.setDash(3, 3)
    c.line(front[1][0], front[1][1], extruded[1][0], extruded[1][1])
    c.line(front[2][0], front[2][1], extruded[2][0], extruded[2][1])
    c.line(front[3][0], front[3][1], extruded[3][0], extruded[3][1])
    c.line(extruded[1][0], extruded[1][1], extruded[2][0], extruded[2][1])
    c.line(extruded[2][0], extruded[2][1], extruded[3][0], extruded[3][1])
    c.setDash()

    return front, extruded, scale, ox, oy


def face_rects(front, extruded):
    """
    Return rects for faces with consistent p0..p3 ordering
    p0 == local (0,0). p1 == (max_x,0), p2 == (max_x,max_y), p3 == (0,max_y)
    """
    rects = {}
    rects["+z"] = front[:]  # L x W
    rects["-z"] = front[:]  # back uses same rect (drawn dashed if needed)
    # left: local_x = thickness (0..T) maps p0->extruded[0], local_y = Y (0..W) maps p0->p3
    rects["-x"] = [front[0], extruded[0], extruded[3], front[3]]
    # right: local_x = thickness, local_y = Y; origin is front[1]
    rects["+x"] = [front[1], extruded[1], extruded[2], front[2]]
    # bottom: local_x = X (0..L), local_y = thickness (0..T)
    rects["-y"] = [front[0], front[1], extruded[1], extruded[0]]
    # top: origin at front[3], local_x = X, local_y = thickness
    rects["+y"] = [front[3], front[2], extruded[2], extruded[3]]
    return rects


def project_local_to_page_affine(rect, local_x_mm, local_y_mm, face_w_mm, face_h_mm):
    """
    Bilinear/affine map from face local mm coords -> page points.
    rect must be ordered p0,p1,p2,p3 as per face_rects docstring.
    """
    (x0, y0), (x1, y1), (_, _), (x3, y3) = rect
    # avoid division by zero, caller should guard; but handle gracefully:
    if face_w_mm == 0 or face_h_mm == 0:
        return x0, y0
    u = local_x_mm / face_w_mm
    v = local_y_mm / face_h_mm
    px = (1 - u) * (1 - v) * x0 + u * (1 - v) * x1 + u * v * x1 + (1 - u) * v * x3
    # note: the above uses a simplified bilinear consistent with p0/p1/p2/p3 co-linearity
    py = (1 - u) * (1 - v) * y0 + u * (1 - v) * y1 + u * v * y1 + (1 - u) * v * y3
    # The simplification (p2 not used separately) is valid because p2 = p1 + (p3-p0)
    return px, py


def draw_hole_affine(c, rect, face, a_mm, b_mm, r_mm, L, W, T, visible=True):
    """
    Draw hole with affine transform aligning mm-space circle into face rectangle.
    Returns (px, py, clamped_flag) page coords of drawn center and whether clamping happened.
    """
    # map local variables depending on face
    if face in ("+z", "-z"):
        local_x_mm = a_mm
        local_y_mm = b_mm
        face_w_mm = L
        face_h_mm = W
    elif face in ("-x", "+x"):
        # for x faces: drill entry a = Y, b = Z  (user convention)
        local_x_mm = a_mm  # Y → vertical axis in drawing
        local_y_mm = b_mm  # Z → horizontal (thickness)
        face_w_mm = T
        face_h_mm = W
    elif face in ("-y", "+y"):
        # for y faces: a = X, b = Z
        local_x_mm = a_mm
        local_y_mm = b_mm
        face_w_mm = L
        face_h_mm = T
    else:
        return None, None, False

    # clamp coords into face
    clamped = False
    orig_local_x = local_x_mm
    orig_local_y = local_y_mm
    if local_x_mm < 0:
        local_x_mm = 0; clamped = True
    if local_x_mm > face_w_mm:
        local_x_mm = face_w_mm; clamped = True
    if local_y_mm < 0:
        local_y_mm = 0; clamped = True
    if local_y_mm > face_h_mm:
        local_y_mm = face_h_mm; clamped = True

    # make sure radius fits inside the face (reduce if needed)
    max_r = min(face_w_mm, face_h_mm) * 0.5
    if r_mm > max_r:
        r_mm = max_r
        clamped = True

    # compute page center for label (before applying transform)
    px, py = project_local_to_page_affine(rect, local_x_mm, local_y_mm, face_w_mm, face_h_mm)

    # compute affine transform parameters (points-per-mm along local axes)
    p0 = rect[0]; p1 = rect[1]; p3 = rect[3]
    # guard
    if face_w_mm == 0 or face_h_mm == 0:
        return px, py, clamped

    m_a = (p1[0] - p0[0]) / face_w_mm
    m_b = (p1[1] - p0[1]) / face_w_mm
    m_c = (p3[0] - p0[0]) / face_h_mm
    m_d = (p3[1] - p0[1]) / face_h_mm
    m_e = p0[0]
    m_f = p0[1]

    # dashed if hidden
    if visible:
        c.setDash()
    else:
        c.setDash(2, 2)
    c.setStrokeColor(colors.red)

    # draw by transforming mm-space -> page-space
    c.saveState()
    c.transform(m_a, m_b, m_c, m_d, m_e, m_f)
    c.setLineWidth(0.8)
    # draw circle in local mm coords (becomes ellipse in page)
    left = local_x_mm - r_mm
    bottom = local_y_mm - r_mm
    right = local_x_mm + r_mm
    top = local_y_mm + r_mm
    c.ellipse(left, bottom, right, top, stroke=1, fill=0)
    c.restoreState()

    c.setDash()  # reset dash style
    return px, py, clamped


def draw_dimensions(c, front, L_mm, W_mm):
    p0, p1, p2, p3 = front
    y_dim = p0[1] - 8 * mm
    c.setStrokeColor(colors.black)
    c.line(p0[0], y_dim, p1[0], y_dim)
    arrow = 3 * mm
    c.line(p0[0], y_dim, p0[0] + arrow, y_dim + arrow / 2)
    c.line(p0[0], y_dim, p0[0] + arrow, y_dim - arrow / 2)
    c.line(p1[0], y_dim, p1[0] - arrow, y_dim + arrow / 2)
    c.line(p1[0], y_dim, p1[0] - arrow, y_dim - arrow / 2)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawCentredString((p0[0] + p1[0]) / 2, y_dim - 6, f"{L_mm:.0f} mm")

    x_dim = p0[0] - 12 * mm
    c.line(x_dim, p0[1], x_dim, p3[1])
    c.line(x_dim, p3[1], x_dim + arrow / 2, p3[1] - arrow)
    c.line(x_dim, p3[1], x_dim - arrow / 2, p3[1] - arrow)
    c.line(x_dim, p0[1], x_dim + arrow / 2, p0[1] + arrow)
    c.line(x_dim, p0[1], x_dim - arrow / 2, p0[1] + arrow)
    c.saveState()
    c.translate(x_dim - 6 * mm, (p0[1] + p3[1]) / 2)
    c.rotate(90)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawCentredString(0, 0, f"{W_mm:.0f} mm")
    c.restoreState()


def generate_drill_pdf_reportlab(order, output_path, filename="Drill_file_reportlab.pdf"):
    os.makedirs(output_path, exist_ok=True)
    out_file = os.path.join(output_path, filename)
    c = canvas.Canvas(out_file, pagesize=A4)
    page_w, page_h = A4
    margin = MARGIN_MM * mm
    header_h = HEADER_HEIGHT_MM * mm

    for cabinet in getattr(order, "cabinets_list", []):
        cabinet.auto_assemble()
        for board in getattr(cabinet, "elements_list", []):
            if board.type != "pal":
            # if not (hasattr(board, "length") and hasattr(board, "width") and hasattr(board, "thick")):
                continue

            L = float(board.length)
            W = float(board.width)
            T = float(board.thick)

            # header
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, page_h - margin - 10,
                         f"Cabinet: {getattr(cabinet,'label','—')}  —  Board: {getattr(board,'label','')}")
            c.setFont("Helvetica", 9)
            c.drawString(margin, page_h - margin - 24,
                         f"{int(L)}×{int(W)}×{int(T)} mm    type: {getattr(board,'type','-')}    material: {getattr(board,'material','-')}")

            # draw board and faces
            front, extruded, scale, ox, oy = draw_board(c, board, page_w, page_h, margin, header_h)
            rects = face_rects(front, extruded)

            # dims + label
            draw_dimensions(c, front, L, W)
            c.setFont("Helvetica", 8)
            if getattr(board, "label", None):
                cx = (front[0][0] + front[2][0]) / 2
                cy = (front[0][1] + front[2][1]) / 2
                c.drawCentredString(cx, cy, board.label)

            # collect holes preserving original a,b for table
            hole_entries = []
            for i, raw in enumerate(getattr(board, "drill_list", []) or []):
                e = parse_drill_entry(raw)
                face = e["face"]
                if not face:
                    continue
                rect = rects.get(face)
                if not rect:
                    continue
                a_mm = float(e["a"])
                b_mm = float(e["b"])
                hole_entries.append({
                    "idx": i + 1,
                    "face": face,
                    "a": a_mm,
                    "b": b_mm,
                    "diameter": float(e["diameter"]),
                    "depth": e["depth"],
                    "note": e["note"],
                    "rect": rect
                })

            # draw holes and labels
            for h in hole_entries:
                px, py, clamped = draw_hole_affine(
                    c, h["rect"], h["face"], h["a"], h["b"], h["diameter"] / 2.0, L, W, T,
                    visible=(h["face"] in ("+z", "-x", "-y"))
                )
                if px is None:
                    continue
                # index label
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 6)
                c.drawString(px + 2, py + 2, str(h["idx"]))
                if clamped:
                    # append a small CLAMPED flag to note so user sees the mismatch
                    h["note"] = (h["note"] + " CLAMPED").strip()

            # hole table with original a,b in mm
            table_x = page_w - margin - 90 * mm
            table_y = margin + 30 * mm
            c.setFont("Helvetica", 8)
            c.drawString(table_x, table_y + 6 * mm, "Holes: idx face a(mm) b(mm) dia depth note")
            y = table_y
            for h in hole_entries:
                depth_txt = f"{h['depth']}" if h['depth'] else ""
                vis_txt = "" if h["face"] in ("+z", "-x", "-y") else "hidden"
                line = f"{h['idx']:>2} {h['face']:>3} {h['a']:6.1f} {h['b']:6.1f} {h['diameter']:5.1f} {depth_txt:>5} {vis_txt} {h['note']}"
                c.drawString(table_x, y, line)
                y -= 10

            c.showPage()

    c.save()
    print(f"Saved drill PDF to {out_file}")
