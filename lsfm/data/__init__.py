from os.path import abspath
from pathlib import Path

import lsfm.io as lio
from menpo.transform import Translation, Scale
import numpy as np
from functools import lru_cache

DATA_DIR = Path(abspath(__file__)).parent

# We define a template that we use for the landmarks
LANDMARK_MASK = np.ones(68, dtype=np.bool)
# Remove the jaw...
LANDMARK_MASK[:18] = False
# ...and the inner lips for robustness.
LANDMARK_MASK[-8:] = False


def prepare_template_reference_space(template):
    r"""Return a copy of the template centred at the origin
    and with max radial distance from centre of 1.

    This means the template is:
      1. fully contained by a bounding sphere of radius 1 at the origin
      2. centred at the origin.

    This isn't necessary, but it's nice to have a meaningful reference space
    for our models.
    """
    max_radial = np.sqrt(
        ((template.points - template.centre()) ** 2).sum(axis=1)).max()
    translation = Translation(-template.centre())
    scale = Scale(1 / max_radial, n_dims=3)
    adjustment = translation.compose_before(scale)

    adjustment.apply(template)
    return adjustment.apply(template)


@lru_cache()
def load_camera_settings():
    return lio.import_pickle(DATA_DIR / 'camera.pkl')


def path_to_template():
    return DATA_DIR / 'template.pkl'


@lru_cache()
def load_template():
    template = lio.import_pickle(DATA_DIR / 'template.pkl')
    template.landmarks['__lsfm'] = template.landmarks['ibug68'].lms.from_mask(
        LANDMARK_MASK)
    return prepare_template_reference_space(template)


def save_template(template, overwrite=False):
    lio.export_pickle(template, path_to_template(), overwrite=overwrite)
