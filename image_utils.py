import pathlib

import imageio as imageio
import numpy as np

import main


# proudly stolen from https://github.com/MrTeferi/mpc-scryfall/blob/master/scryfall_formatter.py
def add_bleed(img_path: pathlib.Path):
    im = imageio.v2.imread(img_path)

    # Scale between 0 and 255 for uint8
    minval = np.min(im)
    maxval = np.max(im)
    im_recon_sc = (255 * ((im - minval) / (maxval - minval))).astype(np.uint8)

    # Borderify image
    pad = 36  # Pad image by 1/8th of inch on each edge
    bordertol = 16  # Overfill onto existing border by 16px to remove white corners
    im_padded = np.zeros([im.shape[0] + 2 * pad, im.shape[1] + 2 * pad, 4])

    # Get border colour from left side of image
    bordercolour = np.median(im_recon_sc[200:(im_recon_sc.shape[0] - 200), 0:bordertol], axis=(0, 1))

    # Pad image
    for i in range(0, 4):
        im_padded[pad:im.shape[0] + pad, pad:im.shape[1] + pad, i] = im_recon_sc[:, :, i]

    # Overfill onto existing border to remove white corners
    # Left
    im_padded[0:im_padded.shape[0],
    0:pad + bordertol, :] = bordercolour

    # Right
    im_padded[0:im_padded.shape[0],
    im_padded.shape[1] - (pad + bordertol):im_padded.shape[1], :] = bordercolour

    # Top
    im_padded[0:pad + bordertol,
    0:im_padded.shape[1], :] = bordercolour

    # Bottom
    im_padded[im_padded.shape[0] - (pad + bordertol):im_padded.shape[0],
    0:im_padded.shape[1], :] = bordercolour

    # Write image to disk
    imageio.imwrite(main.IMAGE_FOLDER / img_path.name, im_padded.astype(np.uint8))
