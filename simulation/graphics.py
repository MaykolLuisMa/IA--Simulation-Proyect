import matplotlib.pyplot as plt

def show(values):
    y = values
    x = range(len(values))
    plt.plot(x,y,'ro-', label = "Grafica")
    plt.ylabel("Values")
    plt.xlabel("Week")
    plt.legend()
    plt.grid(True)
    plt.show()