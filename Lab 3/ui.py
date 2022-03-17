import matplotlib.pyplot as plt
import numpy as np
import time

TIME = []
LIGHT = []
HUMIDITY = []
XLIM = [0,1]
YLIM = [0,1]
MAX_DISPLAY_SIZE = 20

start_time = time.time()


def fetch_data():
    TIME.append(time.time()-start_time)
    LIGHT.append(np.random.random_sample(1))
    HUMIDITY.append(np.random.random_sample(1))
    if len(TIME) > MAX_DISPLAY_SIZE:
        TIME.pop(0)
        LIGHT.pop(0)
        HUMIDITY.pop(0)
    time.sleep(1)


def main_loop():
    plt.ion()
    while True:
        fetch_data()
        fig, axs = plt.subplots(2, figsize=(10, 10))
        axs[0].set_title("Light Intensity vs. Time")
        axs[1].set_title("Humidity vs. Time")
        axs[0].plot(TIME, LIGHT)
        axs[1].plot(TIME, HUMIDITY)
        plt.draw()
        plt.pause(0.00001)
        plt.clf()


main_loop()
