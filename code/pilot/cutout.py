"""Cut a character off a plain light background (flood fill from the border), save RGBA PNG(s).
python3 cutout.py in.png out_prefix [n_columns]  -> splits a pose sheet into n columns, each trimmed."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
def cut(im, tol=26):
    a = np.asarray(im.convert('RGB')).astype(int); h, w, _ = a.shape
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bgc = np.median(border, axis=0)
    near = np.abs(a - bgc).sum(-1) < tol*3
    lab, _ = ndimage.label(near)
    ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bgmask = np.isin(lab, list(ids))
    alpha = (~bgmask).astype(np.uint8)*255
    alpha = ndimage.binary_opening(alpha > 0, iterations=1).astype(np.uint8)*255
    alpha = np.asarray(Image.fromarray(alpha).filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(1.0)))
    rgba = np.dstack([np.asarray(im.convert('RGB')), alpha]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')
def keep_main(im, frac=0.05):
    a = np.asarray(im).copy(); lab, n = ndimage.label(a[..., 3] > 30)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n+1)); big = sizes.max()
        drop = [i+1 for i, sz in enumerate(sizes) if sz < big*frac]
        a[np.isin(lab, drop), 3] = 0
    return Image.fromarray(a, 'RGBA')
def trim(im, pad=12):
    im = keep_main(im)
    bb = im.getchannel('A').point(lambda v: 255 if v > 30 else 0).getbbox()
    x0, y0, x1, y1 = bb; return im.crop((max(0, x0-pad), max(0, y0-pad), min(im.width, x1+pad), min(im.height, y1+pad)))
if __name__ == '__main__':
    im = Image.open(sys.argv[1]); out = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    full = cut(im)
    if n == 1:
        trim(full).save(out+'.png'); print(out+'.png')
    else:
        # split at the emptiest columns near each 1/n boundary
        col = np.asarray(full.getchannel('A')).astype(int).sum(0); W = full.width; cuts = [0]
        for k in range(1, n):
            c0 = int(W*k/n); lo, hi = c0-W//8, c0+W//8
            cuts.append(lo + int(np.argmin(col[lo:hi])))
        cuts.append(W)
        for k in range(n):
            p = trim(full.crop((cuts[k], 0, cuts[k+1], full.height))); p.save(f'{out}_{k}.png'); print(f'{out}_{k}.png', p.size)
