import pyvisa
import time

class Bkp8600(object):
    def __init__(self, resource=None):
        self.rm = pyvisa.ResourceManager()
        if resource:
            self.instr = self.rm.open_resource(resource,timeout=10000)
        else:
            # Find the first BK Precision instrument
            instruments = self.rm.list_resources()
            for r in instruments:
                try:
                    instr = self.rm.open_resource(r)
                    if instr.query("*IDN?").startswith("B&K Precision"):
                        self.instr = instr
                        break
                except pyvisa.VisaIOError:
                    pass
            else:
                raise RuntimeError("No BK Precision instrument found.")

    def get_description(self):
        return self.instr.query("*IDN?")

    def get_current(self):
        return float(self.instr.query(":MEASure:CURRent?"))

    def get_voltage(self):
        return float(self.instr.query(":MEASure:VOLTage?"))
    
    def get_resistance(self):
        return float(self.instr.query(":MEASure:RESistance?"))

    def get_power(self):
        return float(self.instr.query(":MEASure:POWer?"))

    def initialize(self):
        self.instr.write("SYSTem:REMote")
        self.instr.write("INPut OFF")
        self.instr.write("*RST")
        self.instr.write("*CLS")
        self.instr.write("*SRE 0")
        self.instr.write("*ESE 0")

    def set_current(self, current):
        self.instr.write("INPut ON")
        self.instr.write(f"CURRent {current}")

    def reset_to_manual(self):
        self.instr.write("INPut OFF")
        self.instr.write("SYSTem:LOCal")

        
if __name__ == '__main__':
    try:
        last = Bkp8600()

        last.initialize()

        # Perform operations (e.g., setting current and measuring values)
        for n in range(0, 200):
            current_value = n / 100.0
            print(f"Setting current to: {current_value} A")
            last.set_current(current_value)
            time.sleep(1)
            print(f"Current: {last.get_current()} A")
            print(f"Voltage: {last.get_voltage()} V")



    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Reset to local mode and close the connection
        last.reset_to_manual()
        del last
