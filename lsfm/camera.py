import numpy as np

from menpo.transform import Rotation, Translation
from menpo3d.camera import PerspectiveProjection, PerspectiveCamera


# For now we mirror these here - should migrate to menpo conv. constructors
# after https://github.com/menpo/menpo/pull/777 comes in.


def rotation_from_3d_ccw_angle_around_y(theta, degrees=True):
    r"""
    Convenience constructor for 3D CCW rotations around the y axis

    Parameters
    ----------
    theta : `float`
        The angle of rotation about the origin
    degrees : `bool`, optional
        If ``True`` theta is interpreted as a degree. If ``False``, theta is
        interpreted as radians.

    Returns
    -------
    rotation : :map:`Rotation`
        A 3D rotation transform.
    """
    if degrees:
        # convert to radians
        theta = theta * np.pi / 180.0
    return Rotation(np.array([[np.cos(theta), 0, np.sin(theta)],
                              [0, 1, 0],
                              [-np.sin(theta), 0, np.cos(theta)]]),
                    skip_checks=True)


def rotation_from_3d_ccw_angle_around_z(theta, degrees=True):
    r"""
    Convenience constructor for 3D CCW rotations around the z axis

    Parameters
    ----------
    theta : `float`
        The angle of rotation about the origin
    degrees : `bool`, optional
        If ``True`` theta is interpreted as a degree. If ``False``, theta is
        interpreted as radians.

    Returns
    -------
    rotation : :map:`Rotation`
        A 3D rotation transform.
    """
    if degrees:
        # convert to radians
        theta = theta * np.pi / 180.0
    return Rotation(np.array([[np.cos(theta), -np.sin(theta), 0],
                              [np.sin(theta), np.cos(theta), 0],
                              [0, 0, 1]]),
                    skip_checks=True)


def perspective_camera_for_template(img_shape, focal_length_mult=1.1,
                                    pose_angle_deg=0):
    f = np.array(img_shape).max() * focal_length_mult
    rot_z = rotation_from_3d_ccw_angle_around_z(180)
    rot_y = rotation_from_3d_ccw_angle_around_y(180 + pose_angle_deg)
    rotation = rot_z.compose_before(rot_y)

    translation = Translation([0, 0, +3])
    projection = PerspectiveProjection(f, img_shape)
    return PerspectiveCamera(rotation, translation, projection)
