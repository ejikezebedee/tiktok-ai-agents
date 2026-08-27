#!/usr/bin/env python3
"""Third TikTok on Movis — 'Practical AI Examples You Can Use Today'.
Per-scene compositions, rendered then concatenated + muxed with voiceover."""
import os
import movis as mv
from movis.enum import Easing

W, H = 1080, 1920
FPS = 30
FONT_B = "/tmp/fonts/Inter-Bold.ttf"
FONT_SB = "/tmp/fonts/Inter-SemiBold.ttf"
FONT_R = "/tmp/fonts/Inter-Regular.ttf"

BG = '#0a0e1a'
CYAN = '#22d3ee'
BLUE = '#3b82f6'
WHITE = '#f5f8ff'
YELLOW = '#fac81a'
GREY = '#94a3b8'
GREEN = '#22c55e'
OUTLINE = '#05070f'

os.makedirs('/tmp/scenes', exist_ok=True)

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

# ============ SCENES (local time) ============

def scene_hook(dur):
    s = new_scene(dur)
    add_text(s, "PRACTICAL AI", 96, CYAN, W//2, int(H*0.40), 0.05, dur-0.05)
    add_text(s, "what it can do TODAY", 52, WHITE, W//2, int(H*0.52), 0.5, dur-0.5, font=FONT_SB)
    return s

def scene_notes(dur):
    s = new_scene(dur)
    add_text(s, "MESSY NOTES", 76, CYAN, W//2, int(H*0.20), 0.0, dur)
    labels = ["SUMMARY", "TASKS", "EMAIL", "PLAN"]
    for i, L in enumerate(labels):
        t0 = 0.4 + i*1.2
        add_chip(s, L, W//2, int(H*0.42) + i*230, t0, dur-t0, color=BLUE, tcolor=WHITE, w=520, h=150, size=44)
        if i > 0:
            add_arrow(s, "\u2193", W//2, int(H*0.42) + i*230 - 170, t0-0.05)
    return s

def scene_docs(dur):
    s = new_scene(dur)
    add_text(s, "SUMMARIZE", 88, CYAN, W//2, int(H*0.32), 0.0, dur)
    add_chip(s, "50-page document", W//2, int(H*0.48), 0.6, dur-0.6, color='#1e3a5f', tcolor=WHITE, w=620, h=130, size=40)
    add_text(s, "VERIFY IMPORTANT INFO", 52, YELLOW, W//2, int(H*0.68), 2.2, dur-2.2, font=FONT_SB)
    return s

def scene_writing(dur):
    s = new_scene(dur)
    add_chip(s, "ROUGH IDEA", W//2, int(H*0.32), 0.0, dur, color=BLUE, tcolor=WHITE, w=520, h=150, size=42)
    add_arrow(s, "\u2193", W//2, int(H*0.47), 1.2)
    add_chip(s, "PROFESSIONAL MESSAGE", W//2, int(H*0.58), 1.8, dur-1.8, color=GREEN, tcolor='#052014', w=700, h=150, size=40)
    return s

def scene_data(dur):
    s = new_scene(dur)
    add_text(s, "ANALYZE", 88, CYAN, W//2, int(H*0.28), 0.0, dur)
    for i, (label, val) in enumerate([("Revenue", 0.8), ("Expenses", 0.5), ("Best-sellers", 0.7)]):
        t0 = 0.5 + i*1.1
        y = int(H*0.44) + i*200
        # bar track + fill
        s.add_layer(mv.layer.Rectangle(size=(700, 60), color='#1e3a5f'), position=(W//2, y), offset=t0, end_time=dur)
        fw = int(700*val)
        s.add_layer(mv.layer.Rectangle(size=(fw, 60), color=CYAN if i==0 else BLUE), position=(W//2 - (700-fw)/2, y), offset=t0, end_time=dur)
        add_text(s, label, 36, WHITE, W//2, y-80, t0, dur, font=FONT_SB, outline=0, scale_in=False)
    add_chip(s, "Sales +18% this month", W//2, int(H*0.85), 3.8, dur-3.8, color=GREEN, tcolor='#052014', w=700, h=130, size=44)
    return s

def scene_research(dur):
    s = new_scene(dur)
    add_text(s, "RESEARCH", 84, CYAN, W//2, int(H*0.18), 0.0, dur)
    steps = ["SEARCH", "COMPARE", "ORGANIZE", "REPORT"]
    for i, st in enumerate(steps):
        t0 = 0.4 + i*1.2
        add_chip(s, st, W//2, int(H*0.34) + i*190, t0, dur-t0, color=BLUE if i<3 else GREEN, tcolor=WHITE if i<3 else '#052014', w=500, h=120, size=42)
        if i > 0:
            add_arrow(s, "\u2193", W//2, int(H*0.34) + i*190 - 145, t0-0.05)
    return s

def scene_images(dur):
    s = new_scene(dur)
    add_text(s, "UNDERSTAND IMAGES", 74, CYAN, W//2, int(H*0.34), 0.0, dur)
    for i, L in enumerate(["product photo", "screenshot", "diagram"]):
        t0 = 0.6 + i*1.3
        add_chip(s, L, W//2, int(H*0.52) + i*190, t0, dur-t0, color='#1e3a5f', tcolor=WHITE, w=520, h=120, size=38)
    return s

def scene_learn(dur):
    s = new_scene(dur)
    add_text(s, "LEARN", 88, CYAN, W//2, int(H*0.22), 0.0, dur)
    for i, L in enumerate(["BEGINNER", "INTERMEDIATE", "ADVANCED"]):
        t0 = 0.5 + i*1.4
        add_chip(s, L, W//2, int(H*0.40) + i*190, t0, dur-t0, color=[BLUE, CYAN, GREEN][i], tcolor=['#0a0e1a', '#0a0e1a', '#052014'][i], w=520, h=120, size=42)
        if i > 0:
            add_arrow(s, "\u2193", W//2, int(H*0.40) + i*190 - 145, t0-0.05)
    return s

def scene_automate(dur):
    s = new_scene(dur)
    add_text(s, "AUTOMATE", 84, CYAN, W//2, int(H*0.16), 0.0, dur)
    tools = ["Email", "Calendar", "CRM", "Docs"]
    xs = [W//2-320, W//2+320, W//2-320, W//2+320]
    ys = [int(H*0.34), int(H*0.34), int(H*0.50), int(H*0.50)]
    for i, T in enumerate(tools):
        add_chip(s, T, xs[i], ys[i], 0.4+i*0.5, dur, color='#1e3a5f', tcolor=WHITE, w=330, h=130, size=38)
    add_chip(s, "HUMAN REVIEW", W//2, int(H*0.70), 3.0, dur-3.0, color=YELLOW, tcolor='#1a1400', w=600, h=140, size=48)
    return s

def scene_cta(dur):
    s = new_scene(dur)
    add_text(s, "SAVE TIME", 92, CYAN, W//2, int(H*0.36), 0.0, dur)
    add_text(s, "start with one task", 50, WHITE, W//2, int(H*0.48), 1.0, dur-1.0, font=FONT_SB)
    add_text(s, "FOLLOW", 84, YELLOW, W//2, int(H*0.62), 2.2, dur-2.2)
    return s

SCENES = [
    ("00_hook", 2.0, scene_hook),
    ("01_notes", 6.0, scene_notes),
    ("02_docs", 6.0, scene_docs),
    ("03_writing", 6.0, scene_writing),
    ("04_data", 6.0, scene_data),
    ("05_research", 6.0, scene_research),
    ("06_images", 5.0, scene_images),
    ("07_learn", 5.0, scene_learn),
    ("08_automate", 6.0, scene_automate),
    ("09_cta", 5.8, scene_cta),
]

def main():
    for name, dur, fn in SCENES:
        s = fn(dur)
        s.write_video(f'/tmp/scenes/{name}.mp4', fps=FPS, codec='libx264')
        print('rendered', name, dur, flush=True)

if __name__ == '__main__':
    main()
