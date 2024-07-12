from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage,ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
sys.path.append('C:\\Users\\dell\\GUI-read-Bk-precision-data')
from readData import Add_current, Bkp8600, Add_voltage



class GUI:

    ASSETS_PATH = Path(r"C:\Users\dell\GUI-read-Bk-precision-data\build\assets\frame0")
    def __init__(self):
        self.bk_device = Bkp8600()
        self.bk_device.initialize()
        self.data_list_current = []
        self.data_list_voltage = []

        self.window = Tk()
        self.window.title("Agamine")
        self.window.geometry("1000x550")
        self.window.configure(bg="#000000")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=1, fill="both")

        self.tab_edit = ttk.Frame(self.notebook)
        self.tab_display = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_edit, text='Edit')
        self.notebook.add(self.tab_display, text='Display')

        self.setup_edit_tab()
        self.setup_display_tab()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window closing event
        self.window.mainloop()

    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return GUI.ASSETS_PATH / Path(path)

    def validate_numeric_input(self, P, default=False):
        if P.isdigit() or P == "" or (default and P == "default"):
            return True
        return False

    def setup_edit_tab(self):
        canvas_edit = Canvas(
            self.tab_edit,
            bg="#000000",
            height=550,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas_edit.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        image_1 = canvas_edit.create_image(171.0, 36.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        image_2 = canvas_edit.create_image(499.0, 70.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        image_3 = canvas_edit.create_image(78.0, 308.0, image=self.image_image_3)

        canvas_edit.create_text(
            48.0,
            118.0,
            anchor="nw",
            text="Data",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        image_4 = canvas_edit.create_image(64.0, 160.0, image=self.image_image_4)

        canvas_edit.create_text(
            46.0,
            185.0,
            anchor="nw",
            text="Control",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_edit.create_text(
            47.0,
            236.0,
            anchor="nw",
            text="Management",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_edit.create_text(
            47.0,
            290.0,
            anchor="nw",
            text = "State",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        image_5 = canvas_edit.create_image(23.0, 127.0, image=self.image_image_5)

        canvas_edit.create_text(
            47.0,
            344.0,
            anchor="nw",
            text="Result",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold"),
        )

        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        image_6 = canvas_edit.create_image(24.0, 353.0, image=self.image_image_6)

        self.image_image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        image_7 = canvas_edit.create_image(24.0, 243.0, image=self.image_image_7)

        self.image_image_8 = PhotoImage(file=self.relative_to_assets("image_8.png"))
        image_8 = canvas_edit.create_image(23.0, 193.0, image=self.image_image_8)

        self.image_image_9 = PhotoImage(file=self.relative_to_assets("image_9.png"))
        image_9 = canvas_edit.create_image(25.0, 295.0, image=self.image_image_9)

        self.image_image_12 = PhotoImage(file=self.relative_to_assets("image_12.png"))
        image_12 = canvas_edit.create_image(330.0, 138.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(660.0, 138.0, image=self.image_image_12)

        self.image_image_13 = PhotoImage(file=self.relative_to_assets("image_13.png"))
        image_13 = canvas_edit.create_image(250.0, 190.0, image=self.image_image_13)
        image_13_1 = canvas_edit.create_image(580.0, 190.0, image=self.image_image_13)

        vcmd = (self.window.register(self.validate_numeric_input), '%P')

        self.entry_current = Entry(
            self.tab_edit,
            bd=0,
            bg="#D9D9D9",
            highlightthickness=0,
            font=("Inter Medium", 18),
            validate='key',
            validatecommand=vcmd
        )
        self.entry_current.place(x=220, y=124, width=200, height=30)
        self.button_current = Button(
            self.tab_edit,
            text="Add current",
            command=self.add_current,
            bg="#D9D9D9",
            bd=0
        )
        self.button_current.place(x=205, y=174, width=93, height=35)

        self.entry_voltage = Entry(
            self.tab_edit,
            bd=0,
            bg="#D9D9D9",
            highlightthickness=0,
            font=("Inter Medium", 18),
            validate='key',
            validatecommand=vcmd
        )
        self.entry_voltage.place(x=550, y=124, width=200, height=30)
        self.button_voltage = Button(
            self.tab_edit,
            text="Add voltage",
            command=self.add_voltage,
            bg="#D9D9D9",
            bd=0
        )
        self.button_voltage.place(x=535, y=174, width=93, height=35)

    def setup_display_tab(self):
        canvas_display = Canvas(
            self.tab_display,
            bg="#000000",
            height=550,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        
        canvas_display.place(x=0, y=0)

        self.image_image_10 = PhotoImage(file=self.relative_to_assets("image_10.png"))
        self.image_image_11 = PhotoImage(file=self.relative_to_assets("image_11.png"))

        image_1_1 = canvas_display.create_image(171.0, 36.0, image=self.image_image_1)
        image_2_1 = canvas_display.create_image(499.0, 70.0, image=self.image_image_2)
        image_3_1 = canvas_display.create_image(78.0, 308.0, image=self.image_image_3)
        canvas_display.create_text(
            48.0,
            118.0,
            anchor="nw",
            text="Data",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        image_4_1 = canvas_display.create_image(64.0, 160.0, image=self.image_image_4)
        canvas_display.create_text(
            46.0,
            185.0,
            anchor="nw",
            text="Control",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_display.create_text(
            47.0,
            236.0,
            anchor="nw",
            text="Management",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_display.create_text(
            47.0,
            290.0,
            anchor="nw",
            text="State",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        image_5_1 = canvas_display.create_image(23.0, 127.0, image=self.image_image_5)
        canvas_display.create_text(
            47.0,
            344.0,
            anchor="nw",
            text="Result",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold"),
        )

        image_6_1 = canvas_display.create_image(24.0, 353.0, image=self.image_image_6)
        image_7_1 = canvas_display.create_image(24.0, 243.0, image=self.image_image_7)
        image_8_1 = canvas_display.create_image(23.0, 193.0, image=self.image_image_8)
        image_9_1 = canvas_display.create_image(25.0, 295.0, image=self.image_image_9)

        image_image_10 = PhotoImage(file=self.relative_to_assets("image_10.png"))
        image_10_1 = canvas_display.create_image(791.0, 372.0, image=self.image_image_10)

        image_image_11 = PhotoImage(file=self.relative_to_assets("image_11.png"))
        image_11_1 = canvas_display.create_image(365.0, 372.0, image=self.image_image_11)

        fig_current, ax_current = plt.subplots(figsize=(3.3, 2.1))
        canvas_current = FigureCanvasTkAgg(fig_current, master=self.tab_display)
        canvas_current.draw()
        canvas_current.get_tk_widget().place(x=200, y=260)
        self.ani_current = animation.FuncAnimation(
            fig_current,
            self.animate_current,
            fargs=(ax_current,),
            interval=500
        )

        fig_voltage, ax_voltage = plt.subplots(figsize=(3.3, 2.1))
        canvas_voltage = FigureCanvasTkAgg(fig_voltage, master=self.tab_display)
        canvas_voltage.draw()
        canvas_voltage.get_tk_widget().place(x=625, y=260)
        self.ani_voltage = animation.FuncAnimation(
            fig_voltage,
            self.animate_voltage,
            fargs=(ax_voltage,),
            interval=500
        )

    def get_data(self):
        try:
            measured_current = self.bk_device.get_current()
            voltage = self.bk_device.get_voltage()
            return measured_current, voltage
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return 0.0, 0.0

    def animate_current(self, i, ax):
        current, _ = self.get_data()
        self.data_list_current.append(current)
        self.data_list_current = self.data_list_current[-50:]  # Limit to the last 50 data points
        ax.clear()
        ax.plot(self.data_list_current)
        ax.set_ylim([0.0001, 0.001])
        ax.set_title("Current Change")
        ax.set_ylabel("Current Value")

    def animate_voltage(self, i, ax):
        _, voltage = self.get_data()
        self.data_list_voltage.append(voltage)
        self.data_list_voltage = self.data_list_voltage[-50:]  # Limit to the last 50 data points
        ax.clear()
        ax.plot(self.data_list_voltage)
        ax.set_ylim([0, 0.005])
        ax.set_title("Voltage Change")
        ax.set_ylabel("Voltage Value")

    def add_current(self):
        try:
            current_value = float(self.entry_current.get())
            self.bk_device.set_current(current_value)
            Add_current(current_value)  # Update the Excel file
        except ValueError:
            print("Invalid current value entered.")

    def add_voltage(self):
        try:
            voltage_value = float(self.entry_voltage.get())
            self.bk_device.set_voltage(voltage_value)
            Add_voltage(voltage_value)  # Update the Excel file
        except ValueError:
            print("Invalid voltage value entered.")

    def on_closing(self):
        self.bk_device.reset_to_manual()
        self.window.destroy()
        self.window.quit()

if __name__ == "__main__":
    GUI()
