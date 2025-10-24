import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import re
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import AutoMinorLocator

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "figure.titlesize": 18
})

file1_path = "scan_183310-183311_pressure.dat"
file2_path = "results11.csv"

k_B = 1.380649e-23
mbar_to_Pa = 100

df1 = pd.read_csv(file1_path, sep=r'\s+')
df1.columns = ['Frequency', 'Pressure_mbar']

df2 = pd.read_csv(file2_path)
def extract_temperature(filename):
    m = re.search(r"_(\d+\.?\d*)", filename)
    return float(m.group(1)) if m else None
df2['Temperature'] = df2['File'].apply(extract_temperature)
df2 = df2.dropna(subset=['Temperature'])


freq_peak_index = df1['Pressure_mbar'].idxmax()
freq_peak_x = df1['Frequency'].iloc[freq_peak_index]
temp_peak_index = df2['Amplitude'].idxmax()
temp_peak_x = df2['Temperature'].iloc[temp_peak_index]
shift = temp_peak_x - freq_peak_x
df1['Temperature'] = df1['Frequency'] + shift

df1['Pressure_Pa']   = df1['Pressure_mbar'] * mbar_to_Pa
df1['Density_cm3']   = df1['Pressure_Pa'] / (k_B * df1['Temperature']) / 1e6


def sci_fmt(x, _):
    if x == 0:
        return "0"
    e = int(np.floor(np.log10(abs(x))))
    c = x / (10**e)
    return fr"${c:.1f}\times 10^{{{e}}}$"

fig, ax = plt.subplots(figsize=(10, 5))


ax.plot(df1['Temperature'], df1['Density_cm3'], color='blue', label='Density')
ax.set_xlim(130, 200)
ax.set_ylim(bottom=0)
ax.set_xlabel("Temperature (K)", fontsize=16)
ax.set_ylabel(r"Density (cm$^{-3}$)", color='blue', fontsize=16)
ax.tick_params(axis='y', labelcolor='blue')
ax.yaxis.set_major_formatter(FuncFormatter(sci_fmt))


max_pressure = df1['Pressure_mbar'].max()
scaled_pressure = df2['Amplitude'] / df2['Amplitude'].max() * max_pressure

ax2 = ax.twinx()
ax2.plot(df2['Temperature'], scaled_pressure, color='blue', linestyle='--', label='Pressure')
ax2.set_ylabel("Pressure (mbar)", color='blue', fontsize=12)
ax2.tick_params(axis='y', labelcolor='blue')
ax2.yaxis.set_major_formatter(FuncFormatter(sci_fmt))

ax2.yaxis.set_label_position("left")
ax2.yaxis.tick_left()
ax2.spines["left"].set_position(("outward", 105))

ax3 = ax.twinx()
ax3.plot(df2['Temperature'], df2['Amplitude'], color='red', label='Amplitude')
ax3.set_ylabel("Amplitude (a.u.)", color='red', fontsize=16)
ax3.tick_params(axis='y', labelcolor='red')

ax.xaxis.set_minor_locator(AutoMinorLocator())

#plt.title("H₂O Density & Pressure and Amplitude vs Temperature", fontsize=14)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
