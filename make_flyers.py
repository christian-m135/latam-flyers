import os, sys
# The renderer is shared by both flyer repos and lives in the meta-campaign skill.
sys.path.insert(0, os.environ.get("FLYER_RENDERER") or os.path.join(
    os.path.expanduser("~"), ".claude", "skills", "meta-campaign", "renderer"))
from PIL import Image, ImageDraw
import flyer_common as fc
fc.use_brand("latam")           # before the star import, which copies the colours as they stand
from flyer_common import *

# Output dir, resolved relative to this file so the script works from any cwd.
SLUG = "accounting-clerk-french"
NAME = "AccountingClerkFR"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", SLUG)

NB = " "   # keeps "100 %" on one line; wrap_fr() below splits on plain spaces only

# Copy language: French (the role requires fluent French). No client name, no salary.
TITLE = "Commis comptable"
TITLE_LINES = ["Commis", "comptable"]          # square-ish formats stack the title
KICKER = "NOUS RECRUTONS"
SUBHEAD = "Télétravail  ·  Freelance  ·  En français"
DESC = ("Soutenez le service comptable d’une entreprise canadienne de mécanique du bâtiment (CVC), "
        "région de Montréal : comptes clients, facturation, recouvrement et comptes fournisseurs.")
DESC_SHORT = ("Comptes clients, facturation et comptes fournisseurs pour une entreprise "
              "canadienne (CVC) de la région de Montréal.")
BULLETS = [
    "100" + NB + "% à distance, de chez vous",
    "En français, équipe au Canada",
    "Temps partiel ou temps plein",
    "Freelance, rémunération en USD",
]
BULLETS_SHORT = [
    "100" + NB + "% à distance, de chez vous",
    "En français, équipe au Canada",
    "Freelance, temps partiel ou plein",
]
# Chip counts are set by measured row width: a wrapped second row is what pushes the
# caption under the footer band on the dense formats, so render() refuses a wrap there.
CHIPS = ["Français courant", "Anglais fonctionnel", "Comptabilité", "Excel"]
CHIPS_SHORT = ["Français courant", "Comptabilité", "Excel"]
CAPTION = "La rigueur comptable, en français."

PANEL_W = 0.63


def wrap_fr(d, txt, fnt, max_w):
    lines = []; cur = ""
    for w in txt.split(" "):
        t = (cur + " " + w).strip(" ")
        if text_w(d, t, fnt) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def fits(y, img, foot, what):
    """The footer overflow is silent in PIL, so make it loud."""
    limit = img.size[1] - foot - 14
    if y > limit:
        raise RuntimeError("%s ends at y=%d, under the footer band (limit %d) on %dx%d"
                           % (what, y, limit, img.size[0], img.size[1]))


def one_row(rows, what):
    if rows != 1:
        raise RuntimeError("chips wrapped to %d rows on %s - cut a chip" % (rows, what))


def save(img, suffix):
    save_flyer(img, os.path.join(OUT, "%s_LATAM_%s.png" % (NAME, suffix)))


def render_1x1():
    W = H = 1080; img = new_canvas(W, H); M = int(W * 0.065); FOOT_H = 92
    light_panel(img, [0, 0, int(W * PANEL_W), H]); d = ImageDraw.Draw(img)
    lw, lh = paste_logo(img, M, M - 8, 86); d = ImageDraw.Draw(img)
    y = M - 8 + lh + 28; y = kicker_line(img, d, M, y, 29, KICKER) + 22
    tf = osw_b(96)
    for ln in TITLE_LINES:
        text(img, d, (M, y), ln, tf, INK, large=True, role="title"); y += 104
    y += 34
    sf = osw_m(fit_size(d, SUBHEAD, osw_m, int(W * 0.545), 33))
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + so + 22
    dimension_line(d, M, y, int(W * 0.58), y); y += 22
    df = inter(27)
    for ln in wrap_fr(d, DESC_SHORT, df, int(W * 0.54)):
        text(img, d, (M, y), ln, df, BODY, role="body"); y += 37
    y += 14
    bf = inter_m(29)
    for b in BULLETS_SHORT:
        d.rectangle([M, y + 9, M + 15, y + 24], fill=ACCENT)
        text(img, d, (M + 31, y), b, bf, INK, role="bullet"); y += 44
    y += 10
    y, rows = chip_row(img, d, M, y, CHIPS_SHORT, inter_sb(25), int(W * 0.565)); one_row(rows, "1x1")
    y += 26
    cf = osw_sb(36); text(img, d, (M, y), CAPTION, cf, INK, role="caption"); ch, co = bbox_h(d, CAPTION, cf)
    fits(y + ch + co, img, FOOT_H, "caption")
    invoice_motif(img, int(W * 0.835), int(H * 0.44), int(W * 0.27), int(H * 0.32))
    footer_band(img, FOOT_H); save(img, "1x1_1080x1080")


