import scipy.io as sio
import numpy as np
import os
import glob
import pickle

module_loc = os.path.dirname(__file__)
rel_loc = '../../../Downloads/Database/'  # path to raw data
file_name = '*E2*.mat'

myo_band_data = []


def main(rel_path, wildcard, **kwargs):
    for mat_file in glob.glob(get_folder_path(rel_path, wildcard)):
        mat = import_mat(mat_file)
        reps, diff_ind = get_rep_indices(mat)
        stims = get_stims(mat)
        emg = get_emg(mat)
        create_dict(emg, stims, diff_ind)
        save_data()
    return


def get_folder_path(rel_loc, wildcard):
    module_loc = os.path.dirname(__file__)
    rel_path = os.path.join(module_loc, rel_loc, wildcard)
    return rel_path


def import_mat(filename):
    mat = sio.loadmat(filename)
    return mat


def get_rep_indices(mat):
    reps = np.squeeze(mat['rerepetition'])
    diff_reps = [t - s for s, t in zip(reps, reps[1:])]
    diff_ind = np.where(np.array(diff_reps) != 0)[0].tolist()
    diff_ind = [x+290 for x in diff_ind]
    diff_ind.insert(0, 0)
    diff_ind.append(len(reps)-1)
    return reps, diff_ind


def get_stims(mat):
    stims = np.squeeze(mat['restimulus'])
    return stims


def get_emg(mat):
    emg = mat['emg']
    return emg


def create_dict(emg, stims, diff_ind):
    for start, end in zip(diff_ind, diff_ind[1:]):
        try:
            emg_data = emg[start:end]
            stimulus_data = stims[start:end]

            if len(emg_data) == 0:
                continue

            for_export = {'emg': emg_data,
                          'stimulus': stimulus_data}
            myo_band_data.append(for_export)
        except ValueError:

            continue


def save_data():
    with open('myobanddata.pkl', 'wb') as f:
        pickle.dump(myo_band_data, f, protocol=-1)


if __name__ == '__main__':
    main(rel_loc, file_name)
