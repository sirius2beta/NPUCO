import tkinter as tk
import time
import threading

def count():
    while(True):
        if(var_close):
            break
        measured_value_set[0] = measured_value_set[0] + 1
        time.sleep(1) 

def close():
    global var_close
    var_close = True
    print("Exiting the program.")
    root.destroy()

    
def update_labels():
    for i in range(len(measured_value_set)):
        parameter_name = parameter_names[i]
        measured_value = "{:.4f}".format(measured_value_set[i])
        label_texts[i].set(f"{parameter_name} = {measured_value}")
    root.after(1000, update_labels)

parameter_names = [
    "temperature",
    "pressure",
    "depth",
    "level_depth_to_water",
    "level_surface_elevation",
    "actual_conductivity",
    "specific_conductivity",
    "resistivity",
    "salinity",
    "total_dissolved_solids",
    "density_of_water",
    "barometric_pressure",
    "pH",
    "pH_mv",
    "orp",
    "dissolved_oxygen_concentration",
    "dissolved_oxygen_percent_saturation",
    "chloride",
    "turbidity",
    "oxygen_partial_pressure",
    "total_suspended_solids",
    "external_voltage",
    "battery_capacity_remaining",
    "rhodamine_wt_concentration"
]
measured_value_set = [0] * 24
var_close = False

t = threading.Thread(target = count)
t.start()

root = tk.Tk()
root.title("Sensor Reader")
root.protocol("WM_DELETE_WINDOW", close)

label_texts = [] 
for i in range(len(measured_value_set)):
    text_var = tk.StringVar()
    label_texts.append(text_var)
    
    label = tk.Label(root, textvariable = text_var,
                    width=50, height=8, bg="#BEBEBE",
                    anchor="w", bd=1, relief="solid",
                    justify="center" ) 
    label.grid(row=i // 4, column=i % 4)

update_labels()

root.mainloop()