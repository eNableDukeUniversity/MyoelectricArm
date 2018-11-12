import pickle
from math import floor
from statistics import mode, StatisticsError
import numpy as np
import pywt

with open('myobanddata.pkl', 'rb') as f:
    data = pickle.load(f)


max_label = 0
window_size = 200

nn_data = []

window_size = 200
window_diff = 50

first_level = 108
second_level = 62
third_level = 39

wavelet_length = first_level + second_level + 2*third_level
num_electrodes = 16

for trial in data:
    emg_signal = trial['emg']
    stimulus = trial['stimulus']

    window_max = floor((len(emg_signal) - window_size)/window_diff) + 1

    if window_max < 1:
        continue

    start_index = 0

    for i in range(0, window_max):
        wavelet_coeffs = np.zeros((num_electrodes, wavelet_length))
        all_emg = np.zeros((num_electrodes, window_size))
        rms_electrodes = np.sqrt(np.mean(np.square(emg_signal[start_index:(start_index + window_size)]), axis=0))
        num = 0
        for electrodes in emg_signal.T:
            emg_data = electrodes[start_index:(start_index + window_size)]
            cA3, cD3, cD2, cD1 = pywt.wavedec(emg_data,
                                              wavelet='db9',
                                              mode='zero',
                                              level=3)
            all_emg[num, :] = emg_data
            wavelet_coeffs[num, :] = np.concatenate((cD1, cD2, cD3, cA3))
            num += 1

        stim_label = np.zeros((18))
        try:
            label_ind = mode(stimulus[start_index:(start_index + window_size)])
        except StatisticsError:
            label_ind = stimulus[start_index:(start_index + window_size)].max()
        wavelet_coeffs = np.reshape(wavelet_coeffs, (248, 16))
        all_emg = np.reshape(all_emg, (200, 16))
        stim_label[label_ind] = 1
        nn_data.append({'wavelet': wavelet_coeffs,
                        'emg': all_emg,
                        'rms': rms_electrodes,
                        'label': stim_label})
        print(label_ind)
        start_index += window_diff


with open('full_data.pkl', 'wb') as f:
    pickle.dump(nn_data, f, protocol=-1)
