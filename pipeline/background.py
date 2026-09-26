import cv2
import numpy as np
import random

def generate_background(width=1150, height=620, style=None):
    if style is None:
        style = random.choice(['vibrant_ancient', 'classical_aged', 'palm_leaf', 'tea_patina'])

    if style == 'palm_leaf':
        r_base = random.randint(215, 230)
        g_base = random.randint(175, 192)
        b_base = random.randint(120, 140)
    elif style == 'vibrant_ancient':
        r_base = random.randint(238, 246)
        g_base = random.randint(192, 206)
        b_base = random.randint(132, 148)
    elif style == 'tea_patina':
        r_base = random.randint(232, 242)
        g_base = random.randint(210, 222)
        b_base = random.randint(168, 182)
    else:
        r_base = random.randint(236, 245)
        g_base = random.randint(218, 228)
        b_base = random.randint(182, 195)

    bg = np.zeros((height, width, 3), dtype=np.float32)
    bg[:, :, 0] = r_base
    bg[:, :, 1] = g_base
    bg[:, :, 2] = b_base

    cloud = cv2.resize(np.random.normal(0, 3.5, (height // 24, width // 24, 1)).astype(np.float32),
                       (width, height), interpolation=cv2.INTER_CUBIC)[:, :, np.newaxis]
    grain = np.random.normal(0, 1.8, (height, width, 1)).astype(np.float32)
    bg += (cloud + grain)

    if style == 'palm_leaf':
        fibers = cv2.resize(np.random.normal(0, 6.0, (height, width // 4, 1)).astype(np.float32),
                            (width, height), interpolation=cv2.INTER_LINEAR)[:, :, np.newaxis]
        bg += fibers

    Y, X = np.ogrid[:height, :width]
    norm_x = (X - width / 2.0) / (width / 2.0)
    norm_y = (Y - height / 2.0) / (height / 2.0)
    dist = (norm_x**2 * 1.05 + norm_y**2 * 0.95).astype(np.float32)
    vignette = np.clip(1.0 - (dist * random.uniform(0.16, 0.25)), 0.64, 1.0)[:, :, np.newaxis]

    bg[:, :, 0] *= vignette[:, :, 0]
    bg[:, :, 1] *= (vignette[:, :, 0] * 0.95)
    bg[:, :, 2] *= (vignette[:, :, 0] * 0.86)

    num_dark_spots = random.randint(15, 30)
    for _ in range(num_dark_spots):
        sx = random.randint(15, width - 15)
        sy = random.randint(15, height - 15)
        sr = random.randint(1, 4)
        spot_col = np.array([random.randint(45, 75), random.randint(35, 55), random.randint(25, 40)], dtype=np.float32)
        cv2.circle(bg, (sx, sy), sr, spot_col.tolist(), -1)
        if sr > 2:
            cv2.circle(bg, (sx, sy), sr + 1, (spot_col * 1.3).tolist(), 1)

    if random.random() > 0.3:
        crease_x = width - random.randint(180, 230) if random.random() > 0.4 else random.randint(int(width * 0.35), int(width * 0.65))
        for y in range(height):
            cx = int(crease_x + np.sin(y / 45.0) * 2)
            if 2 <= cx < width - 2:
                bg[y, cx-2:cx, :] *= 0.92
                bg[y, cx:cx+2, :] *= 1.05

    if style != 'palm_leaf' and random.random() < 0.85:
        rule_x1 = int(width * 0.865)
        rule_x2 = int(width * 0.878)
        rule_color = (random.randint(176, 196), random.randint(50, 68), random.randint(40, 56))

        for y in range(int(height * 0.04), int(height * 0.96)):
            dx1 = int(np.sin(y / 45.0) * 1)
            dx2 = int(np.sin(y / 50.0) * 1)
            a1 = random.uniform(0.72, 0.90)
            a2 = random.uniform(0.70, 0.88)
            if 0 <= rule_x1 + dx1 < width:
                bg[y, rule_x1 + dx1, :] = bg[y, rule_x1 + dx1, :] * (1.0 - a1) + np.array(rule_color) * a1
            if 0 <= rule_x2 + dx2 < width:
                bg[y, rule_x2 + dx2, :] = bg[y, rule_x2 + dx2, :] * (1.0 - a2) + np.array(rule_color) * a2

    if random.random() < 0.85:
        hole_x = int(width * 0.97)
        num_holes = 5
        hole_ys = np.linspace(int(height * 0.16), int(height * 0.84), num_holes).astype(int)
        for hy in hole_ys:
            hx = hole_x + random.randint(-1, 1)
            cv2.circle(bg, (hx, hy), 3, (40, 30, 22), -1)
            cv2.circle(bg, (hx, hy), 5, (95, 76, 52), 1)
            cv2.circle(bg, (hx, hy), 7, (145, 118, 85), 1)

    border_noise = cv2.GaussianBlur(np.random.normal(0, 0.8, (height, width)).astype(np.float32), (5, 5), 0)
    cut = 5
    mask = np.ones((height, width), dtype=np.float32)
    for x in range(width):
        tc = max(1, int(cut + border_noise[0, x] * 2.0))
        bc = max(1, int(cut + border_noise[-1, x] * 2.0))
        mask[:tc, x] *= np.linspace(0.5, 0.98, tc)
        mask[-bc:, x] *= np.linspace(0.98, 0.5, bc)
    for y in range(height):
        lc = max(1, int(cut + border_noise[y, 0] * 2.0))
        rc = max(1, int(cut + border_noise[y, -1] * 2.0))
        mask[y, :lc] *= np.linspace(0.5, 0.98, lc)
        mask[y, -rc:] *= np.linspace(0.98, 0.5, rc)

    bg *= mask[:, :, np.newaxis]
    return np.clip(bg, 0, 255).astype(np.uint8)
