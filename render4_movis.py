#!/usr/bin/env python3
"""Fourth TikTok on Movis — 'Stop Doing These Tasks Yourself' (Emeka's own examples)."""
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

os.makedirs('/tmp/scenes4', exist_ok=True)

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
    add_text(s, "STOP DOING IT", 86, CYAN, W//2, int(H*0.38), 0.05, dur-0.05)
    add_text(s, "YOURSELF", 96, WHITE, W//2, int(H*0.48), 0.4, dur-0.4)
    return s

def scene_email(dur):
    s = new_scene(dur)
    add_text(s, "READ + DRAFT EMAILS", 64, CYAN, W//2, int(H*0.18), 0.0, dur)
    add_chip(s, "INBOX", W//2, int(H*0.36), 0.4, dur, color=BLUE, tcolor=WHITE, w=520, h=140, size=46)
    add_arrow(s, "\u2193", W//2, int(H*0.50), 1.4)
    add_chip(s, "DRAFT REPLY", W//2, int(H*0.58), 1.8, dur, color=BLUE, tcolor=WHITE, w=520, h=140, size=46)
    add_arrow(s, "\u2193", W//2, int(H*0.72), 2.8)
    add_chip(s, "YOU APPROVE", W//2, int(H*0.80), 3.2, dur, color=YELLOW, tcolor='#1a1400', w=520, h=140, size=46)
    return s

def scene_notes(dur):
    s = new_scene(dur)
    add_text(s, "VOICE NOTE", 74, CYAN, W//2, int(H*0.22), 0.0, dur)
    add_arrow(s, "\u2193", W//2, int(H*0.36), 1.2)
    add_chip(s, "TASK LIST", W//2, int(H*0.46), 1.6, dur, color=GREEN, tcolor='#052014', w=560, h=150, size=48)
    for i, L in enumerate(["1. Call supplier", "2. Send quote", "3. Book meeting"]):
        t0 = 2.4 + i*1.0
        add_chip(s, L, W//2, int(H*0.66) + i*140, t0, dur-t0, color='#1e3a5f', tcolor=WHITE, w=680, h=110, size=38)
    return s

def scene_leads(dur):
    s = new_scene(dur)
    add_text(s, "FIND LEADS", 84, CYAN, W//2, int(H*0.18), 0.0, dur)
    rows = [("Alpha Ltd", "Logistics", "High"), ("Beta GmbH", "Retail", "Med"), ("Gamma Co", "Finance", "High")]
    for i, (c, ind, pri) in enumerate(rows):
        t0 = 0.5 + i*1.6
        y = int(H*0.34) + i*300
        add_chip(s, c, W//2, y, t0, dur, color='#1e3a5f', tcolor=WHITE, w=760, h=120, size=40)
        add_text(s, ind + "  ·  " + pri, 32, YELLOW, W//2, y+90, t0, dur, font=FONT_SB, outline=0, scale_in=False)
    return s

def scene_invoices(dur):
    s = new_scene(dur)
    add_text(s, "CHASE INVOICES", 76, CYAN, W//2, int(H*0.20), 0.0, dur)
    for i, L in enumerate(["INV #104  ·  paid", "INV #107  ·  due", "INV #109  ·  OVERDUE"]):
        t0 = 0.5 + i*1.4
        col = GREEN if i==0 else ('#1e3a5f' if i==1 else YELLOW)
        tcol = '#052014' if i in (0,2) else WHITE
        add_chip(s, L, W//2, int(H*0.38) + i*260, t0, dur, color=col, tcolor=tcol, w=760, h=130, size=40)
    return s

def scene_proposals(dur):
    s = new_scene(dur)
    add_chip(s, "ROUGH IDEA", W//2, int(H*0.30), 0.0, dur, color=BLUE, tcolor=WHITE, w=540, h=150, size=44)
    add_arrow(s, "\u2193", W//2, int(H*0.45), 1.3)
    add_chip(s, "PROPOSAL", W//2, int(H*0.55), 1.9, dur, color=GREEN, tcolor='#052014', w=540, h=150, size=48)
    add_text(s, "or quote", 40, GREY, W//2, int(H*0.70), 2.6, dur, font=FONT_SB, outline=0, scale_in=False)
    return s

def scene_numbers(dur):
    s = new_scene(dur)
    add_text(s, "WEEKLY SUMMARY", 74, CYAN, W//2, int(H*0.18), 0.0, dur)
    for i, (label, val) in enumerate([("Sales", 0.8), ("Expenses", 0.5), ("Profit", 0.6)]):
        t0 = 0.5 + i*1.3
        y = int(H*0.36) + i*240
        s.add_layer(mv.layer.Rectangle(size=(700, 60), color='#1e3a5f'), position=(W//2, y), offset=t0, end_time=dur)
        fw = int(700*val)
        s.add_layer(mv.layer.Rectangle(size=(fw, 60), color=CYAN if i==0 else (YELLOW if i==1 else GREEN)), position=(W//2-(700-fw)//2, y), offset=t0, end_time=dur)
        add_text(s, label, 38, WHITE, W//2, y-85, t0, dur, font=FONT_SB, outline=0, scale_in=False)
    return s

def scene_content(dur):
    s = new_scene(dur)
    add_text(s, "ONE POST", 76, CYAN, W//2, int(H*0.16), 0.0, dur)
    add_arrow(s, "\u2193", W//2, int(H*0.30), 1.0)
    for i, L in enumerate(["EMAIL", "SOCIAL", "SCRIPT"]):
        t0 = 1.4 + i*1.4
        add_chip(s, L, W//2, int(H*0.40) + i*200, t0, dur, color=BLUE, tcolor=WHITE, w=520, h=130, size=44)
    return s

def scene_cta(dur):
    s = new_scene(dur)
    add_text(s, "APPROVE + AUTOMATE", 70, CYAN, W//2, int(H*0.34), 0.0, dur)
    add_text(s, "keep the important parts", 44, WHITE, W//2, int(H*0.46), 1.2, dur-1.2, font=FONT_SB)
    add_text(s, "FOLLOW", 84, YELLOW, W//2, int(H*0.60), 2.6, dur-2.6)
    return s

SCENES = [
    ("00_hook", 2.0, scene_hook),
    ("01_email", 6.0, scene_email),
    ("02_notes", 6.0, scene_notes),
    ("03_leads", 6.0, scene_leads),
    ("04_invoices", 6.0, scene_invoices),
    ("05_proposals", 6.0, scene_proposals),
    ("06_numbers", 6.0, scene_numbers),
    ("07_content", 6.0, scene_content),
    ("08_cta", 6.0, scene_cta),
]

def main():
    for name, dur, fn in SCENES:
        s = fn(dur)
        s.write_video(f'/tmp/scenes4/{name}.mp4', fps=FPS, codec='libx264')
        print('rendered', name, dur, flush=True)

if __name__ == '__main__':
    main()
