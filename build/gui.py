from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
sys.path.append('C:\\Users\\dell\\GUI-read-Bk-precision-data')
from readData import Add_current, Bkp8600
import time

ASSETS_PATH = Path(r"C:\Users\dell\GUI-read-Bk-precision-data\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
    

def validate_numeric_input(P):
    if P.isdigit() or P == "":
        return True
    return False


def get_data():
    last = Bkp8600()
    last.initialize()
    
    measured_current = last.get_current()
    voltage = last.get_voltage()
    
    last.reset_to_manual()
    del last
    
    return measured_current, voltage
    
def animateCurrent(i, ax, dataList):
    current = get_data()
    dataList.append(current[0])
    dataList = dataList[-50:]  # Limit to the last 50 data points
    ax.clear()
    ax.plot(dataList)
    ax.set_ylim([0.0001, 0.001])
    ax.set_title("Current Change")
    ax.set_ylabel("Current Value")

def animateVoltage(i, ax, dataList):
    voltage = get_data()
    dataList.append(voltage[1])
    dataList = dataList[-50:]  # Limit to the last 50 data points
    ax.clear()
    ax.plot(dataList)
    ax.set_ylim([0, 0.005])
    ax.set_title("Voltage Change")
    ax.set_ylabel("Voltage Value")
    


def main():
    window = Tk()
    window.geometry("1000x550")
    window.configure(bg = "#000000")



    canvas = Canvas(
        window,
        bg = "#000000",
        height = 550,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        171.0,
        36.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        499.0,
        70.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        78.0,
        308.0,
        image=image_image_3
    )

    canvas.create_text(
        48.0,
        118.0,
        anchor="nw",
        text="Data",
        fill="#000000",
        font=("Inter Medium", 16 * -1,"bold")
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        64.0,
        160.0,
        image=image_image_4
    )

    canvas.create_text(
        46.0,
        185.0,
        anchor="nw",
        text="Control",
        fill="#000000",
        font=("Inter Medium", 16 * -1,"bold")
    )

    canvas.create_text(
        47.0,
        236.0,
        anchor="nw",
        text="Management",
        fill="#000000",
        font=("Inter Medium", 16 * -1,"bold")
    )

    canvas.create_text(
        47.0,
        290.0,
        anchor="nw",
        text="State",
        fill="#000000",
        font=("Inter Medium", 16 * -1,"bold")
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        23.0,
        127.0,
        image=image_image_5
    )

    canvas.create_text(
        47.0,
        344.0,
        anchor="nw",
        text="Result",
        fill="#000000",
        font=("Inter Medium", 16 * -1,"bold"),
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        24.0,
        353.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        24.0,
        243.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        23.0,
        193.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        25.0,
        295.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        791.0,
        372.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        365.0,
        372.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        330.0,
        138.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        250.0,
        190.0,
        image=image_image_13
    )


    fig_current, ax_current = plt.subplots(figsize=(3.3, 2.1))
    canvas_current = FigureCanvasTkAgg(fig_current, master=window)
    canvas_current.draw()
    canvas_current.get_tk_widget().place(x=200, y=260)
    dataListCurrent = []
    ani_current = animation.FuncAnimation(fig_current, animateCurrent, frames=100,fargs=(ax_current, dataListCurrent), interval=500)

    fig_voltage, ax_voltage = plt.subplots(figsize=(3.3, 2.1))
    canvas_voltage = FigureCanvasTkAgg(fig_voltage, master=window)
    canvas_voltage.draw()
    canvas_voltage.get_tk_widget().place(x=625, y=260)
    dataListVoltage = []
    ani_voltage = animation.FuncAnimation(fig_voltage, animateVoltage, fargs=(ax_voltage, dataListVoltage), interval=500)

    vcmd = (window.register(validate_numeric_input), '%P')

    entry_numeric = Entry(window, 
                        bd=0, 
                        bg="#D9D9D9", 
                        highlightthickness=0, 
                        font=("Inter Medium", 18), 
                        validate='key', 
                        validatecommand=vcmd)
    entry_numeric.place(x=220, y=124, width=200, height=30)
    button = Button(window, text="Add current", command=lambda: Add_current(float(entry_numeric.get())), bg="#D9D9D9", bd=0)
    button.place(x=205, y=174, width=93, height=35)

    def on_closing():
        window.destroy()  # Destroy the main window
        window.quit()     # Quit the main loop

    window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing event

    window.mainloop()

if __name__ == "__main__":
    main()
