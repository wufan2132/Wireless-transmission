import matplotlib.pyplot as plt

def draw(input, output_need, output_value, energy_rate):
    x_axix = list(range(len(input)))
    plt.plot(x_axix, input, color='green', label='input')
    plt.plot(x_axix, output_need, color='blue', label='output_need')
    plt.plot(x_axix, output_value, color='skyblue', label='output_value')
    plt.plot(x_axix, energy_rate, color='red', label='energy_rate')
    plt.legend()  # 显示图例
    plt.show()


class plot():
    def __init__(self, refresh=True):
        self.refresh = refresh
        plt.figure(figsize=(10, 6), dpi=80)
        if self.refresh:
            plt.ion()