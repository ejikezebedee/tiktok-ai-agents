#!/usr/bin/env python3
"""Motion-graphics TikTok renderer #2: '5 Things an AI Agent Can Do'.
Pure Pillow + ffmpeg, CPU-only, 1080x1920 30fps."""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 30
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG_TOP = (10, 14, 26)
BG_BOT = (17, 24, 46)
CYAN = (34, 211, 238)
BLUE = (59, 130, 246)
WHITE = (245, 248, 255)
YELLOW = (250, 204, 21)
GREY = (148, 163, 184)
GREEN = (34, 197, 94)

_BG = Image.new('RGBA', (W, H))
_bd = ImageDraw.Draw(_BG)
for y in range(H):
    t = y / H
    _bd.line([(0,y),(W,y)], fill=(int(BG_TOP[0]+(BG_BOT[0]-BG_TOP[0])*t),
                                    int(BG_TOP[1]+(BG_BOT[1]-BG_TOP[1])*t),
                                    int(BG_TOP[2]+(BG_BOT[2]-BG_TOP[2])*t), 255))

_FONT_CACHE = {}
def font(size, bold=True):
    k = (size, bold)
    if k not in _FONT_CACHE:
        _FONT_CACHE[k] = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    return _FONT_CACHE[k]

_GLOW_CACHE = {}
def glow_sprite(color, r):
    k = (color, r)
    if k in _GLOW_CACHE: return _GLOW_CACHE[k]
    size = r*2 + 40
    s = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(s)
    for i in range(4, 0, -1):
        rr = r + i*8
        d.ellipse([size//2-rr, size//2-rr, size//2+rr, size//2+rr], fill=(color[0],color[1],color[2],max(6,42-i*9)))
    s = s.filter(ImageFilter.GaussianBlur(7))
    _GLOW_CACHE[k] = s
    return s

def bg(img): img.paste(_BG, (0,0))

def text_c(d, s, y, size, color=WHITE, bold=True, border=3, bcol=(0,0,0,255)):
    f = font(size, bold)
    w = d.textlength(s, font=f)
    d.text(((W-w)/2, y), s, font=f, fill=color, stroke_width=border, stroke_fill=bcol)
    return f

def text_l(d, s, x, y, size, color=WHITE, bold=True, border=2):
    f = font(size, bold)
    d.text((x, y), s, font=f, fill=color, stroke_width=border, stroke_fill=(0,0,0,255))
    return f

def glow_circle(img, cx, cy, r, color):
    spr = glow_sprite(color, r)
    img.alpha_composite(spr, (int(cx)-spr.width//2, int(cy)-spr.height//2))
    d = ImageDraw.Draw(img)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    return d

def round_rect(d, box, r, fill, outline=None, ow=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=ow)

def chip(img, cx, cy, w, h, label, color, tsize=30, tcol=(10,14,26,255)):
    d = ImageDraw.Draw(img)
    round_rect(d, (cx-w//2, cy-h//2, cx+w//2, cy+h//2), 18, color)
    f = font(tsize, True)
    tw = d.textlength(label, font=f)
    d.text((cx-tw/2, cy-tsize//2), label, font=f, fill=tcol)

def arrow_h(d, x1, x2, y, color, w=6):
    d.line([(x1,y),(x2,y)], fill=color, width=w)
    d.polygon([(x2,y),(x2-16,y-12),(x2-16,y+12)], fill=color)

def arrow_v(d, x, y1, y2, color, w=6):
    d.line([(x,y1),(x,y2)], fill=color, width=w)
    d.polygon([(x,y2),(x-12,y2-16),(x+12,y2-16)], fill=color)

# ============ SCENES ============

def scene_hook(img, p):
    d = ImageDraw.Draw(img); bg(img)
    if p < 0.5:
        # chatbot phase
        round_rect(d, (240, int(H*0.20), 840, int(H*0.20)+130), 30, (37,60,100,255))
        text_c(d, "Ask a question...", int(H*0.20)+48, 40, WHITE)
        text_c(d, "CHATBOT", H*0.34, 54, GREY)
        text_c(d, "ask  ->  answer", H*0.42, 46, YELLOW, border=3)
    else:
        q = (p-0.5)/0.5
        glow_circle(img, W//2, int(H*0.30), 120, BLUE)
        d2 = ImageDraw.Draw(img)
        text_c(d2, "AI AGENT", H*0.30, 88, CYAN, border=5)
        text_c(d2, "does the work", H*0.40, 52, WHITE)
        tools = ["Email", "Calendar", "CRM", "Data"]
        xs = [270, 540, 810, 540]
        ys = [int(H*0.56), int(H*0.56), int(H*0.56), int(H*0.68)]
        for i in range(min(4, int(q*4)+1)):
            chip(img, xs[i], ys[i], 220, 90, tools[i], (30,64,120,255), 34, WHITE)
        d3 = ImageDraw.Draw(img)
        for i in range(1, min(4, int(q*4)+1)):
            arrow_h(d3, xs[i-1]+110, xs[i]-110, ys[i], CYAN, 5)

def scene_email(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_l(d, "1 / 5", 60, 60, 40, GREY)
    text_c(d, "READ EMAILS", H*0.13, 64, CYAN, border=4)
    for i in range(6):
        local = p*6 - i
        if local <= 0: continue
        y = int(H*0.22) + i*66
        round_rect(d, (60, y, 470, y+46), 14, (37,60,100,255))
    steps = ["READ", "CLASSIFY", "PRIORITIZE", "DRAFT"]
    y0 = int(H*0.26)
    shown = min(4, int(p*4)+1)
    for i in range(shown):
        y = y0 + i*110
        chip(img, 720, y, 300, 84, steps[i], (59,130,246,255) if i<3 else (250,204,21,255), 30)
    if shown > 1:
        d2 = ImageDraw.Draw(img)
        for i in range(1, shown):
            arrow_v(d2, 720, y0+(i-1)*110+42, y0+i*110-42, CYAN, 6)
    if p > 0.72:
        round_rect(d, (120, int(H*0.82), 960, int(H*0.82)+108), 24, (250,204,21,255))
        text_c(d, "HUMAN REVIEW REQUIRED", int(H*0.82)+34, 40, (10,14,26,255))

def scene_leads(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_l(d, "2 / 5", 60, 60, 40, GREY)
    text_c(d, "FIND LEADS", H*0.13, 64, CYAN, border=4)
    steps = ["Business Search", "Public Info", "Qualify Leads", "Create Report"]
    y0 = int(H*0.22)
    shown = min(4, int(p*4)+1)
    for i in range(shown):
        y = y0 + i*88
        chip(img, W//2, y, 560, 70, steps[i], (30,64,120,255) if i<3 else (34,197,94,255), 30, WHITE)
        if i > 0:
            arrow_v(d, W//2, y0+(i-1)*88+35, y-35, CYAN, 5)
    if p > 0.6:
        rows = [("Alpha Ltd", "Logistics", "High"),
                ("Beta GmbH", "Retail", "Med"),
                ("Gamma Co", "Finance", "High")]
        for i, (c, ind, pri) in enumerate(rows):
            local = (p-0.6)*3.5 - i
            if local <= 0: continue
            y = int(H*0.66) + i*110
            round_rect(d, (100, y, 980, y+92), 18, (25,40,75,255))
            text_l(d, c, 140, y+20, 34, WHITE)
            text_l(d, ind, 140, y+54, 26, GREY)
            text_l(d, pri, 780, y+28, 30, YELLOW)

def scene_calendar(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_l(d, "3 / 5", 60, 60, 40, GREY)
    text_c(d, "MANAGE CALENDAR", H*0.13, 64, CYAN, border=4)
    # calendar grid
    gx, gy = 200, int(H*0.24)
    cw, ch = 90, 80
    for r in range(5):
        for c in range(7):
            x = gx + c*(cw+8); y = gy + r*(ch+8)
            col = (37,60,100,255) if (r+c) % 3 else (30,64,120,255)
            round_rect(d, (x, y, x+cw, y+ch), 12, col)
    if p > 0.35:
        slots = ["10:00", "13:30", "15:00"]
        for i, s in enumerate(slots):
            local = (p-0.35)*2.5 - i
            if local <= 0: continue
            y = int(H*0.72) + i*100
            round_rect(d, (240, y, 840, y+80), 20, (30,64,120,255), outline=CYAN, ow=2)
            text_c(d, s, y+22, 40, WHITE)
    if p > 0.8:
        round_rect(d, (560, int(H*0.72), 880, int(H*0.72)+80), 22, (34,197,94,255))
        text_c(d, "APPROVE", int(H*0.72)+22, 40, (10,14,26,255))

def scene_report(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_l(d, "4 / 5", 60, 60, 40, GREY)
    text_c(d, "ANALYZE DATA", H*0.13, 64, CYAN, border=4)
    bars = [("Sales", 0.8, CYAN), ("Expenses", 0.5, YELLOW), ("Customers", 0.65, BLUE), ("Trends", 0.9, GREEN)]
    bx = 180
    for i, (name, val, col) in enumerate(bars):
        local = p*4 - i
        if local <= 0: continue
        y = int(H*0.24) + i*150
        hgt = int(120 * val * min(1.0, local))
        round_rect(d, (bx, y, bx+90, y+140), 12, (37,60,100,255))
        round_rect(d, (bx, y+140-hgt, bx+90, y+140), 12, col)
        text_l(d, name, bx+110, y+50, 34, WHITE)
    if p > 0.65:
        round_rect(d, (160, int(H*0.82), 920, int(H*0.82)+130), 22, (25,40,75,255), outline=WHITE, ow=2)
        text_c(d, "WEEKLY BUSINESS REPORT", int(H*0.82)+22, 36, CYAN)
        text_c(d, "charts + recommendations", int(H*0.82)+68, 30, GREY)

def scene_coordinate(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_l(d, "5 / 5", 60, 60, 40, GREY)
    text_c(d, "COORDINATE WORK", H*0.13, 64, CYAN, border=4)
    # human supervision
    text_c(d, "HUMAN SUPERVISION", H*0.22, 40, YELLOW, border=3)
    cx, cy = W//2, int(H*0.50)
    glow_circle(img, cx, cy, 66, CYAN)
    d2 = ImageDraw.Draw(img)
    d2.ellipse([cx-66, cy-66, cx+66, cy+66], fill=(34,211,238,255))
    text_c(d2, "MAIN", cy-34, 34, (10,14,26,255))
    text_c(d2, "AGENT", cy+2, 34, (10,14,26,255))
    labels = ["EMAIL", "RESEARCH", "SALES", "DATA", "CODING"]
    for i in range(5):
        ang = p*2*math.pi + i*2*math.pi/5
        rr = 360
        nx = cx + rr*math.cos(ang); ny = cy + rr*math.sin(ang)
        glow_circle(img, int(nx), int(ny), 42, BLUE if i%2==0 else (30,64,120,255))
        d3 = ImageDraw.Draw(img)
        d3.ellipse([int(nx)-42, int(ny)-42, int(nx)+42, int(ny)+42], fill=(59,130,246,255) if i%2==0 else (30,64,120,255))
        f = font(28); tw = d3.textlength(labels[i], font=f)
        d3.text((int(nx)-tw/2, int(ny)-14), labels[i], font=f, fill=WHITE)
        d3.line([(cx,cy),(int(nx),int(ny))], fill=(60,80,120,255), width=3)

def scene_cta(img, p):
    d = ImageDraw.Draw(img); bg(img)
    glow_circle(img, W//2, H//2-100, 150, BLUE)
    d2 = ImageDraw.Draw(img)
    text_c(d2, "AI THAT", H*0.34, 72, WHITE)
    text_c(d2, "TAKES ACTION", H*0.42, 72, CYAN, border=5)
    if p > 0.35:
        text_c(d2, "FOLLOW", H*0.60, 78, YELLOW, border=6)

SCENES = [
    ("hook", 4.0, scene_hook),
    ("email", 8.0, scene_email),
    ("leads", 7.0, scene_leads),
    ("calendar", 7.0, scene_calendar),
    ("report", 7.0, scene_report),
    ("coordinate", 8.0, scene_coordinate),
    ("cta", 9.0, scene_cta),
]

def render_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    frame = 0
    for name, dur, fn in SCENES:
        n = int(dur * FPS)
        for k in range(n):
            p = k / max(1, n-1)
            img = Image.new('RGBA', (W, H), (0,0,0,0))
            fn(img, p)
            img.convert('RGB').save(f"{outdir}/{frame:05d}.png")
            frame += 1
    print("total frames:", frame, flush=True)

if __name__ == "__main__":
    render_all("/tmp/tkframes2")
