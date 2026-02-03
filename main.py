import matplotlib.pyplot as plt
import numpy as np

def main():
    fig, ax = plt.subplots()
    ax.scatter([1, 2, 3, 4], [1, 4, 9, 16])
    plt.show()

if __name__ == "__main__":
    main()