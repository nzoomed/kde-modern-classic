#!/usr/bin/env python3
"""Upscale bitmap icons with xBRZ (pixel-art edge-aware scaler).

Library use:  xbrz_scale(pil_rgba, factor) -> PIL image
             upscale_to(pil_rgba, target) -> PIL image of target x target
"""
import ctypes, os
import numpy as np
from PIL import Image

_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "xbrz", "libxbrz.so"))
_lib.xbrz_scale_defaults.argtypes = [ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
                                     ctypes.c_int, ctypes.c_int, ctypes.c_int]
RGBA = 2


def xbrz_scale(img, factor):
    img = img.convert("RGBA")
    w, h = img.size
    src = np.ascontiguousarray(np.asarray(img, dtype=np.uint8)).view(np.uint32).reshape(-1).copy()
    dst = np.zeros(w * h * factor * factor, dtype=np.uint32)
    _lib.xbrz_scale_defaults(factor, src.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),
                             dst.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)), w, h, RGBA)
    return Image.fromarray(dst.view(np.uint8).reshape(h * factor, w * factor, 4), "RGBA")


def _premult_resize(img, size):
    """Lanczos resize with premultiplied alpha (no dark fringes)."""
    a = np.asarray(img, dtype=np.float32) / 255
    a[..., :3] *= a[..., 3:4]
    chans = [Image.fromarray(a[..., i]).resize(size, Image.LANCZOS) for i in range(4)]
    out = np.stack([np.asarray(c) for c in chans], -1)
    al = np.clip(out[..., 3:4], 1e-6, 1)
    out[..., :3] = np.where(out[..., 3:4] > 1e-4, out[..., :3] / al, 0)
    return Image.fromarray((np.clip(out, 0, 1) * 255 + .5).astype(np.uint8), "RGBA")


def upscale_to(img, target, over=1.25):
    """xBRZ until at least target*over pixels, then downsample to target.
    Oversampling a little then shrinking softens xBRZ's stair-steps."""
    big = img
    while big.size[0] < target * over:
        need = target * over / big.size[0]
        f = next((k for k in range(2, 7) if k >= need), 6)
        big = xbrz_scale(big, f)
    return big if big.size[0] == target else _premult_resize(big, (target, target))
