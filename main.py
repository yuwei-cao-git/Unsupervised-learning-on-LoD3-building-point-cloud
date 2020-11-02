
#
#
#      0=================================0
#      |    Project Name                 |
#      0=================================0
#
#
# ----------------------------------------------------------------------------------------------------------------------
#
#      Implements
#
# ----------------------------------------------------------------------------------------------------------------------
#
#      YUWEI CAO - 2020/10/26 17:17 PM 
#
#


import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(ROOT_DIR, 'model'))

from evaluation import Inference
from trainer import Trainer
from svm import SVM

def get_parser():
    parser = argparse.ArgumentParser(description='Unsupervised Building Point Cloud Feature Learning')
    parser.add_argument('--experiment_name', type=str, default=None, metavar='N',
                        help='Name of the experiment')
    parser.add_argument('--encoder', type=str, default='foldnet', metavar='N',
                        choices=['foldnet', 'dgcnn_cls', 'dgcnn_seg'],
                        help='Encoder to use, [foldnet, dgcnn_cls, dgcnn_seg]')
    parser.add_argument('--dropout', type=float, default=0.5,
                        help='dropout rate')
    parser.add_argument('--feat_dims', type=int, default=512, metavar='N',
                        help='Number of dims for feature ')
    parser.add_argument('--k', type=int, default=None, metavar='N',
                        help='Num of nearest neighbors to use for KNN')
    parser.add_argument('--dataset', type=str, default='shapenetcorev2', metavar='N',
                        choices=['arch','shapenetcorev2','modelnet40', 'modelnet10'],
                        help='Encoder to use, [arch, shapenetcorev2, modelnet40, modelnet10]')
    parser.add_argument('--use_rotate', action='store_true',
                        help='Rotate the pointcloud before training')
    parser.add_argument('--use_translate', action='store_true',
                        help='Translate the pointcloud before training')
    parser.add_argument('--use_jitter', action='store_true',
                        help='Jitter the pointcloud before training')
    parser.add_argument('--batch_size', type=int, default=16, metavar='batch_size',
                        help='Size of batch)')
    parser.add_argument('--workers', type=int, help='Number of data loading workers', default=16)
    parser.add_argument('--epochs', type=int, default=None, metavar='N',
                        help='Number of episode to train ')
    parser.add_argument('--snapshot_interval', type=int, default=10, metavar='N',
                        help='Save snapshot interval ')
    parser.add_argument('--gpu_mode', action='store_true',
                        help='Enables CUDA training')
    parser.add_argument('--eval', action='store_true',
                        help='Evaluate the model')
    parser.add_argument('--num_points', type=int, default=2048,
                        help='Num of points to use')
    parser.add_argument('--model_path', type=str, default='', metavar='N',
                        help='Path to load model')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_parser()
    if args.eval == False:
        reconstruction = Trainer(args)
        reconstruction.train()
    else:
        inference = Inference(args)
        feature_dir = inference.evaluate()
        svm = SVM(feature_dir)
        svm.classify()