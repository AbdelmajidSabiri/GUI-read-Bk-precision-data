from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage,ttk, DoubleVar,Label,StringVar
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import sys
sys.path.append('C:\\Users\\dell\\GUI-read-Bk-precision-data')
from readData import Add_current, Bkp8600, Add_voltage



class GUI:

    ASSETS_PATH = Path(r"C:\Users\dell\GUI-read-Bk-precision-data\build\assets\frame0")
    def __init__(self):

        # Initialize BK Precision device and data lists
        self.bk_device = Bkp8600()
        self.bk_device.initialize()
        self.data_list_current = []
        self.data_list_voltage = []
        self.data_list_power = []
        self.max_power = 0.0
        self.MPP = {"Vmpp" : 0 , "Impp" : 0}

        # Create main window
        self.window = Tk()
        self.window.title("Agamine")
        self.window.geometry("1900x1500")
        self.window.configure(bg="#000000")

        # Create a notebook To Add tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=1, fill="both")

        # Create variables for displaying max power and other parameters
        self.max_power_var = DoubleVar()
        self.Vmpp_var = StringVar()
        self.Impp_var = StringVar()
        self.Isc_var = StringVar()
        self.Voc_var = StringVar()


       # Create tabs
        self.tab_edit = ttk.Frame(self.notebook)
        self.tab_display = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_edit, text='Edit')
        self.notebook.add(self.tab_display, text='Display')

        # Add functionality tabs
        self.setup_edit_tab()
        self.setup_display_tab()

        # Close window
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window closing event
        self.window.mainloop()

    # Method to create path to images
    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return GUI.ASSETS_PATH / Path(path)

    # Function to validate number input (accept only numbers)
    def validate_numeric_input(self, P, default=False):
        if P.isdigit() or P == "" or (default and P == "default"):
            return True
        return False

    # Function To get Max Power
    def GetMaxPower(self) :

        # Get current and voltage
        current, voltage = self.get_data()
        # Assign 0 to power if no data found
        if current and voltage :
            power = current * voltage
        else :
            power = 0

        # If other max power found, change the old one and return it
        if power > self.max_power:
            self.max_power = power

            # Take voltage and current of Max Power (Vmpp & Impp)
            self.MPP["Vmpp"] = voltage
            self.MPP["Impp"] = current
        return self.max_power,self.MPP

    # Keep updatign Max Power
    def update_max_power(self):
        # Update displayed maximum power and MPP values periodically
        max_power, MPP = self.GetMaxPower()

        #Format Values
        max_power_formatted = "{:.8f} W".format(max_power)
        Vmpp_formatted = "{:.8f} V".format(MPP["Vmpp"])
        Impp_formatted = "{:.8f} A".format(MPP["Impp"])
        
        #Assign Values to Variables
        self.max_power_var.set(max_power_formatted)
        self.Vmpp_var.set(Vmpp_formatted)
        self.Impp_var.set(Impp_formatted)

        # Calculate and Update Isc and Voc
        self.calculate_isc_voc()

        # Update every sec
        self.window.after(1000, self.update_max_power)


    #Function to calculate Isc and Voc
    def calculate_isc_voc(self):
        # Get Value of Isc if it found if not make it 0
        Isc_found = False
        for v, i in zip(self.data_list_voltage, self.data_list_current):
            if v == 0:
                self.Isc_var.set("{:.8f} A".format(i))
                Isc_found = True
                break
        if not Isc_found :
            self.Isc_var.set("0.00000000 A")


        # Get Value of Voc if it found if not make it 0
        Voc_found = False

        for v, i in zip(self.data_list_voltage, self.data_list_current):
            
            if i == 0:
                self.Voc_var.set("{:.8f} V".format(v))
                Voc_found = True
                break

        if not Voc_found :
            self.Voc_var.set("0.00000000 V")


    def setup_edit_tab(self):

        # Setup the edit tab
        canvas_edit = Canvas(
            self.tab_edit,
            bg="#000000",
            height=1000,
            width=1900,
            bd=0,
            highlightthickness=0,
            relief="ridge"
            
        )
        canvas_edit.pack(fill="both", expand=True)


        # Load and display images and text on the canvas
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        image_1 = canvas_edit.create_image(171.0, 36.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        image_2 = canvas_edit.create_image(950.0001220703125,67.5, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        image_3 = canvas_edit.create_image(125.0,533.0, image=self.image_image_3)

        canvas_edit.create_text(
            54.0,
            136.0,
            anchor="nw",
            text="Data",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        image_4 = canvas_edit.create_image(89.0,170.0, image=self.image_image_4)

        canvas_edit.create_text(
            62.0,
            205.0,
            anchor="nw",
            text="Control",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_edit.create_text(
            60.0,
            276.0,
            anchor="nw",
            text="Management",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_edit.create_text(
            60.0,
            352.0,
            anchor="nw",
            text = "State",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        image_5 = canvas_edit.create_image(30.0,137.0, image=self.image_image_5)

        canvas_edit.create_text(
            59.0,
            424.0,
            anchor="nw",
            text="Result",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold"),
        )

        canvas_edit.create_text(
            1160.0,
            125.0,
            anchor="nw",
            text="Max Power : ",
            fill="#FFFFFF",
            font=("Bold", 19 * -1)
        )

        canvas_edit.create_text(
            1210.0,
            250.0,
            anchor="nw",
            text="MPP : ",
            fill="#FFFFFF",
            font=("Bold", 19 * -1)
        )

        canvas_edit.create_text(
            1360.0,
            210.0,
            anchor="nw",
            text="Vmpp",
            fill="#FFFFFF",
            font=("Bold", 17 * -1)
        )
        canvas_edit.create_text(
            1660.0,
            210.0,
            anchor="nw",
            text="Impp",
            fill="#FFFFFF",
            font=("Bold", 17 * -1)
        )
        canvas_edit.create_text(
            1370.0,
            330.0,
            anchor="nw",
            text="Isc",
            fill="#FFFFFF",
            font=("Bold", 17 * -1)
        )
        canvas_edit.create_text(
            1670.0,
            330.0,
            anchor="nw",
            text="Voc",
            fill="#FFFFFF",
            font=("Bold", 17 * -1)
        )


        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        image_6 = canvas_edit.create_image(29.0,435.0, image=self.image_image_6)

        self.image_image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        image_7 = canvas_edit.create_image(30.0,285.0, image=self.image_image_7)

        self.image_image_8 = PhotoImage(file=self.relative_to_assets("image_8.png"))
        image_8 = canvas_edit.create_image(30.0,215.0, image=self.image_image_8)

        self.image_image_9 = PhotoImage(file=self.relative_to_assets("image_9.png"))
        image_9 = canvas_edit.create_image(29.0,360.0, image=self.image_image_9)

        self.image_image_12 = PhotoImage(file=self.relative_to_assets("image_12.png"))
        image_12 = canvas_edit.create_image(400.0, 138.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(730.0, 138.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(1400.0, 138.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(1400.0, 260.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(1700.0, 260.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(1400.0, 380.0, image=self.image_image_12)
        image_12 = canvas_edit.create_image(1700.0, 380.0, image=self.image_image_12)




        self.image_image_13 = PhotoImage(file=self.relative_to_assets("image_13.png"))
        image_13 = canvas_edit.create_image(320.0, 190.0, image=self.image_image_13)
        image_13_1 = canvas_edit.create_image(650.0, 190.0, image=self.image_image_13)

        # Setup entry fields and buttons for adding current and voltage
        vcmd = (self.window.register(self.validate_numeric_input), '%P')


        #Current
        self.entry_current = Entry(
            self.tab_edit,
            bd=0,
            bg="#D9D9D9",
            highlightthickness=0,
            font=("Inter Medium", 18),
            validate='key',
            validatecommand=vcmd
        )
        self.entry_current.place(x=290, y=124, width=200, height=30)
        self.button_current = Button(
            self.tab_edit,
            text="Add current",
            command=self.add_current,
            bg="#D9D9D9",
            bd=0
        )
        self.button_current.place(x=275, y=174, width=93, height=35)



        #Voltage
        self.entry_voltage = Entry(
            self.tab_edit,
            bd=0,
            bg="#D9D9D9",
            highlightthickness=0,
            font=("Inter Medium", 18),
            validate='key',
            validatecommand=vcmd
        )
        self.entry_voltage.place(x=620, y=124, width=200, height=30)
        self.button_voltage = Button(
            self.tab_edit,
            text="Add voltage",
            command=self.add_voltage,
            bg="#D9D9D9",
            bd=0
        )
        self.button_voltage.place(x=605, y=174, width=93, height=35)


        # Create labels to display calculated value 
        self.label_max_power_value = Label(
                self.tab_edit,
                textvariable=self.max_power_var,
                bg="#D9D9D9",
                fg="#D68102",
                font=("Inter Medium", 16)
            )
        self.label_max_power_value.place(x=1310, y=124)

        self.label_Vmpp_value = Label(
                self.tab_edit,
                textvariable=self.Vmpp_var,
                bg="#D9D9D9",
                fg="#D68102",
                font=("Inter Medium", 16)
            )
        self.label_Vmpp_value.place(x=1310, y=246)

        self.label_Impp_value = Label(
                self.tab_edit,
                textvariable=self.Impp_var,
                bg="#D9D9D9",
                fg="#D68102",
                font=("Inter Medium", 16)
            )
        self.label_Impp_value.place(x=1605, y=246)

        
        self.label_Isc_value = Label(
                self.tab_edit,
                textvariable=self.Isc_var,
                bg="#D9D9D9",
                fg="#D68102",
                font=("Inter Medium", 16)
            )
        self.label_Isc_value.place(x=1310, y=367)

        self.label_Voc_value = Label(
                self.tab_edit,
                textvariable=self.Voc_var,
                bg="#D9D9D9",
                fg="#D68102",
                font=("Inter Medium", 16)
            )
        self.label_Voc_value.place(x=1605, y=367)

        # Start updating maximum power and MPP values
        self.update_max_power()
            

    def setup_display_tab(self):

        # Setup UI components for the 'Display' tab
        canvas_display = Canvas(
            self.tab_display,
            bg="#000000",
            height=1000,
            width=1900,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas_display.pack(fill="both", expand=True)



        # Load and place images and text labels on the canvas
        self.image_image_10 = PhotoImage(file=self.relative_to_assets("image_10.png"))
        self.image_image_11 = PhotoImage(file=self.relative_to_assets("image_11.png"))
        self.image_image_14 = PhotoImage(file=self.relative_to_assets("image_14.png"))

        image_1_1 = canvas_display.create_image(171.0, 36.0, image=self.image_image_1)
        image_2_1 = canvas_display.create_image(950.0001220703125,67.5, image=self.image_image_2)
        image_3_1 = canvas_display.create_image(125.0,533.0, image=self.image_image_3)

        canvas_display.create_text(
            54.0,
            136.0,
            anchor="nw",
            text="Data",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        image_4_1 = canvas_display.create_image(89.0,170.0, image=self.image_image_4)
        canvas_display.create_text(
            62.0,
            205.0,
            anchor="nw",
            text="Control",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_display.create_text(
            60.0,
            276.0,
            anchor="nw",
            text="Management",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        canvas_display.create_text(
            60.0,
            352.0,
            anchor="nw",
            text="State",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold")
        )

        image_5_1 = canvas_display.create_image(30.0,137.0, image=self.image_image_5)
        canvas_display.create_text(
            59.0,
            424.0,
            anchor="nw",
            text="Result",
            fill="#000000",
            font=("Inter Medium", 16 * -1, "bold"),
        )

        canvas_display.create_text(
            550.0,
            98.0,
            anchor="nw",
            text="Current Variation",
            fill="#FFFFFF",
            font=("Inter Bold", 27 * -1)
        )

        canvas_display.create_text(
            550.0,
            533.0,
            anchor="nw",
            text="Power Variation",
            fill="#FFFFFF",
            font=("Inter Bold", 27 * -1)
        )

        canvas_display.create_text(
            1326.0,
            98.0,
            anchor="nw",
            text="Voltage Variation",
            fill="#FFFFFF",
            font=("Inter Bold", 27 * -1)
        )
        
        canvas_display.create_text(
            1326.0,
            533.0,
            anchor="nw",
            text="Combined Chart",
            fill="#FFFFFF",
            font=("Inter Bold", 27 * -1)
        )

        image_6_1 = canvas_display.create_image(29.0,435.0, image=self.image_image_6)
        image_7_1 = canvas_display.create_image(30.0,285.0, image=self.image_image_7)
        image_8_1 = canvas_display.create_image(30.0,215.0, image=self.image_image_8)
        image_9_1 = canvas_display.create_image(29.0,360.0, image=self.image_image_9)
        image_10_1 = canvas_display.create_image(669.0,318.0, image=self.image_image_10)
        image_11_1 = canvas_display.create_image(669.0,753.0, image=self.image_image_11)
        image_14 =canvas_display.create_image(1445.0,318.0,image=self.image_image_14)
        image_15 = canvas_display.create_image(1445.0, 753.0, image = self.image_image_11)



        # Setup animated plots using Matplotlib and add them to the canvas
        fig_current, ax_current = plt.subplots(figsize=(5, 3))
        canvas_current = FigureCanvasTkAgg(fig_current, master=self.tab_display)
        canvas_current.draw()
        canvas_current.get_tk_widget().place(x=420, y=170)
        self.ani_current = animation.FuncAnimation(
            fig_current,
            self.animate_current,
            fargs=(ax_current,),
            interval=00
        )

        fig_voltage, ax_voltage = plt.subplots(figsize=(5, 3))
        canvas_voltage = FigureCanvasTkAgg(fig_voltage, master=self.tab_display)
        canvas_voltage.draw()
        canvas_voltage.get_tk_widget().place(x=1195, y=170)
        self.ani_voltage = animation.FuncAnimation(
            fig_voltage,
            self.animate_voltage,
            fargs=(ax_voltage,),
            interval=100
        )

        fig_power, ax_power = plt.subplots(figsize=(5, 3))
        canvas_power = FigureCanvasTkAgg(fig_power, master=self.tab_display)
        canvas_power.draw()
        canvas_power.get_tk_widget().place(x=420, y=600)
        self.ani_power = animation.FuncAnimation(
            fig_power,
            self.animate_power,
            fargs=(ax_power,),
            interval=100
        )

        fig_combined, ax_combined = plt.subplots(figsize=(5, 3))
        canvas_combined = FigureCanvasTkAgg(fig_combined, master=self.tab_display)
        canvas_combined.draw()
        canvas_combined.get_tk_widget().place(x=1195, y=600)
        self.ani_combined = animation.FuncAnimation(
            fig_combined,
            self.animate_combined,
            fargs=(ax_combined,),
            interval=100
        )


    # Method to Take current and voltage data from the BK Precision device
    def get_data(self):
        try:
            measured_current = self.bk_device.get_current()
            voltage = self.bk_device.get_voltage()
            return measured_current, voltage
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return 0.0, 0.0

    # Animation function for updating current plot
    def animate_current(self, i, ax):
        current, _ = self.get_data()
        self.data_list_current.append(current)
        self.data_list_current = self.data_list_current[-50:]  # Limit to the last 50 data points
        ax.clear()
        ax.plot(self.data_list_current)
        ax.set_ylim([0.0001, 0.003])


    # Animation function for updating Voltage plot
    def animate_voltage(self, i, ax):
        _, voltage = self.get_data()
        self.data_list_voltage.append(voltage)
        self.data_list_voltage = self.data_list_voltage[-50:]  # Limit to the last 50 data points
        ax.clear()
        ax.plot(self.data_list_voltage)
        ax.set_ylim([0, 20])


    # Animation function for updating Power plot
    def animate_power(self,i,ax) :
        current, voltage = self.get_data()
        power = current * voltage
        self.data_list_power.append(power)
        self.data_list_power = self.data_list_power[-50:]  # Limit to the last 50 data points
        ax.clear()
        ax.plot(self.data_list_power)
        ax.set_ylim([0, 0.000005])


    # Animation function for updating Combined (current & voltage) plot
    def animate_combined(self, i, ax):
        current, voltage = self.get_data()
        self.data_list_current.append(current)
        self.data_list_voltage.append(voltage)
        self.data_list_current = self.data_list_current[-50:]  # Limit to the last 50 data points
        self.data_list_voltage = self.data_list_voltage[-50:]  # Limit to the last 50 data points
        ax.clear()
        ax.plot(self.data_list_current, label='Current')
        ax.plot(self.data_list_voltage, label='Voltage')
        ax.legend()
        ax.set_ylim([0, 20]) 


    # Method to add current data to the list
    def add_current(self):
        try:
            current_value = float(self.entry_current.get())
            self.bk_device.set_current(current_value)
            Add_current(current_value)  # Update the Excel file
        except ValueError:
            print("Invalid current value entered.")

    # Method to add voltage data to the list
    def add_voltage(self):
        try:
            voltage_value = float(self.entry_voltage.get())
            self.bk_device.set_voltage(voltage_value)
            Add_voltage(voltage_value)
        except ValueError:
            print("Invalid voltage value entered.")

    #Function of closing window
    def on_closing(self):
        self.bk_device.reset_to_manual()
        self.window.destroy()
        self.window.quit()

# Instantiate the GUI class to start the application
if __name__ == "__main__":
    GUI()
