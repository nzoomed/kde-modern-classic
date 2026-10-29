#!/usr/bin/env python3
"""Retrace shapes from a KDE Classic original PNG into smooth SVG paths (64-unit canvas).

The shapes are found by flood-filling from seed pixels over pixels that pass a test, enlarged with
xBRZ (keeps pixel-art corners crisp), smoothed lightly, contoured, simplified and written as
Catmull-Rom curves. Used for lettering and silhouettes that should follow the original exactly.
"""
import sys, os


def _deps():
    """Tracing needs numpy, Pillow, scikit-image and the xBRZ upscaler (tools/upscale.py, which loads
    tools/xbrz/libxbrz.so). They are imported only when tracing, so building the theme (which just uses
    catmull() below) needs none of them."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
    global np, Image, ImageFilter, measure, xbrz_scale
    import numpy as np
    from PIL import Image, ImageFilter
    from skimage import measure
    from upscale import xbrz_scale


def flood(im, seeds, ok, box=None):
    _deps()
    w, h = im.size
    px = im.load()
    x0, y0, x1, y1 = box or (0, 0, w, h)
    m = np.zeros((h, w), bool)
    st = list(seeds)
    while st:
        x, y = st.pop()
        if not (x0 <= x < x1 and y0 <= y < y1) or m[y, x] or not ok(px[x, y]):
            continue
        m[y, x] = True
        st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return m


def mask_to_path(m, src_px=48, up=6, blur=1.6, tol=0.9, grow=0.0, min_area=4.0, dilate=0):
    """Binary mask (src_px square) -> SVG path string in 64-unit coordinates."""
    _deps()
    h, w = m.shape
    img = Image.fromarray((m * 255).astype("uint8")).convert("RGBA")
    img.putalpha(img.getchannel("R"))
    big = xbrz_scale(img, up).getchannel("A")
    if dilate:
        big = big.filter(ImageFilter.MaxFilter(2 * dilate + 1))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(big, float) / 255
    a = np.pad(a, 2)
    level = 0.5 - grow
    k = 64.0 / (src_px * up)
    out = []
    for c in measure.find_contours(a, level):
        c = measure.approximate_polygon(c, tol)
        pts = [((x - 2) * k, (y - 2) * k) for y, x in c[:-1]]
        if len(pts) < 3:
            continue
        area = 0.5 * abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts))))
        if area < min_area:
            continue
        out.append(catmull(pts))
    return " ".join(out)


def catmull(p, t=0.5):
    n = len(p)
    s = f"M{p[0][0]:.2f},{p[0][1]:.2f}"
    for i in range(n):
        p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % n], p[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        s += f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}"
    return s + "Z"


def smooth_outline(m, src_px=32, up=6, blur=3.0, corner_deg=55, sigma=3.0, step=1.6, min_area=6.0):
    """Like mask_to_path, but redraws each outline with smooth curves: the contour is resampled evenly,
    sharp corners (turning more than corner_deg) are kept as real corners, and every stretch between
    corners is smoothed (Gaussian along the outline) and written as Catmull-Rom curves. Good for organic
    shapes such as KDE Classic's curling arrows, where a straight trace looks lumpy."""
    _deps()
    import numpy as np
    from scipy.ndimage import gaussian_filter1d
    h, w = m.shape
    img = Image.fromarray((m * 255).astype("uint8")).convert("RGBA")
    img.putalpha(img.getchannel("R"))
    big = xbrz_scale(img, up).getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    a = np.pad(np.asarray(big, float) / 255, 2)
    k = 64.0 / (src_px * up)
    out = []
    for c in measure.find_contours(a, 0.5):
        pts = np.array([((x - 2) * k, (y - 2) * k) for y, x in c[:-1]])
        if len(pts) < 8:
            continue
        # resample evenly along the closed outline
        seg = np.r_[np.hypot(*np.diff(np.vstack([pts, pts[:1]]), axis=0).T)]
        s = np.r_[0, np.cumsum(seg)]
        L = s[-1]
        n = max(12, int(L / step))
        t = np.linspace(0, L, n, endpoint=False)
        closed = np.vstack([pts, pts[:1]])
        P = np.c_[np.interp(t, s, closed[:, 0]), np.interp(t, s, closed[:, 1])]
        area = 0.5 * abs(np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1]))
        if area < min_area:
            continue
        # light smoothing to find true corners (ignore pixel stair-steps)
        Q = np.c_[gaussian_filter1d(P[:, 0], 1.5, mode="wrap"), gaussian_filter1d(P[:, 1], 1.5, mode="wrap")]
        span = 3
        v1 = Q - np.roll(Q, span, axis=0)
        v2 = np.roll(Q, -span, axis=0) - Q
        ang = np.degrees(np.abs(np.arctan2(v1[:, 0] * v2[:, 1] - v1[:, 1] * v2[:, 0], (v1 * v2).sum(1))))
        corners = [i for i in range(n) if ang[i] > corner_deg and ang[i] >= ang[(i - 1) % n] and ang[i] >= ang[(i + 1) % n]]
        if not corners:
            S = np.c_[gaussian_filter1d(P[:, 0], sigma, mode="wrap"), gaussian_filter1d(P[:, 1], sigma, mode="wrap")]
            out.append(catmull([tuple(p) for p in S[::2]]))
            continue
        d = ""
        for ci, c0 in enumerate(corners):
            c1 = corners[(ci + 1) % len(corners)]
            idx = [(c0 + j) % n for j in range(((c1 - c0) % n) + 1)]
            run = P[idx]
            if len(run) > 4:
                sm = np.c_[gaussian_filter1d(run[:, 0], sigma, mode="nearest"), gaussian_filter1d(run[:, 1], sigma, mode="nearest")]
                sm[0], sm[-1] = run[0], run[-1]
                # keep the ends pinned while easing the smoothing in
                for j in range(1, min(4, len(sm) - 1)):
                    f = j / 4
                    sm[j] = run[j] * (1 - f) + sm[j] * f
                    sm[-1 - j] = run[-1 - j] * (1 - f) + sm[-1 - j] * f
            else:
                sm = run
            pts_run = [tuple(p) for p in sm[::2]] + ([tuple(sm[-1])] if (len(sm) - 1) % 2 else [])
            if not d:
                d = f"M{pts_run[0][0]:.2f},{pts_run[0][1]:.2f}"
            q = pts_run
            for i in range(len(q) - 1):
                p0 = q[i - 1] if i > 0 else q[i]
                p1, p2 = q[i], q[i + 1]
                p3 = q[i + 2] if i + 2 < len(q) else q[i + 1]
                c1x, c1y = p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6
                c2x, c2y = p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6
                d += f"C{c1x:.2f},{c1y:.2f} {c2x:.2f},{c2y:.2f} {p2[0]:.2f},{p2[1]:.2f}"
        out.append(d + "Z")
    return " ".join(out)
