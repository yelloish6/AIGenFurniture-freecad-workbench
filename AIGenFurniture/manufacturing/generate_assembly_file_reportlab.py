# save as generate_drill_reportlab.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
import math
import os

# Visual / projection parameters
VIEW_ANGLE_DEG = 30  # like your original VIEW_ANGLE
PAGE_SIZE = A4
MARGIN_MM = 12
HEADER_HEIGHT_MM = 18
DEFAULT_DRAW_AREA = (PAGE_SIZE[0] - 2 * MARGIN_MM * mm,
                     PAGE_SIZE[1] - 2 * MARGIN_MM * mm - HEADER_HEIGHT_MM * mm)

def normalize_face_code(face):
    """Normalize face name to canonical token."""
    if face is None:
        return None
    s = str(face).lower()
    if s in ("+x", "right", "r"):
        return "+x"
    if s in ("-x", "left", "l"):
        return "-x"
    if s in ("+y", "up", "u", "top"):
        return "+y"
    if s in ("-y", "down", "d", "bottom"):
        return "-y"
    if s in ("+z", "front", "f"):
        return "+z"
    if s in ("-z", "back", "b"):
        return "-z"
    return face

def parse_drill_entry(entry):
    """
    Accept either tuple/list or dict.
    Tuple convention used here:
      (diameter_mm, face, a, b, depth_mm_opt, note_opt)
    where (a,b) meaning depends on face (see top-level comment).
    Returns dict with keys: diameter, face, a, b, depth, note
    """
    if isinstance(entry, dict):
        diameter = float(entry.get("diameter", entry.get("d", 0)))
        face = normalize_face_code(entry.get("face", entry.get("side")))
        a = entry.get("a", entry.get("x", None))
        b = entry.get("b", entry.get("y", None))
        depth = entry.get("depth", None)
        note = entry.get("note", "")
        return {"diameter": diameter, "face": face, "a": a, "b": b, "depth": depth, "note": note}
    elif isinstance(entry, (list, tuple)):
        # destruct tuple safely
        diameter = float(entry[0]) if len(entry) > 0 else 0.0
        face = normalize_face_code(entry[1]) if len(entry) > 1 else None
        a = entry[2] if len(entry) > 2 else None
        b = entry[3] if len(entry) > 3 else None
        depth = entry[4] if len(entry) > 4 else None
        note = entry[5] if len(entry) > 5 else ""
        return {"diameter": float(diameter), "face": face, "a": a, "b": b, "depth": depth, "note": note}
    else:
        raise ValueError("Unsupported drill_list entry type: " + str(type(entry)))

