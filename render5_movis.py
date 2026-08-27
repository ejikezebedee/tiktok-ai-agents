#!/usr/bin/env python3
"""Fifth TikTok on Movis — 'Build a Business With an AI Agent'."""
import os
import movis as mv
from movis.enum import Easing

W, H = 1080, 1920
FPS = 30
FONT_B = "/tmp/fonts/Inter-Bold.ttf"
FONT_SB = "/tmp/fonts/Inter-SemiBold.ttf"

BG = '#0a0e1a'
CYAN = '#22d3ee'
BLUE = '#3b82f6'
WHITE = '#f5f8ff'
YELLOW = '#fac81a'
GREY = '#94a3b8'
GREEN = '#22c55e'
OUTLINE = '#05070f'

os.makedirs('/tmp/scenes5', exist_ok=True)

def new_scene(dur):
    c = mv.layer.Composition(size=(W, H), duration=dur)
    c.add_layer(mv.layer.Rectangle(c.size, color=BG))
    return c

def add_text(scene, text, size, color, x, y, t0, dur, font=FONT_B, outline=4, scale_in=True):
    layer = mv.layer.Text(
        text, font_size=size, font_family=font,
        contents=[mv.layer.FillProperty(color), mv.layer.StrokeProperty(OUTLINE, outline)]
    )
    item = scene.add_layer(layer, position=(x, y), offset=t0, end_time=t0+dur)
    item.opacity.enable_motion().append(0.0, 0.0, Easing.LINEAR).append(min(0.35, dur*0.5), 1.0, Easing.EASE_OUT)
    if scale_in:
        item.scale.enable_motion().append(0.0, 0.92).append(min(0.35, dur*0.5), 1.0, Easing.EASE_OUT)
    return item

def add_chip(scene, text, x, y, t0, dur, color=BLUE, tcolor=WHITE, w=460, h=110, size=40):
    scene.add_layer(mv.layer.Rectangle(size=(w, h), color=color), position=(x, y), offset=t0, end_time=t0+dur)
    add_text(scene, text, size, tcolor, x, y, t0, dur, font=FONT_SB, outline=0, scale_in=False)

def add_arrow(scene, ch, x, y, t0, color=GREY, size=52):
    add_text(scene, ch, size, color, x, y, t0, 0.01, font=FONT_B, outline=0, scale_in=False)

