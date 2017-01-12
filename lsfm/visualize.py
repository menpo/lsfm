import numpy as np
from menpo.image import Image
from menpo.shape import ColouredTriMesh
from menpo.transform import AlignmentSimilarity
from menpo3d.rasterize import rasterize_mesh
from scipy.stats import chi2

from .camera import perspective_camera_for_template
from .data import load_template
from .shading import lambertian_shading
from matplotlib import pyplot as plt


def rasterize_mesh_at_template(mesh, img_shape=(640, 480),
                               pose_angle_deg=0, shaded=False):
    camera = perspective_camera_for_template(img_shape,
                                             pose_angle_deg=pose_angle_deg)
    mesh_aligned = AlignmentSimilarity(mesh, load_template()).apply(mesh)

    if shaded:
        mesh_aligned = lambertian_shading(mesh_aligned)

    return rasterize_mesh(camera.apply(mesh_aligned), img_shape)


def visualize_nicp_weighting(template, weighting):
    colours = ((weighting[:, None] * np.array([1, 0, 0])) +
               ((1 - weighting[:, None]) * np.array([1, 1, 1])))
    print('min: {}, max: {}'.format(weighting.min(), weighting.max()))
    ColouredTriMesh(template.points, trilist=template.trilist,
                    colours=colours).view()


def visualize_pruning(w_norm, n_retained,
                      title='Initial model weights vs theoretical for pruning'):
    fig, ax1 = plt.subplots()
    ax1.set_title(title)
    ax1.hist(w_norm, normed=True, bins=200, alpha=0.6, histtype='stepfilled',
             range=[0, n_retained * 5])
    ax1.axvline(x=n_retained, linewidth=1, color='r')
    ax1.set_ylabel('PDF', color='b')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Survival Function', color='r')

    ax1.set_xlabel('w_norm')

    x = np.linspace(chi2.ppf(0.001, n_retained),
                    chi2.ppf(0.999, n_retained), 100)
    ax2.plot(x, chi2.sf(x, n_retained),
             'g-', lw=1, alpha=0.6, label='chi2 pdf')
    ax1.plot(x, chi2.pdf(x, n_retained),
             'r-', lw=1, alpha=0.6, label='chi2 pdf')


def visualize_nicp_result(mesh):

    l = rasterize_mesh_at_template(mesh, pose_angle_deg=+20, shaded=True)
    r = rasterize_mesh_at_template(mesh, pose_angle_deg=-20, shaded=True)

    return Image(np.concatenate([l.pixels, r.pixels], axis=-1))
