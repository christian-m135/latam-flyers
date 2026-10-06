import os, sys
# The renderer is shared by both flyer repos and lives in the meta-campaign skill.
sys.path.insert(0, os.environ.get("FLYER_RENDERER") or os.path.join(
    os.path.expanduser("~"), ".claude", "skills", "meta-campaign", "renderer"))
from PIL import Image, ImageDraw
import flyer_common as fc
fc.use_brand("latam")
from flyer_common import *

SLUG = "accounting-clerk-french"

# Three candidates for Accounting Clerk (French). B, the invoice sheet, was chosen and
# lives in the renderer as invoice_motif(); A and C stay here as the record of what
# was considered.


def taccount_motif(img, cx, cy, w, h, label_room=True):
    """T-account with debit and credit entries ruled off to a balance - double-entry bookkeeping."""
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    def px(f): return x0 + (x1 - x0) * f
    def py(f): return y0 + (y1 - y0) * f
    for i in range(1, 7):
        d.line([(x0, py(0.16 + i * 0.105)), (x1, py(0.16 + i * 0.105))], fill=FAINT, width=1)
    d.line([(px(0.30), py(0.05)), (px(0.70), py(0.05))], fill=ACCENT, width=3)        # account name
    d.line([(x0, py(0.16)), (x1, py(0.16))], fill=STRUCT, width=3)               # the T bar
    d.line([(px(0.5), py(0.16)), (px(0.5), py(0.86))], fill=STRUCT, width=3)     # the T stem
    for i, ln in enumerate((0.30, 0.22, 0.34, 0.26)):                              # debits
        y = py(0.265 + i * 0.105)
        d.line([(px(0.44) - w * ln, y), (px(0.44), y)], fill=ACCENT, width=3)
    for i, ln in enumerate((0.26, 0.33, 0.20)):                                    # credits
        y = py(0.265 + i * 0.105)
        d.line([(px(0.94) - w * ln, y), (px(0.94), y)], fill=ACCENT, width=3)
    for (a, b) in ((0.08, 0.44), (0.58, 0.94)):                                    # ruled-off totals
        d.line([(px(a), py(0.74)), (px(b), py(0.74))], fill=STRUCT, width=2)
        d.line([(px(a), py(0.86)), (px(b), py(0.86))], fill=STRUCT, width=2)
        d.line([(px(a), py(0.895)), (px(b), py(0.895))], fill=STRUCT, width=2)
    d.line([(px(0.58), py(0.80)), (px(0.94), py(0.80))], fill=ACCENT, width=3)        # the balance
    d.line([(px(0.14), py(0.80)), (px(0.44), py(0.80))], fill=ACCENT, width=3)
    dimension_line(d, x0 - 24, py(0.16), x0 - 24, py(0.895))
    return (x0, y0, x1, y1)


def aging_motif(img, cx, cy, w, h, label_room=True):
    """Receivables aging chart: four buckets falling away, the 30-60 day window called out - collections."""
    d = ImageDraw.Draw(img)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    def px(f): return x0 + (x1 - x0) * f
    def py(f): return y0 + (y1 - y0) * f
    for i in range(1, 5):
        d.line([(x0, py(i / 5)), (x1, py(i / 5))], fill=FAINT, width=1)
    d.line([(x0, y1), (x1, y1)], fill=STRUCT, width=3)
    d.line([(x0, y0), (x0, y1)], fill=STRUCT, width=3)
    heights = (0.82, 0.56, 0.36, 0.18)
    bw, gap = 0.165, 0.065
    tops = []
    for i, hh in enumerate(heights):
        bx0 = px(0.085 + i * (bw + gap)); bx1 = bx0 + w * bw
        by = y1 - (y1 - y0) * hh
        d.line([(bx0, y1), (bx0, by), (bx1, by), (bx1, y1)], fill=STRUCT, width=3)
        tops.append(((bx0 + bx1) / 2, by, bx0, bx1))
    pts = [(t[0], t[1] - h * 0.07) for t in tops]
    d.line(pts, fill=ACCENT, width=3)
    for (qx, qy) in pts:
        d.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill=ACCENT, outline=(255, 255, 255), width=1)
    d.line([(tops[1][2], y1 + 26), (tops[2][3], y1 + 26)], fill=ACCENT, width=2)
    dimension_line(d, tops[1][2], y1 + 26, tops[2][3], y1 + 26)
    return (x0, y0, x1, y1)


if __name__ == "__main__":
    W, H = 1200, 480
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    for i, (label, fn) in enumerate([("A", taccount_motif), ("B", invoice_motif), ("C", aging_motif)]):
        cx = int(W * (i + 0.5) / 3)
        d.text((cx - 10, 30), label, font=osw_b(44), fill=INK)
        fn(img, cx, 280, 290, 260)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", SLUG)
    os.makedirs(out, exist_ok=True)
    img.convert("RGB").save(os.path.join(out, "_motif-options.png"), "PNG")
    print("saved", os.path.join(out, "_motif-options.png"))
