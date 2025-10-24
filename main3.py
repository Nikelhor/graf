import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.ticker import MultipleLocator
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

df = pd.read_csv("results11.csv")

def extract_temperature(filename):
    match = re.search(r'_(\d+\.?\d*)', filename)
    return float(match.group(1)) if match else None

df["Temperature"] = df["File"].apply(extract_temperature)
df = df.sort_values(by="Temperature")

frequencies = np.linspace(0, 500, 5000)
spectra = []
for amp in df["Amplitude"]:
    noise = np.random.normal(0, amp * 0.02, len(frequencies))
    signal = np.exp(-((frequencies - 65)/1)**2) * amp + noise
    spectra.append(signal)

temperatures = df["Temperature"].values

#norm = colors.Normalize(vmin=temperatures.min(), vmax=temperatures.max())
norm = colors.Normalize(vmin=100, vmax=200)
cmap = plt.colormaps['plasma']

fig, ax = plt.subplots(figsize=(10, 6))

for temp, amp in zip(temperatures, spectra):
    ax.plot(frequencies, amp, color=cmap(norm(temp)))

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, label="Temperature (K)")

ax.set_xlim(62, 68)
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Amplitude")
ax.set_title("Multi-File FFT Spectra H2O")
ax.grid(True)
plt.tight_layout()
plt.show()

LO = 183245
frequencies_mol = frequencies + LO

fig2, ax2 = plt.subplots(figsize=(10, 6))
for temp, amp in zip(temperatures, spectra):
    ax2.plot(frequencies_mol, amp, color=cmap(norm(temp)))

sm2 = cm.ScalarMappable(cmap=cmap, norm=norm)
sm2.set_array([])
fig2.colorbar(sm2, ax=ax2, label="Temperature (K)")

ax2.set_xlim(183304, 183316)
ax2.xaxis.set_major_locator(MultipleLocator(2.0))
ax2.xaxis.set_minor_locator(MultipleLocator(1.0))
ax2.ticklabel_format(style='plain', axis='x')
ax2.get_xaxis().get_major_formatter().set_useOffset(False)
ax2.set_xlabel("Frequency (MHz)")
ax2.set_ylabel("Amplitude a.u.")
ax2.set_title("Molecular Spectrum H2O")
ax2.grid(True)
plt.tight_layout()
plt.show()
