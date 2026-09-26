import os
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = {
    'devanagari': ['fonts/devanagari_kalam.ttf'],
    'modi': ['fonts/modi_noto.ttf'],
    'sharada': ['fonts/sharada_noto.ttf']
}

def get_font(script, size=28):
    path = random.choice(FONTS.get(script, FONTS['devanagari']))
    return ImageFont.truetype(path, size)

def render_folio(bg_img, lines, script='devanagari'):
    h, w, _ = bg_img.shape

    margin_x = int(w * 0.09)
    margin_y = int(h * 0.13)
    max_w = int(w * 0.74)
    max_h = int(h * 0.74)

    font_size = random.randint(28, 30) if script == 'devanagari' else random.randint(26, 28)
    font = get_font(script, font_size)

    line_spacing = int(font_size * 1.70)
    target_lines = 7

    rendered_lines = []
    ground_truth = []

    for raw in lines:
        words = raw.strip().split()
        if not words:
            continue
        curr = []
        for word in words:
            test_line = " ".join(curr + [word])
            bbox = font.getbbox(test_line)
            if (bbox[2] - bbox[0]) <= max_w:
                curr.append(word)
            else:
                if curr:
                    rendered_lines.append(curr)
                    if len(rendered_lines) >= target_lines:
                        break
                curr = [word]
        if len(rendered_lines) >= target_lines:
            break
        if curr:
            rendered_lines.append(curr)
            if len(rendered_lines) >= target_lines:
                break

    rendered_lines = rendered_lines[:target_lines]

    canvas = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    base_ink = (32, 28, 24)
    rubric_ink = (196, 56, 38)

    y = margin_y
    for line_words in rendered_lines:
        x = margin_x + random.randint(-4, 4)
        ground_truth.append(" ".join(line_words))

        freq = random.uniform(0.012, 0.024)
        phase = random.uniform(0, np.pi * 2)
        amp = random.uniform(1.8, 3.2)

        dip_step = 0
        flow = 1.0

        for word in line_words:
            if dip_step >= random.randint(3, 5):
                flow = random.uniform(0.96, 1.0)
                dip_step = 0
            else:
                flow *= random.uniform(0.92, 0.96)
                dip_step += 1

            is_rubric = (('।' in word or '॥' in word) and random.random() < 0.45) or (random.random() < 0.18)
            color = rubric_ink if is_rubric else base_ink

            alpha = int(255 * np.clip(flow + random.uniform(-0.06, 0.06), 0.70, 1.0))
            if flow < 0.82:
                adj_color = tuple(min(255, int(c * 1.15)) for c in color)
            else:
                adj_color = tuple(max(0, int(c * 0.90)) for c in color)

            dy = int(np.sin(x * freq + phase) * amp + random.uniform(-1.5, 1.5))
            draw.text((x, y + dy), word + " ", font=font, fill=adj_color + (alpha,))

            bbox = font.getbbox(word + " ")
            x += (bbox[2] - bbox[0])

        y += line_spacing

    rgba = np.array(canvas, dtype=np.uint8)
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0

    shear = random.uniform(-0.10, -0.13) if script == 'devanagari' else random.uniform(-0.06, -0.09)
    M = np.float32([[1, shear, 0], [0, 1, 0]])
    rgb = cv2.warpAffine(rgb, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    alpha = cv2.warpAffine(alpha, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    pmap = cv2.resize(np.random.uniform(0.85, 1.15, (h // 8, w // 8)).astype(np.float32), (w, h), interpolation=cv2.INTER_LINEAR)
    alpha = np.clip(alpha * pmap, 0, 1.0)
    alpha *= (np.random.random((h, w)) > 0.008).astype(np.float32)

    bg_f = bg_img.astype(np.float32) / 255.0
    fg_f = rgb.astype(np.float32) / 255.0
    a = alpha[:, :, np.newaxis]

    out = bg_f * (1.0 - a) + (bg_f * fg_f * 1.15) * a
    return np.clip(out * 255.0, 0, 255).astype(np.uint8), "\n".join(ground_truth)