def render_9x16():
    """Stories and Reels. Everything a reader must see - kicker, title, subhead, bullets,
    chips - sits in the safe zone y=270..1250; the renderer fails the render otherwise.
    The description is left to the ad's primary text. Motif, caption and footer sit in
    the lower zone that the Reels interface covers, so nothing there is essential."""
    W, H = 1080, 1920; img = new_canvas(W, H); M = int(W * 0.075); FOOT_H = 118
    top, bottom = safe_zone(img)
    light_panel(img, [0, top - 34, W, bottom + 16]); d = ImageDraw.Draw(img)
    y = top + 12
    lw, lh = paste_logo(img, M, y, 92); d = ImageDraw.Draw(img)
    y += lh + 32; y = kicker_line(img, d, M, y, 34, KICKER) + 26
    tf = osw_b(fit_size(d, TITLE, osw_b, W - 2 * M, 130))
    text(img, d, (M, y), TITLE, tf, INK, large=True, role="title"); th, off = bbox_h(d, TITLE, tf); y += th + off + 20
    sf = osw_m(fit_size(d, SUBHEAD, osw_m, W - 2 * M, 46))
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + so + 26
    dimension_line(d, M, y, W - M, y); y += 30
    bf = inter_m(48)
    for b in BULLETS:
        d.rectangle([M, y + 16, M + 22, y + 38], fill=ACCENT)
        text(img, d, (M + 42, y), b, bf, INK, role="bullet"); y += 71
    y += 10
    y, rows = chip_row(img, d, M, y, CHIPS, inter_sb(34), W - 2 * M, gap=14, padx=22, pady=12)
    if rows > 2:
        raise RuntimeError("chips wrapped to %d rows on 9x16 - cut a chip" % rows)
    # Below the safe zone: decorative only.
    invoice_motif(img, W // 2, 1462, int(W * 0.30), 300)
    cf = osw_sb(54); ch, co = bbox_h(d, CAPTION, cf); cy = 1672
    text(img, d, (M, cy), CAPTION, cf, INK, role="caption")
    fits(cy + ch + co, img, FOOT_H, "caption")
    footer_band(img, FOOT_H); save(img, "9x16_1080x1920")


def render_191x1():
    W, H = 1200, 628; img = new_canvas(W, H); M = int(W * 0.05); FOOT_H = 70
    light_panel(img, [0, 0, int(W * 0.63), H]); d = ImageDraw.Draw(img)
    lw, lh = paste_logo(img, M, int(H * 0.07), 64); d = ImageDraw.Draw(img)
    y = int(H * 0.07) + lh + 20; y = kicker_line(img, d, M, y, 24, KICKER) + 16
    tf = osw_b(fit_size(d, TITLE, osw_b, int(W * 0.56), 84))
    text(img, d, (M, y), TITLE, tf, INK, large=True, role="title"); th, off = bbox_h(d, TITLE, tf); y += th + off + 12
    sf = osw_m(fit_size(d, SUBHEAD, osw_m, int(W * 0.56), 27))
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + so + 18
    bf = inter_m(25)
    for b in BULLETS_SHORT:
        d.rectangle([M, y + 8, M + 14, y + 22], fill=ACCENT)
        text(img, d, (M + 28, y), b, bf, INK, role="bullet"); y += 37
    y += 6
    y, rows = chip_row(img, d, M, y, CHIPS_SHORT, inter_sb(22), int(W * 0.56)); one_row(rows, "1.91x1")
    fits(y, img, FOOT_H, "chips")
    invoice_motif(img, int(W * 0.815), int(H * 0.445), int(W * 0.25), int(H * 0.60))
    footer_band(img, FOOT_H); save(img, "1.91x1_1200x628")


def render_4x5():
    W, H = 1080, 1350; img = new_canvas(W, H); M = int(W * 0.065); FOOT_H = 96
    light_panel(img, [0, 0, int(W * PANEL_W), H]); d = ImageDraw.Draw(img)
    lw, lh = paste_logo(img, M, M, 92); d = ImageDraw.Draw(img)
    y = M + lh + 36; y = kicker_line(img, d, M, y, 30, KICKER) + 28
    tf = osw_b(104)
    for ln in TITLE_LINES:
        text(img, d, (M, y), ln, tf, INK, large=True, role="title"); y += 114
    y += 44
    sf = osw_m(fit_size(d, SUBHEAD, osw_m, int(W * 0.545), 34))
    text(img, d, (M, y), SUBHEAD, sf, TEXT_ACCENT, role="subhead"); sh, so = bbox_h(d, SUBHEAD, sf); y += sh + so + 30
    dimension_line(d, M, y, int(W * 0.58), y); y += 30
    df = inter(29)
    for ln in wrap_fr(d, DESC, df, int(W * 0.54)):
        text(img, d, (M, y), ln, df, BODY, role="body"); y += 41
    y += 20
    bf = inter_m(31)
    for b in BULLETS:
        d.rectangle([M, y + 9, M + 16, y + 25], fill=ACCENT)
        text(img, d, (M + 32, y), b, bf, INK, role="bullet"); y += 49
    y += 14
    y, rows = chip_row(img, d, M, y, CHIPS_SHORT, inter_sb(27), int(W * 0.565)); one_row(rows, "4x5")
    y += 34
    cf = osw_sb(40); text(img, d, (M, y), CAPTION, cf, INK, role="caption"); ch, co = bbox_h(d, CAPTION, cf)
    fits(y + ch + co, img, FOOT_H, "caption")
    invoice_motif(img, int(W * 0.835), int(H * 0.40), int(W * 0.27), int(H * 0.27))
    footer_band(img, FOOT_H); save(img, "4x5_1080x1350")


os.makedirs(OUT, exist_ok=True)
render_1x1(); render_9x16(); render_191x1(); render_4x5()
print("rendered:", sorted(f for f in os.listdir(OUT) if not f.startswith("_")))
print("contrast:", contrast_report())
