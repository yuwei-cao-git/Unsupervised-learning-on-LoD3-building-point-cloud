#
#
#      0=================================0
#      |    Project Name                 |
#      0=================================0
#
#
# ----------------------------------------------------------------------------------------------------------------------
#
#      Implements point clouds augument functions, read/write, draw
#
# ----------------------------------------------------------------------------------------------------------------------
#
#      YUWEI CAO - 2020/10/20 15:40 PM
#
#


# ----------------------------------------
# import packages
# ----------------------------------------
import numpy as np

# ----------------------------------------
# Point cloud argument
# ----------------------------------------

def translate_pointcloud(pointcloud):
    xyz1 = np.random.uniform(low=2./3., high=3./2., size=[3])
    xyz2 = np.random.uniform(low=-0.2, high=0.2, size=[3])
    translated_pointcloud = np.add(np.multiply(pointcloud, xyz1), xyz2).astype('float32')
    return translated_pointcloud


def jitter_pointcloud(pointcloud, sigma=0.01, clip=0.02):
    N, C = pointcloud.shape
    pointcloud += np.clip(sigma * np.random.randn(N, C), -1*clip, clip)
    return pointcloud


def rotate_pointcloud(pointcloud):
    theta = np.pi*2 * np.random.rand()
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    pointcloud[:,[0,2]] = pointcloud[:,[0,2]].dot(rotation_matrix) # random rotation (x,z)
    return pointcloud


def getshiftedpc(point_set):
    xyz_min = np.amin(point_set, axis=0)[0:3]
    return xyz_min

def norm_rgb(points_colors):
    points_colors[:,0:3] /= 255.0
    return points_colors


def shuffle_pointcloud(pointcloud, label):
    N = pointcloud.shape[0]
    order = np.arrange(N)
    np.random.shuffle(order)
    pointcloud = pointcloud[order, :]
    lable = label[order]
    return pointcloud, label


# ----------------------------------------
# Point cloud IO
# ----------------------------------------

#parse point cloud files
def load_txt(filename):
    all_data = []
    all_label = []
    data = np.loadtxt(filename)
    scene_xyz = data[:,0:3].astype(np.float32)
    points_colors = data[:,3:6].astype(np.int8)
    points_norms = data[:,7:10]
    segment_label = data[:,6].astype(np.int8)

    return scene_xyz, points_colors, points_norms, segment_label


def write_ply(points, filename, text=True):
    """ input: Nx3, write points to filename as PLY format. """
    points = [(points[i,0], points[i,1], points[i,2]) for i in range(points.shape[0])]
    vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4')])
    el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
    PlyData([el], text=text).write(filename)


# ----------------------------------------
# Draw Point cloud
# ----------------------------------------
import matplotlib.pyplot as plt
def pyplot_draw_point_cloud(points, output_filename):
    """ points is a Nx3 numpy array """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:,0], points[:,1], points[:,2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    #savefig(output_filename)