import numpy as np
from menpo.model import PCAModel
from menpo.visualize import print_progress


def prune(weights, n_retained=50):
    w_norm = (weights[:, :n_retained] ** 2).sum(axis=1)
    # High weights here suggest problematic samples
    bad_to_good_index = np.argsort(w_norm)[::-1]
    return w_norm, bad_to_good_index


def pca_and_weights(meshes, retain_eig_cum_val=0.997, verbose=False):
    model = PCAModel(meshes, verbose=verbose)
    n_comps_retained = (model.eigenvalues_cumulative_ratio() <
                        retain_eig_cum_val).sum()
    if verbose:
        print('\nRetaining {:.2%} of eigenvalues keeps {} components'.format(
              retain_eig_cum_val, n_comps_retained))
    model.trim_components(retain_eig_cum_val)
    if verbose:
        meshes = print_progress(meshes, prefix='Calculating weights')
    weights = (np.vstack([model.project(m) for m in meshes])
               / np.sqrt(model.eigenvalues))
    return model, weights