def scene_hook(dur):
    s = new_scene(dur)
    add_text(s, "BUILD WITHOUT", 78, CYAN, W//2, int(H*0.38), 0.05, dur-0.05)
    add_text(s, "A BIG TEAM", 88, WHITE, W//2, int(H*0.48), 0.4, dur-0.4)
    return s

def scene_market(dur):
    s = new_scene(dur)
    add_text(s, "RESEARCH + VALIDATE", 62, CYAN, W//2, int(H*0.18), 0.0, dur)
    for i, L in enumerate(["your market", "your idea", "your customers"]):
        t0 = 0.5 + i*1.6
        add_chip(s, L, W//2, int(H*0.36) + i*250, t0, dur, color=BLUE, tcolor=WHITE, w=620, h=140, size=44)
    return s

def scene_brand(dur):
    s = new_scene(dur)
    add_text(s, "BUILD YOUR BRAND", 70, CYAN, W//2, int(H*0.20), 0.0, dur)
    for i, L in enumerate(["Name", "Logo ideas", "First message"]):
        t0 = 0.5 + i*1.5
        add_chip(s, L, W//2, int(H*0.40) + i*240, t0, dur, color='#1e3a5f', tcolor=WHITE, w=620, h=140, size=44)
    return s

def scene_customers(dur):
    s = new_scene(dur)
    add_text(s, "HANDLE CUSTOMERS", 66, CYAN, W//2, int(H*0.16), 0.0, dur)
    add_chip(s, "ANSWER QUESTIONS", W//2, int(H*0.34), 0.4, dur, color=BLUE, tcolor=WHITE, w=620, h=150, size=42)
    add_arrow(s, "\u2193", W//2, int(H*0.50), 1.6)
    add_chip(s, "DRAFT REPLIES", W//2, int(H*0.58), 2.0, dur, color=BLUE, tcolor=WHITE, w=620, h=150, size=42)
    add_arrow(s, "\u2193", W//2, int(H*0.74), 3.2)
    add_chip(s, "YOU APPROVE", W//2, int(H*0.82), 3.6, dur, color=YELLOW, tcolor='#1a1400', w=620, h=150, size=46)
    return s

def scene_sell(dur):
    s = new_scene(dur)
    add_text(s, "FIND + SELL", 78, CYAN, W//2, int(H*0.16), 0.0, dur)
    for i, L in enumerate(["Find leads", "Write follow-ups", "Prepare proposals"]):
        t0 = 0.5 + i*1.6
        add_chip(s, L, W//2, int(H*0.36) + i*250, t0, dur, color=GREEN if i==2 else BLUE, tcolor='#052014' if i==2 else WHITE, w=680, h=150, size=42)
    return s

def scene_backoffice(dur):
    s = new_scene(dur)
    add_text(s, "RUN THE BACK OFFICE", 62, CYAN, W//2, int(H*0.18), 0.0, dur)
    for i, L in enumerate(["Invoices", "Expenses", "Weekly report"]):
        t0 = 0.5 + i*1.6
        add_chip(s, L, W//2, int(H*0.36) + i*250, t0, dur, color='#1e3a5f', tcolor=WHITE, w=620, h=140, size=44)
    return s

def scene_content(dur):
    s = new_scene(dur)
    add_text(s, "GROW CONTENT", 76, CYAN, W//2, int(H*0.16), 0.0, dur)
    add_chip(s, "ONE IDEA", W//2, int(H*0.34), 0.4, dur, color=BLUE, tcolor=WHITE, w=520, h=140, size=46)
    add_arrow(s, "\u2193", W//2, int(H*0.48), 1.6)
    for i, L in enumerate(["Posts", "Scripts", "Emails"]):
        t0 = 2.0 + i*1.3
        add_chip(s, L, W//2, int(H*0.56) + i*170, t0, dur, color='#1e3a5f', tcolor=WHITE, w=520, h=120, size=40)
    return s

def scene_coordinate(dur):
    s = new_scene(dur)
    add_text(s, "COORDINATE IT ALL", 68, CYAN, W//2, int(H*0.18), 0.0, dur)
    add_text(s, "one agent", 48, WHITE, W//2, int(H*0.36), 0.6, dur, font=FONT_SB)
    add_arrow(s, "\u2193", W//2, int(H*0.46), 1.4)
    for i, L in enumerate(["Research", "Brand", "Sales", "Reports"]):
        t0 = 1.8 + i*1.3
        add_chip(s, L, W//2, int(H*0.54) + i*170, t0, dur, color=BLUE, tcolor=WHITE, w=520, h=120, size=40)
    add_text(s, "you stay in charge", 40, YELLOW, W//2, int(H*0.80), 4.0, dur-4.0, font=FONT_SB)
    return s

def scene_cta(dur):
    s = new_scene(dur)
    add_text(s, "AUTOMATE", 88, CYAN, W//2, int(H*0.32), 0.0, dur)
    add_text(s, "one process at a time", 46, WHITE, W//2, int(H*0.44), 1.2, dur-1.2, font=FONT_SB)
    add_text(s, "FOLLOW", 84, YELLOW, W//2, int(H*0.58), 2.6, dur-2.6)
    return s

SCENES = [
    ("00_hook", 2.0, scene_hook),
    ("01_market", 6.0, scene_market),
    ("02_brand", 6.0, scene_brand),
    ("03_customers", 6.0, scene_customers),
    ("04_sell", 6.0, scene_sell),
    ("05_backoffice", 6.0, scene_backoffice),
    ("06_content", 6.0, scene_content),
    ("07_coordinate", 6.0, scene_coordinate),
    ("08_cta", 6.0, scene_cta),
]

def main():
    for name, dur, fn in SCENES:
        s = fn(dur)
        s.write_video(f'/tmp/scenes5/{name}.mp4', fps=FPS, codec='libx264')
        print('rendered', name, dur, flush=True)

if __name__ == '__main__':
    main()
