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

file1_path = "methanol_252803MHz_pressure.dat"
file2_path = "results5.csv"

k_B = 1.380649e-23
mbar_to_Pa = 100

df1 = pd.read_csv(file1_path, sep=r'\s+')
df1.columns = ['Frequency', 'Pressure_mbar']

df2 = pd.read_csv(file2_path)
df2.columns = df2.columns.str.strip()
df2['Temperature'] = df2['File'].apply(
    lambda f: float(re.search(r"_(\d+\.?\d*)", f).group(1)) if re.search(r"_(\d+\.?\d*)", f) else None
)
df2 = df2.dropna(subset=['Temperature'])

freq_peak_index = df1['Pressure_mbar'].idxmax()
freq_peak_x = df1['Frequency'].iloc[freq_peak_index]

temp_peak_index = df2['Amplitude'].idxmax()
temp_peak_x = df2['Temperature'].iloc[temp_peak_index]

shift = temp_peak_x - freq_peak_x
df1['Temperature'] = df1['Frequency'] + shift

df1['Pressure_Pa'] = df1['Pressure_mbar'] * 100
df1['Concentration_cm3'] = df1['Pressure_Pa'] / (k_B * df1['Temperature']) / 1e6

fig, ax = plt.subplots(figsize=(10, 5))


ax.plot(df1['Temperature'], df1['Concentration_cm3'], color='blue', label='Density')
ax.set_xlim(100, 200)
ax.set_ylim(bottom=0)
ax.set_xlabel("Temperature (K)", fontsize=16)
ax.set_ylabel(r"$\mathrm{Density\ (cm^{-3})}$", color='blue', fontsize=16)
ax.tick_params(axis='y', labelcolor='blue')

def sci_notation_formatter(x, _):
    if x == 0:
        return "0"
    exponent = int(np.floor(np.log10(abs(x))))
    coeff = x / (10 ** exponent)
    return fr"${coeff:.1f} \times 10^{{{exponent}}}$"

ax.yaxis.set_major_formatter(FuncFormatter(sci_notation_formatter))

ax2 = ax.twinx()
ax2.plot(
    df2['Temperature'],
    df2['Amplitude']/df2['Amplitude'].max()*df1['Pressure_mbar'].max(),
    color='blue', linestyle='--', label='Pressure')

ax2.set_ylabel(r"$\mathrm{Pressure\ (mbar)}$", color='blue', fontsize=16)
ax2.tick_params(axis='y', labelcolor='blue')
ax2.yaxis.set_label_position("left")
ax2.yaxis.tick_left()
ax2.spines["left"].set_position(("outward", 105))
ax2.yaxis.set_major_formatter(FuncFormatter(sci_notation_formatter))


ax3 = ax.twinx()
ax3.plot(df2['Temperature'], df2['Amplitude'], color='red', linestyle='-', label='Amplitude')

ax3.set_ylabel("Amplitude (a.u.)", color='red', fontsize=16)
ax3.tick_params(axis='y', labelcolor='red')

ax.xaxis.set_minor_locator(AutoMinorLocator())

#plt.title("Methanol Density, Pressure and Amplitude vs Temperature", fontsize=14)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
