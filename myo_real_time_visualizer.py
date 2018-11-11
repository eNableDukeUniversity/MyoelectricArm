from __future__ import print_function
import collections
import myo
import threading
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation


class MyListener(myo.DeviceListener):

    def __init__(self, queue_size=8):
        self.lock = threading.Lock()
        self.emg_data_queue = collections.deque(maxlen=queue_size)
        self.start_time = time.time()

    def on_connect(self, device, timestamp, firmware_version):
        device.set_stream_emg(myo.StreamEmg.enabled)

    def on_emg_data(self, device, timestamp, emg_data):
        with self.lock:
            self.emg_data_queue.append((time.time(), emg_data))

    def get_emg_data(self):
        with self.lock:
            EMGData = collections.namedtuple('EMGData', ['time', 'recordings'])
            if len(self.emg_data_queue) != 0:
                return EMGData(list(self.emg_data_queue)[0][0],
                               list(self.emg_data_queue)[0][1])
            else:
                return EMGData(time.time(), [0, 0, 0, 0, 0, 0, 0, 0])


myo.init(dist_path="D:/Users/Gabriel/Documents/eNable/myo-sdk-win-0.9.0/bin/")
hub = myo.Hub()
listener = MyListener()


def data_gen():
    try:
        hub.run(10, listener)
        while True:
            time.sleep(0.010)
            data = listener.get_emg_data()
            time_val = data.time - listener.start_time
            time_val = time_val*(time_val > 0)
            yield time_val, data.recordings
    finally:
        hub.shutdown()


fig, ([ax1, ax2], [ax3, ax4], [ax5, ax6], [ax7, ax8]) = \
                    plt.subplots(nrows=4, ncols=2, sharex='all', sharey='all')
line1, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)
line3, = ax3.plot([], [], lw=2)
line4, = ax4.plot([], [], lw=2)
line5, = ax5.plot([], [], lw=2)
line6, = ax6.plot([], [], lw=2)
line7, = ax7.plot([], [], lw=2)
line8, = ax8.plot([], [], lw=2)

axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
lines = [line1, line2, line3, line4, line5, line6, line7, line8]


xdata, sen1, sen2, sen3, sen4, sen5, sen6, sen7, sen8 = [], [], [], [], [], \
                                                        [], [], [], []

sensors = [sen1, sen2, sen3, sen4, sen5, sen6, sen7, sen8]


def init():
    i = 0
    for ax in axes:
        ax.grid()
        ax.set_ylim(-75, 75)
        ax.set_xlim(0, 20)
    for line in lines:
        line.set_data([], [])
        i += 1
    return lines


def run(data):
    t, y = data

    xdata.append(t)
    list(map(lambda x, z: x.append(z), sensors, y))

    xmin, xmax = ax1.get_xlim()
    if t >= xmax:
        list(map(lambda x: x.set_xlim(xmax - 1, xmax + 19), axes))
        list(map(lambda x: x.figure.canvas.draw(), axes))

    iii = 0
    for line in lines:
        line.set_data(xdata, sensors[iii])
        iii += 1

    return lines


try:
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
                                  repeat=False, init_func=init)
    plt.show()
except (KeyboardInterrupt):
    hub.shutdown()
    raise KeyboardInterrupt
