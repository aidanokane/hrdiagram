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
    return fig, ax

'''
    Converts temperature color to rgb color
    Honestly I do not know the math behind this
'''
def get_color(T):
    T = max(1000.0, min(40000.0, float(T)))
    t = T / 100.0

    # --- Red ---
    if t <= 66.0:
        r = 255.0
    else:
        r = 329.698727446 * ((t - 60.0) ** -0.1332047592)

    # --- Green ---
    if t <= 66.0:
        g = 99.4708025861 * np.log(t) - 161.1195681661
    else:
        g = 288.1221695283 * ((t - 60.0) ** -0.0755148492)

    # --- Blue ---
    if t >= 66.0:
        b = 255.0
    elif t <= 19.0:
        b = 0.0
    else:
        b = 138.5177312231 * np.log(t - 10.0) - 305.0447927307

    # clamp to 0..255 and convert to int
    r = int(max(0.0, min(255.0, r)))
    g = int(max(0.0, min(255.0, g)))
    b = int(max(0.0, min(255.0, b)))

    return f"#{r:02X}{g:02X}{b:02X}"

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

    R_anchor = get_radius(T_MAX, L_MAX)
    frac_anchor = (np.log10(R_anchor) - np.log10(R_min)) / (np.log10(R_max) - np.log10(R_min))
    frac_anchor = np.clip(frac_anchor, 1e-6, 1 - 1e-6)

    target = 0.5  # halfway between a_min and a_max

    # solve gamma so frac_anchor maps to target
    gamma = np.log(target) / np.log(frac_anchor)

    # apply curve
    frac = frac ** gamma
    return a_min + frac * (a_max - a_min)


def main():
    d = 10
    c = 'red'
    get_radius(30000, 1e-4)
    get_radius(2500, 1e6)
    fig, ax = create_hr_diagram()
    ax.scatter([4000], [1e4], get_plt_size(4000, 1e4), get_color(4000))
    ax.scatter([5000], [10], get_plt_size(5000, 10), get_color(5000))
    ax.scatter([10000], [10], get_plt_size(10000, 10), get_color(10000))
    ax.scatter([15000], [10], get_plt_size(15000, 10), get_color(15000))
    pt = ax.scatter([25000], [1e-3], get_plt_size(25000, 1e-3), get_color(25000))

    dragging = False
    button = None

    def on_press(event):
        nonlocal dragging, button
        if(not event.inaxes):
            return
        else:
            contains, _ = pt.contains(event)
            if contains:
                dragging = True
                button = event.button

    def on_release(event):
        nonlocal dragging, button
    # Only end drag if we are dragging and this is the same button
        if not dragging:
            return
        if event.button != button:
            return
        
        dragging = False
        button = None

    def on_motion(event):
        nonlocal dragging, button
        if not dragging:
            return
        if event.inaxes != ax:
            return
        if event.xdata is None or event.ydata is None:
            return
        
        x = event.xdata
        y = event.ydata

        pt.set_offsets([[x, y]])
        pt.set_color(get_color(x))
        pt.set_sizes([get_plt_size(x, y)])
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("button_press_event", on_press)
    fig.canvas.mpl_connect("button_release_event", on_release)
    fig.canvas.mpl_connect("motion_notify_event", on_motion)

    plt.subplots_adjust(right=0.70)

    tax = fig.add_axes([0.75, 0.15, 0.22, 0.7])
    tax.axis("off")

    cell_text = [
        ["T (K)", "5800"],
        ["L", "1.0"],
        ["R", "1.0"],
        ["λ_peak", "500 nm"],
    ]

    table = tax.table(cellText=cell_text, loc="center")
    table.scale(1, 1.4)
    plt.show()

if __name__ == "__main__":
    main()