def generate_drill_pdf_reportlab(order, output_path, filename="Drill_file_reportlab.pdf",
                                 view_angle_deg=VIEW_ANGLE_DEG):
    """
    Generate a PDF of drill coordinates for each Board-like element in the order's cabinets.
    Uses ReportLab. One page per board.

    order.cabinets_list -> iterate cabinets
    cabinet.elements_list -> iterate elements, filter Board-like by having .length,.width,.thick and .position and .drill_list
    """

    # projection basis (matches your fitz code: depth vector projected with cos/sin)
    angle_rad = math.radians(view_angle_deg)
    angle_x = math.cos(angle_rad)
    angle_z = math.sin(angle_rad)

    # create canvas
    out_path = os.path.join(output_path, filename)
    c = canvas.Canvas(out_path, pagesize=PAGE_SIZE)
    page_w, page_h = PAGE_SIZE
    margin = MARGIN_MM * mm
    header_h = HEADER_HEIGHT_MM * mm

    for cabinet in getattr(order, "cabinets_list", []):
        for elem in getattr(cabinet, "elements_list", []):
            # detect board-like element
            if not (hasattr(elem, "length") and hasattr(elem, "width") and hasattr(elem, "thick") and hasattr(elem, "position")):
                continue

            board = elem
            # dimensions (use actual physical dimensions)
            L = float(board.length)  # length along x (mm)
            W = float(board.width)   # width along y (mm)
            T = float(board.thick)   # thickness along z (mm)

            # offsets from position[3..5] (can be negative)
            pos = getattr(board, "position", [L, W, T, 0.0, 0.0, 0.0])
            x_off = float(pos[3])
            y_off = float(pos[4])
            z_off = float(pos[5])

            # compute a scale to fit the drawing into available draw area
            draw_area_w, draw_area_h = DEFAULT_DRAW_AREA
            # compute projected extents in the same style as your fitz code:
            # projected_x_extent ~ L + W * angle_x
            # projected_y_extent ~ T + W * angle_z
            proj_w_mm = L + W * angle_x
            proj_h_mm = T + W * angle_z
            # convert mm to points (use mm->pt later); compute scale to fit into area
            pts_per_mm = mm
            scale = min(draw_area_w / (proj_w_mm * pts_per_mm), draw_area_h / (proj_h_mm * pts_per_mm), 1.0)

            # set origin (bottom-left corner of front face projected)
            # mimic your existing origin calc: start from margin + offsets
            # We map x_off, y_off offsets into the drawing similarly:
            ox = margin + (x_off * pts_per_mm + y_off * angle_x * pts_per_mm) * scale
            oy = margin + header_h + draw_area_h - ((z_off * pts_per_mm) + (y_off * angle_z * pts_per_mm)) * scale - (T * pts_per_mm * scale)

            # helper: project a 3D board-local point (x,y,z) in mm -> page points
            def project(x_mm, y_mm, z_mm):
                px = ox + (x_mm * pts_per_mm + y_mm * angle_x * pts_per_mm) * scale
                py = oy + (- y_mm * angle_z * pts_per_mm + z_mm * pts_per_mm) * scale
                return (px, py)

            # draw header
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, page_h - margin - 10, f"Cabinet: {getattr(cabinet, 'label', '—')}  —  Board: {getattr(board, 'label', '')}")
            c.setFont("Helvetica", 9)
            c.drawString(margin, page_h - margin - 24, f"{int(L)}×{int(W)}×{int(T)} mm  type: {getattr(board,'type','-')}  material: {getattr(board,'material','-')}")

            # draw three principal faces: front, top, right (like original)
            # points for the front rectangle (z from 0 to T, x from 0..L, y=0)
            p_front_bl = project(0, 0, 0)         # origin lower-left of front face
            p_front_br = project(L, 0, 0)
            p_front_tl = project(0, 0, T)
            p_front_tr = project(L, 0, T)
            # top face (y = W plane): quad (project(0,W,T) ... etc)
            p_top_bl = project(0, W, 0)
            p_top_br = project(L, W, 0)
            p_top_tl = project(0, W, T)
            p_top_tr = project(L, W, T)
            # right face (x = L plane): quad
            p_right_bl = project(L, 0, 0)
            p_right_br = project(L, W, 0)
            p_right_tl = project(L, 0, T)
            p_right_tr = project(L, W, T)

            # draw faces: front (filled white), top (light grey), right (light grey)
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            # fill order: top -> right -> front so front draws on top
            # helper to draw filled polygons on canvas
            def draw_polygon(c, points, fill_color=colors.whitesmoke, stroke_color=colors.black, stroke=1, fill=1):
                path = c.beginPath()
                x0, y0 = points[0]
                path.moveTo(x0, y0)
                for (x, y) in points[1:]:
                    path.lineTo(x, y)
                path.close()
                c.setFillColor(fill_color)
                c.setStrokeColor(stroke_color)
                c.drawPath(path, stroke=stroke, fill=fill)

            # draw faces: top -> right -> front
            draw_polygon(c, [p_top_bl, p_top_br, p_top_tr, p_top_tl], fill_color=colors.whitesmoke)
            draw_polygon(c, [p_right_bl, p_right_br, p_right_tr, p_right_tl], fill_color=colors.whitesmoke)
            draw_polygon(c, [p_front_bl, p_front_br, p_front_tr, p_front_tl], fill_color=colors.white)

            # draw boards label centered on the front
            c.setFont("Helvetica", 8)
            center_front_x = (p_front_bl[0] + p_front_br[0]) / 2
            center_front_y = (p_front_bl[1] + p_front_tl[1]) / 2 + 4
            c.drawCentredString(center_front_x, center_front_y, board.label if getattr(board, "label", None) else "")

            # collect hole entries
            hole_entries = []
            for i, raw in enumerate(getattr(board, "drill_list", []) or []):
                entry = parse_drill_entry(raw)
                face = entry["face"]
                diameter = float(entry["diameter"])
                depth = entry.get("depth", None)
                note = entry.get("note", "")

                # map a,b to 3D (x_mm, y_mm, z_mm) depending on face:
                a = entry["a"]
                b = entry["b"]
                # guard: missing coords -> skip
                if a is None or b is None:
                    continue

                if face == "+z":            # front face: (x=a, y=b), z = T
                    x3, y3, z3 = float(a), float(b), T
                elif face == "-z":          # back face: z = 0
                    x3, y3, z3 = float(a), float(b), 0.0
                elif face == "+x":          # right face (x = L): coords (y,z) -> a=y, b=z
                    x3, y3, z3 = L, float(a), float(b)
                elif face == "-x":          # left face (x = 0)
                    x3, y3, z3 = 0.0, float(a), float(b)
                elif face == "+y":          # top face (y = W): coords (x,z)
                    x3, y3, z3 = float(a), W, float(b)
                elif face == "-y":          # bottom face (y = 0)
                    x3, y3, z3 = float(a), 0.0, float(b)
                else:
                    # unknown face: skip
                    continue

                # compute 2D projection
                px, py = project(x3, y3, z3)
                # circle radius in pts
                r_pts = (diameter / 2.0) * mm * scale
                # determine if face is "visible" in this view:
                # approximate visibility: we assume front (+z), top (+y), right (+x) are visible
                visible_faces = {"+z", "+y", "+x"}
                visible = (face in visible_faces)

                hole_entries.append({
                    "idx": i + 1,
                    "face": face,
                    "x3": x3, "y3": y3, "z3": z3,
                    "px": px, "py": py,
                    "diameter": diameter,
                    "depth": depth,
                    "note": note,
                    "r_pts": r_pts,
                    "visible": visible
                })

            # draw holes: visible = solid circle, hidden = dashed circle
            for h in hole_entries:
                if h["visible"]:
                    c.setDash()  # solid
                    c.setStrokeColor(colors.red)
                    c.circle(h["px"], h["py"], h["r_pts"], stroke=1, fill=0)
                else:
                    c.setDash(3, 3)
                    c.setStrokeColor(colors.red)
                    c.circle(h["px"], h["py"], h["r_pts"], stroke=1, fill=0)
                    c.setDash()  # reset

                # small index near hole
                c.setFont("Helvetica", 6)
                c.setFillColor(colors.black)
                c.drawString(h["px"] + 1.5 * mm * scale, h["py"] + 1.5 * mm * scale, str(h["idx"]))

            # draw hole table on the lower right area of the page
            c.setFont("Helvetica", 8)
            table_x = page_w - margin - 90 * mm
            table_y = margin + 20 * mm
            line_h = 10
            c.drawString(table_x, table_y + 6 * mm, "Holes (index, face, X(mm), Y(mm), Z(mm), Dia(mm), Depth, note)")
            y = table_y
            for h in hole_entries:
                visible_note = "" if h["visible"] else "hidden"
                depth_txt = f"{h['depth']}" if h['depth'] is not None else ""
                txt = f"{h['idx']:>2}: {h['face']:>3}  {h['x3']:6.1f}  {h['y3']:6.1f}  {h['z3']:6.1f}  {h['diameter']:5.1f}  {depth_txt:>5}  {visible_note} {h['note']}"
                c.drawString(table_x, y, txt)
                y -= line_h
                # if table area overflows page, it will overwrite — you can split into multiple pages if needed

            # finished page
            c.showPage()

    c.save()
    print(f"Saved PDF to {out_path}")
