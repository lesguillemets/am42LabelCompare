
import matplotlib.pyplot as plt
import matplotlib.colors as clr

N : int = 5

def load(f):
    with open(f) as f:
        dat = f.read()
    d: list[int] = list(map(int, dat.split('\n')))
    return d


width_in_pixels = 2000
# Convert width to inches (1 inch = 96 pixels)
width_in_inches = width_in_pixels / 96

# Specify the height in inches (you can adjust this as needed)
height_in_inches = 3

def main():
    d = load("./assets/majority_iter2_conv_6frames_HAorNOAH.csv") # ラベルの一致した数
    # d = load("./assets/majority_counts_HAorNOHA.csv") # HAかどうかの合致
    report(d)
    report_two(d)
    do_plot(d)
    # fig = plt.figure()

def report(d):
    """
    半数以上の人が合致してるフレーム数
    """
    l = len(d)
    matches = len(list(filter(lambda n: n > N//2, d)))
    print(f"{matches} / {l} frames: ratio = {matches/l}"  )

def report_two(d):
    """
    4人以上の人が合致してるフレーム数
    """
    l = len(d)
    matches = len(list(filter(lambda n: n >= 4, d)))
    print(f"{matches} / {l} frames: ratio = {matches/l}"  )

def do_plot(d):
    fig, ax = plt.subplots(figsize=(width_in_inches, height_in_inches))
    ax.fill_between(range(len(d)),d, color=clr.CSS4_COLORS['teal']) # 色つけるとき
    # ax.fill_between(range(len(d)),d) # そのままの色のとき
    ax.set_xlim(0, len(d))
    ax.set_ylim(0, N)
    ax.set_yticks(list(range(N)))
    ax.tick_params(axis='y', direction='in', pad=-22)
    fig.show()
    n = input()
    fig.savefig("assets/agreements_iter02_max6frames_HAorNOAH_series.svg")

if __name__ == "__main__":
    main()

