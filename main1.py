import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.ticker import MultipleLocator, MaxNLocator, FuncFormatter
import pandas as pd
import re

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "figure.titlesize": 18
})

df = pd.read_csv("results5.csv")

def extract_temperature(filename):
    match = re.search(r'_(\d+\.?\d*)', filename)
    return float(match.group(1)) if match else None

df["Temperature"] = df["File"].apply(extract_temperature)
df = df.sort_values(by="Temperature")

frequencies = np.linspace(0, 500, 5000)
spectra = []
for amp in df["Amplitude"]:
    noise = np.random.normal(0, amp * 0.03, len(frequencies))
    signal = np.exp(-((frequencies - 73)/1)**2) * amp + noise
    spectra.append(signal)

temperatures = df["Temperature"].values
norm = colors.Normalize(vmin=100, vmax=200)
cmap = plt.colormaps['plasma']

dfp = pd.read_csv("methanol_252803MHz_pressure.dat", sep=r"\s+", names=["Frequency", "Pressure"])
pmin, pmax = dfp["Pressure"].min(), dfp["Pressure"].max()

def sci_tick(x, _):
    if x == 0:
        return "0"
    exp = int(np.floor(np.log10(abs(x))))
    coeff = x / (10 ** exp)
    return rf"${coeff:.0f}\times 10^{{{exp}}}$"

fig, ax = plt.subplots(figsize=(10, 6))
for temp, amp in zip(temperatures, spectra):
    ax.plot(frequencies, amp, color=cmap(norm(temp)))

ax.set_xlim(70, 76)
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Amplitude a.u.")
ax.tick_params(axis="y", labelcolor="tab:blue")
ax.set_title("Multi-File FFT Spectra Metanol")
ax.grid(True)

ax_press = ax.twinx()
ax_press.set_ylim(pmin, pmax)
ax_press.yaxis.set_major_locator(MaxNLocator(6))
ax_press.yaxis.set_major_formatter(FuncFormatter(sci_tick))
ax_press.tick_params(axis="y", labelcolor="tab:red")
ax_press.set_ylabel("")

plt.tight_layout(rect=[0, 0, 0.88, 1])
sm = cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label("Temperature (K)", fontsize=16)
cbar.ax.tick_params(labelsize=14, pad=4)

plt.show()

#LO = 252803.4
LO = 252730.4
frequencies_mol = frequencies + LO


fig2, ax2 = plt.subplots(figsize=(12, 6))
for temp, amp in zip(temperatures, spectra):
    ax2.plot(frequencies_mol, amp, color=cmap(norm(temp)))

ax2.set_xlim(252797, 252809)
ax2.xaxis.set_major_locator(MultipleLocator(2.0))
ax2.ticklabel_format(style='plain', axis='x')
ax2.get_xaxis().get_major_formatter().set_useOffset(False)
ax2.set_xlabel("Frequency (MHz)")
ax2.set_ylabel("Amplitude a.u.")
ax2.tick_params(axis="y")
ax2.set_title("Methanol Lineshape vs Temperature")
ax2.grid(True)

plt.tight_layout(rect=[0, 0, 0.75, 1])
fig2.subplots_adjust(right=0.82)

sm2 = cm.ScalarMappable(cmap=cmap, norm=norm); sm2.set_array([])
cbar2 = fig2.colorbar(sm2, ax=ax2)
cbar2.set_label("Temperature (K)", fontsize=16)
cbar2.ax.tick_params(labelsize=14)
pos2 = cbar2.ax.get_position()
cbar2.ax.set_position([pos2.x0 + 0.02, pos2.y0, pos2.width, pos2.height])

plt.show()
