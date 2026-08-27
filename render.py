#!/usr/bin/env python3
"""Motion-graphics TikTok renderer for 'AI Agents' explainer.
Pure Pillow + ffmpeg, CPU-only. Renders 8 animated scenes at 1080x1920 30fps.
Optimized: background + glow sprites pre-rendered once."""
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

# Pre-render background once
_BG = Image.new('RGBA', (W, H))
_bd = ImageDraw.Draw(_BG)
for y in range(H):
    t = y / H
    r = int(BG_TOP[0] + (BG_BOT[0]-BG_TOP[0])*t)
    g = int(BG_TOP[1] + (BG_BOT[1]-BG_TOP[1])*t)
    b = int(BG_TOP[2] + (BG_BOT[2]-BG_TOP[2])*t)
    _bd.line([(0,y),(W,y)], fill=(r,g,b,255))

_FONT_CACHE = {}
def font(size, bold=True):
    k = (size, bold)
    if k not in _FONT_CACHE:
        _FONT_CACHE[k] = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    return _FONT_CACHE[k]

_GLOW_CACHE = {}
def glow_sprite(color, r):
    k = (color, r)
    if k in _GLOW_CACHE:
        return _GLOW_CACHE[k]
    size = r*2 + 40
    s = Image.new('RGBA', (size, size), (0,0,0,0))
    d = ImageDraw.Draw(s)
    for i in range(4, 0, -1):
        rr = r + i*8
        a = max(6, 42 - i*9)
        d.ellipse([size//2-rr, size//2-rr, size//2+rr, size//2+rr], fill=(color[0],color[1],color[2],a))
    s = s.filter(ImageFilter.GaussianBlur(7))
    _GLOW_CACHE[k] = s
    return s

def bg(img):
    img.paste(_BG, (0,0))

def text_c(d, s, y, size, color=WHITE, bold=True, border=3, bcol=(0,0,0,255)):
    f = font(size, bold)
    w = d.textlength(s, font=f)
    x = (W - w)/2
    d.text((x, y), s, font=f, fill=color, stroke_width=border, stroke_fill=bcol)
    return x, y, w, size

def glow_circle(img, cx, cy, r, color):
    spr = glow_sprite(color, r)
    img.alpha_composite(spr, (int(cx)-spr.width//2, int(cy)-spr.height//2))
    d = ImageDraw.Draw(img)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    return d

def round_rect(d, box, r, fill, outline=None, ow=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=ow)

def node(img, cx, cy, r, color, label=None, lsize=30):
    d = glow_circle(img, cx, cy, r, color)
    if label:
        f = font(lsize)
        w = d.textlength(label, font=f)
        d.text((cx-w/2, cy-lsize/2), label, font=f, fill=(10,14,26,255))

def line(d, a, b, color, w=6):
    d.line([a, b], fill=color, width=w)

# ============ SCENES ============
def scene_hook(img, p):
    d = ImageDraw.Draw(img); bg(img)
    r = 160 + int(30*math.sin(p*math.pi))
    glow_circle(img, W//2, H//2 - 120, r, BLUE)
    d = ImageDraw.Draw(img)
    scale = 1.0 + 0.04*math.sin(p*2*math.pi)
    text_c(d, "AI AGENTS", H*0.40, int(110*scale), CYAN, border=5)
    if p > 0.4:
        text_c(d, "the next shift", H*0.50, 54, WHITE, border=3)

def scene_chatbot(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "CHATBOT", H*0.30, 70, WHITE)
    if p > 0.15:
        round_rect(d, (120, int(H*0.40), 560, int(H*0.40)+120), 28, (37,60,100,255))
        text_c(d, "Ask", 540, 44, WHITE)
    if p > 0.45:
        round_rect(d, (520, int(H*0.40)+150, 960, int(H*0.40)+270), 28, (30,64,120,255))
        text_c(d, "Answer", int(H*0.40)+185, 44, CYAN)
    if p > 0.6:
        text_c(d, "ASK  ->  ANSWER", H*0.62, 60, YELLOW, border=4)

def scene_agent(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "AI AGENT", H*0.28, 70, CYAN)
    round_rect(d, (140, int(H*0.38), 940, int(H*0.38)+130), 30, (25,40,75,255), outline=BLUE, ow=3)
    text_c(d, "GOAL", int(H*0.38)+45, 46, WHITE)
    cx = W//2; base_y = int(H*0.56)
    nodes = [(cx-300, base_y), (cx, base_y+60), (cx+300, base_y), (cx-150, base_y+220), (cx+150, base_y+220)]
    labels = ["Plan", "Tools", "Act", "Steps", "Done"]
    if p > 0.2:
        cnt = min(5, max(1, int(p*5)))
        for i in range(cnt):
            nx, ny = nodes[i]
            node(img, nx, ny, 46, BLUE if i%2==0 else CYAN, labels[i], 26)
    if p > 0.6:
        text_c(d, "GOAL  ->  ACTION", H*0.78, 62, YELLOW, border=4)

def scene_workflow(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "HOW IT WORKS", H*0.20, 62, WHITE)
    labels = ["GOAL", "STEPS", "TOOLS", "DONE"]
    ys = [H*0.36, H*0.48, H*0.60, H*0.72]
    cols = [CYAN, BLUE, BLUE, YELLOW]
    shown = min(4, int(p*4)+1)
    pts = []
    for i in range(shown):
        y = ys[i]; x = W//2
        node(img, x, int(y), 62, cols[i], labels[i], 30)
        pts.append((x, int(y)+62))
    if len(pts) > 1:
        d2 = ImageDraw.Draw(img)
        for k in range(1, len(pts)):
            line(d2, pts[k-1], pts[k], CYAN, 8)

def scene_example(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "REAL EXAMPLE", H*0.14, 56, WHITE)
    text_c(d, "Find customers + build report", H*0.22, 44, GREY)
    cards = ["Research", "Collect data", "Organize", "Analyze", "Report"]
    for i,c in enumerate(cards):
        local = p*5 - i
        if local <= 0: continue
        y = int(H*0.34 + i*0.10*H)
        col = (30,64,120,255) if i<4 else (250,204,21,255)
        round_rect(d, (180, y, 900, y+120), 24, col)
        text_c(d, c, y+42, 42, WHITE)

def scene_approval(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "HUMAN APPROVAL", H*0.30, 74, YELLOW, border=5)
    if p > 0.2:
        round_rect(d, (200, int(H*0.44), 880, int(H*0.62)), 30, (25,40,75,255), outline=WHITE, ow=2)
        text_c(d, "Allow agent to send?", int(H*0.47), 44, WHITE)
    if p > 0.5:
        round_rect(d, (560, int(H*0.64), 860, int(H*0.64)+110), 30, (22,160,90,255))
        text_c(d, "APPROVE", int(H*0.64)+36, 44, WHITE)
    if p > 0.75:
        glow_circle(img, 300, int(H*0.70), 40, (34,211,238))
        d2 = ImageDraw.Draw(img)
        d2.ellipse([280, int(H*0.70)-25, 320, int(H*0.70)+25], fill=(34,211,238,255))
        d2.line([(288,int(H*0.70)),(302,int(H*0.70)+14),(322,int(H*0.70)-12)], fill=(10,14,26,255), width=6)

def scene_team(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "HUMANS + AI AGENTS", H*0.18, 60, CYAN)
    cx, cy = W//2, int(H*0.52)
    glow_circle(img, cx, cy, 55, (245,248,255))
    d2 = ImageDraw.Draw(img)
    d2.ellipse([cx-55, cy-55, cx+55, cy+55], fill=(245,248,255,255))
    d2.ellipse([cx-20, cy-20, cx+20, cy+20], fill=(30,64,120,255))
    labels = ["Research", "Sales", "Code", "Data", "Ops"]
    for i in range(5):
        ang = p*2*math.pi + i*2*math.pi/5
        rr = 330
        nx = cx + rr*math.cos(ang); ny = cy + rr*math.sin(ang)
        node(img, int(nx), int(ny), 40, CYAN if i%2==0 else BLUE)
        d3 = ImageDraw.Draw(img)
        f = font(26); tw = d3.textlength(labels[i], font=f)
        d3.text((nx-tw/2, ny-60), labels[i], font=f, fill=WHITE, stroke_width=2, stroke_fill=(0,0,0,255))
        line(d3, (cx, cy), (int(nx), int(ny)), (60,80,120,255), 3)

def scene_cta(img, p):
    d = ImageDraw.Draw(img); bg(img)
    text_c(d, "HUMANS WHO USE", H*0.38, 66, WHITE)
    text_c(d, "AI AGENTS WIN", H*0.46, 74, CYAN, border=5)
    if p > 0.6:
        text_c(d, "FOLLOW", H*0.62, 80, YELLOW, border=6)

SCENES = [
    ("hook", 5.0, scene_hook),
    ("chatbot", 6.0, scene_chatbot),
    ("agent", 7.0, scene_agent),
    ("workflow", 8.0, scene_workflow),
    ("example", 7.0, scene_example),
    ("approval", 6.0, scene_approval),
    ("team", 8.0, scene_team),
    ("cta", 12.0, scene_cta),
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
    render_all("/tmp/tkframes")
