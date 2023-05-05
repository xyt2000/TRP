from utils import load_my_data
from utils import extract_DenseSift_descriptors
from utils import build_codebook
from utils import input_vector_encoder
from classifier import svm_classifier
import feature_spm

import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Image loader')
parser.add_argument("--train", type=str, help='load training data')
parser.add_argument("--test", type=str, help='load test data (optional)')

args = parser.parse_args()
print "Training data load from {}".format(args.train)
print "Test data load from {}".format(args.test)

X, y = load_my_data(args.train)

# to save time...
X = X[:200]
y = y[:200]

print "Codebook Size: {:d}".format(feature_spm.VOC_SIZE)
print "Pyramid level: {:d}".format(feature_spm.PYRAMID_LEVEL)
print "Dense SIFT feature extraction"
x_feature = [extract_DenseSift_descriptors(img) for img in X]
x_kp, x_des = zip(*x_feature)

print "Building the codebook, it will take some time"
codebook = build_codebook(x_des, feature_spm.VOC_SIZE)
#import cPickle
#with open('./data/codebook_spm.pkl','w') as f:
#    cPickle.dump(codebook, f)

print "Spatial Pyramid Matching encoding"
X = [feature_spm.spatial_pyramid_matching(X[i],
                                          x_des[i],
                                          codebook,
                                          level=feature_spm.PYRAMID_LEVEL)
     for i in xrange(len(x_des))]

X = np.asarray(X)
svm_classifier(X, y)
