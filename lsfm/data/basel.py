from scipy.io import loadmat
from menpo.shape import ColouredTriMesh

import lsfm.io as lio
from . import DATA_DIR, save_template


def load_mean_from_basel(path):
    mm = loadmat(str(path))
    trilist = mm['tl'][:, [0, 2, 1]] - 1
    mean_points = mm['shapeMU'].reshape(-1, 3)
    mean_colour = mm['texMU'].reshape(-1, 3) / 255
    return ColouredTriMesh(mean_points, trilist=trilist, colours=mean_colour)


def load_basel_template_metadata():
    return lio.import_pickle(DATA_DIR / 'basel_template_metadata.pkl')


def generate_template_from_basel_and_metadata(basel, meta):
    template = ColouredTriMesh(basel.points[meta['map_tddfa_to_basel']],
                               trilist=meta['tddfa_trilist'],
                               colours=basel.colours[
                                   meta['map_tddfa_to_basel']])

    template.landmarks['ibug68'] = meta['landmarks']['ibug68']
    template.landmarks['nosetip'] = meta['landmarks']['nosetip']

    return template


def save_template_from_basel(path):
    basel = load_mean_from_basel(path)
    meta = load_basel_template_metadata()
    template = generate_template_from_basel_and_metadata(basel, meta)
    save_template(template, overwrite=True)
