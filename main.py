import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np

T_MAX = 30000
T_MIN = 2500

L_MAX = 1e6
L_MIN = 1e-4

'''
    Sets the scales, labels and titles for the X axis (temperature),
    and Y axis (Luminosity). 
    
    The X and Y axes are scaled by log_10 and log_2 respectively
'''
def create_hr_diagram():
    fig, ax = plt.subplots()
    ax.set_xscale('log', base=2)
    ax.set_xlim(T_MAX, T_MIN)
    ax.set_xlabel("Temperature (K)")
    
    #This formats the x labels better because the base formatting isnt great
    ticks = [30000, 17000, 10000, 5000, 2500]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter([str(t) for t in ticks]))

    ax.set_yscale('log')
    ax.set_ylim(L_MIN, L_MAX)
    ax.set_ylabel("Luminosity")
    return ax

'''
    Calculations are made from 
    https://405nm.com/wavelength-to-color/

    Converts temperature to rgb color using simple ranges
'''
def get_color(t):
    colors = [
        ("#783CFF"),  # 380 nm (violet)
        ("#3C78FF"),  # 430 nm (blue)
        ("#00AAFF"),  #  470 nm (cyan)
        ("#00DCAA"),  #  500 nm (blue green)
        ("#3CFF3C"),  #  540 nm (green)
        ("#FFFF00"),  #  580 nm (yellow)
        ("#FF8C00"),  #  620 nm (orange)
        ("#FF3C3C"),  #  700 nm (red)
    ]

    n = len(colors)

    T = min(t, T_MAX)
    T = max(t, T_MIN)

    idx = int((1.0 - (T - T_MIN) / (T_MAX - T_MIN)) * (n - 1) + 1e-9)
    return colors[idx]

'''
    Returns the radius of the star given the temperature and the luminance
    Converts the star luminosity from solar lumens to absolute units
'''
def get_radius(T, L):
    L_abs = L * 3.9e26
    R_sq = L_abs/(4 * np.pi * 5.67e-8 * T**4)
    r = np.sqrt(R_sq)

    return r

def get_plt_size(T, L):
    a_min = 10
    a_max = 10000
    R_min = get_radius(T_MAX, L_MIN)
    R_max = get_radius(T_MIN, L_MAX)
    R = get_radius(T, L)

    frac = (np.log10(R) - np.log10(R_min)) / (np.log10(R_max) - np.log10(R_min))
    frac = np.clip(frac, 0, 1)

    gamma = 2
    frac = frac**gamma

    return a_min + frac * (a_max - a_min)



def main():
    d = 10
    c = 'red'
    get_radius(30000, 1e-4)
    get_radius(2500, 1e6)
    ax = create_hr_diagram()
    ax.scatter([3000], [1e5], get_plt_size(3000, 1e5), get_color(3000))
    ax.scatter([5000], [10], get_plt_size(5000, 10), get_color(5000))
    ax.scatter([10000], [10], get_plt_size(10000, 10), get_color(10000))
    ax.scatter([15000], [10], get_plt_size(15000, 10), get_color(15000))
    ax.scatter([25000], [1e-3], get_plt_size(25000, 1e-3), get_color(25000))
    plt.show()

if __name__ == "__main__":
    main()