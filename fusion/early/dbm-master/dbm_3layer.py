# Implementation of 3 layer ( 2 hidden layer ) Deep Boltzmann Machine
from __future__ import division
import numpy as np
from scipy.special import expit
from matplotlib import pylab as plt

from evaluate.apfd import get_apfd
from pipeline.fileUtils import read_path
from prioritization.art import  art_sim_matrix_new
from text_feature.distance import get_sim_matrix


def binary_cross_entropy(data, reconst):
    return - np.mean( np.sum( data * np.log(reconst) + (1-data) * np.log(1 - reconst), axis=1) )

def reconstruct_data(data, b, c1, c2, w_vh1, w_h1h2, num_sample=100):
    m_h1 = expit( np.dot(data, w_vh1) + c1 )
    for i in range(num_sample):
        m_h2 = expit( np.dot(m_h1, w_h1h2) + c2 )
        m_h1 = expit( np.dot(w_h1h2, m_h2.T).T + c1 )
    return expit( np.dot(w_vh1, m_h1.T).T + b )

def popup(data, c1, w_vh1):
    return expit( np.dot(data, w_vh1) + c1 )

def rbm_contrastive_divergence(data, b, c, w, num_sample=10):
    # Mean field
    m_vis = data
    m_hid = expit( np.dot(data, w) + c )
    # Gibbs sample
    s_vis = m_vis
    for i in range(num_sample):
        sm_hid = expit( np.dot(s_vis, w) + c )
        s_hid = np.random.binomial(1, sm_hid)
        sm_vis = expit( np.dot(w, s_hid.T).T + b )
        s_vis = np.random.binomial(1, sm_vis)
    return np.mean(m_vis - s_vis, axis=0), np.mean(m_hid - s_hid, axis=0), \
                    (np.dot(m_vis.T, m_hid) - np.dot(s_vis.T, s_hid)) / len(data)

def dbm_contrastive_divergence(data, b, c1, c2, w_vh1, w_h1h2, num_sample=10):
    # Mean field
    m_vis = data
    m_h1 = np.random.uniform(size=(len(data), len(c1)))
    m_h2 = np.random.uniform(size=(len(data), len(c2)))
    for i in range(num_sample):
        m_h1 = expit( np.dot(m_vis, w_vh1) + np.dot(w_h1h2, m_h2.T).T + c1 )
        m_h2 = expit( np.dot(m_h1, w_h1h2) + c2 )
    # Gibbs sample
    # print(m_vis)
    s_vis = np.random.binomial(1, m_vis)
    s_h1 = np.random.binomial(1, 0.5, size=(len(data), len(c1)))
    s_h2 = np.random.binomial(1, 0.5, size=(len(data), len(c2)))
    for i in range(num_sample):
        sm_vis = expit( np.dot(w_vh1, s_h1.T).T + b )
        s_vis = np.random.binomial(1, sm_vis)
        sm_h1 = expit( np.dot(s_vis, w_vh1) + np.dot(w_h1h2, s_h2.T).T + c1 )
        s_h1 = np.random.binomial(1, sm_h1)
        sm_h2 = expit( np.dot(s_h1, w_h1h2) + c2 )
        s_h2 = np.random.binomial(1, sm_h2)
    return np.mean(m_vis - s_vis, axis=0), np.mean(m_h1 - s_h1, axis=0), np.mean(m_h2 - s_h2, axis=0), \
                ( np.dot(m_vis.T, m_h1) - np.dot(s_vis.T, s_h1) ) / len(data), ( np.dot(m_h1.T, m_h2) - np.dot(s_h1.T, s_h2) ) / len(data)



def dbm(data):
    # Assign structural parameters
    num_visible = data.shape[1]
    num_hidden1 = 1000
    num_hidden2 = 500

    # Assign learning parameters     # Assign learning parameters
    pretrain_epochs = 100
    pretrain_learning_rate = 0.1
    train_epochs = 100
    train_learning_rate = 0.1

    # Initialize weights
    b = np.zeros((num_visible, ))
    c1 = np.zeros((num_hidden1, ))
    c2 = np.zeros((num_hidden2, ))
    w_vh1 = np.random.normal(scale=0.01, size=(num_visible, num_hidden1))
    w_h1h2 = np.random.normal(scale=0.01, size=(num_hidden1, num_hidden2))

    # Load data, data needs to be in range [0, 1]
    data = data
    # Pretraining
    for i in range(pretrain_epochs):
        # Calculate gradient
        update_b, update_c1, update_w_vh1 = rbm_contrastive_divergence(data, b, c1, w_vh1)
        # Upate parameters
        b += pretrain_learning_rate * update_b
        c1 += pretrain_learning_rate * update_c1
        w_vh1 += pretrain_learning_rate * update_w_vh1

    pseudo_data = popup(data, c1, w_vh1)
    for i in range(pretrain_epochs):
        # Calculate gradient
        update_c1, update_c2, update_w_h1h2 = rbm_contrastive_divergence(pseudo_data, c1, c2, w_h1h2)
        # Upate parameters
        c1 += pretrain_learning_rate * update_c1
        c2 += pretrain_learning_rate * update_c2
        w_h1h2 += pretrain_learning_rate * update_w_h1h2
    pseudo_data = popup(pseudo_data, c2, w_h1h2)
    print(reconstruct_data(data, b, c1, c2, w_vh1, w_h1h2))
    # Show current cost
    cost = binary_cross_entropy(data, reconstruct_data(data, b, c1, c2, w_vh1, w_h1h2))
    print( "Reconstruction cost is %.2f"%cost )

    # Fine tuning
    for i in range(train_epochs):
        # Calculate gradient
        update_b, update_c1, update_c2, update_w_vh1, update_w_h1h2 \
                                        = dbm_contrastive_divergence(data, b, c1, c2, w_vh1, w_h1h2)
        # Update parameters
        b += train_learning_rate * update_b
        c1 += train_learning_rate * update_c1
        c2 += train_learning_rate * update_c2
        w_vh1 += train_learning_rate * update_w_vh1
        w_h1h2 += train_learning_rate * update_w_h1h2
        cost = binary_cross_entropy(data, reconstruct_data(data, b, c1, c2, w_vh1, w_h1h2))
        print("Reconstruction cost is %.2f" % cost)

    # Show fine tuning result
    cost = binary_cross_entropy(data, reconstruct_data(data, b, c1, c2, w_vh1, w_h1h2))
    print( "Reconstruction cost is %.2f"%cost )
    pseudo_data = popup(data, c1, w_vh1)
    pseudo_data = popup(pseudo_data, c2, w_h1h2)
    return pseudo_data
    # Show result images
    return reconstruct_data(data, b, c1, c2, w_vh1, w_h1h2)

data = read_path("output","spm",1)
data = np.array(data)
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] > 1:
            data[i][j] = 1
matrix = get_sim_matrix(data)
# print(matrix)
sequence = art_sim_matrix_new(matrix)
app_path = "E:\TRP\data\\reports\\" + str(1) + "\\" + "app" + str(1) + ".csv"
apfd = get_apfd(app_path, sequence)
print(apfd)

matrix = dbm(data)
#print(matrix)
matrix = get_sim_matrix(matrix)
#print(matrix)
sequence = art_sim_matrix_new(matrix)
apfd = get_apfd(app_path, sequence)
print(apfd)