import pygame
import random
import numpy as np
from settings import *
import time
import game_statistics
import os
import json

'''
Bu script main.py dosyasından çağırılıyor. amaç her saniye verileri
data klasöründe bulunan JSON doyasına kaydetmek.
'''

class PeriodicRecorder:
    def __init__(self, statistics, file_name="./data/game_statistics.json"):
        self.statistics = statistics
        self.file_name = file_name
        self.start_time = time.time()
        self.data = []  # Her saniyenin verileri burada birikir.

    def save_statistics_to_file(self):
        """Tüm kayıtları JSON dosyasına kaydet."""
        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)

    def record_statistics(self):
        """Anlık istatistikleri listeye ekle."""
        elapsed_time = int(time.time() - self.start_time)
        stats_snapshot = self.statistics.retun_statistics()
        stats_snapshot["time"] = elapsed_time  # Geçen süreyi ekliyoruz.
        self.data.append(stats_snapshot)
        print(f"Recorded stats at {elapsed_time} seconds: {stats_snapshot}")

    def start_recording(self, duration):
        """Belirtilen süre boyunca her saniye istatistik kaydet."""
        try:
            for _ in range(duration):
                self.record_statistics()
                #time.sleep(0.05)  # 1 saniye bekle
        finally:
            self.save_statistics_to_file()  # Program sonunda veriyi kaydet.


#PeriodicRecorder(global_stats_object).start_recording(10)