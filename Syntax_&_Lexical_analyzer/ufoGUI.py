import tkinter
from tkinter import ttk
from tkinter import *
from turtle import shape
from data_structures import filter_events_list_by_shape, filter_events_list_by_state, get_stats_for_all_states, state_list, shape_list
import ufolex as ufo

# Imports for plots
import matplotlib, numpy
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Main window
window = tkinter.Tk()
#window.geometry("750x400")
window.title("UFO Sightings")
frame = tkinter.Frame(window)
frame.pack()

# Sightings Frame
event_info_frame = tkinter.LabelFrame(frame, text="UFO sighting events")
event_info_frame.grid(row=0, column=0)

#myscrollbar=Scrollbar(event_table_frame,orient="vertical")
#myscrollbar.pack(side="right",fill="y")

# State filter
#Paso los keys del diccionario
statesList = list(ufo.data_structures.state_list.keys())
states_label = tkinter.Label(event_info_frame, text="State")
state_selected = tkinter.StringVar()
states_combobox = ttk.Combobox(event_info_frame, state="readonly", values=[""], textvariable=state_selected)
for index in range(len(statesList)):
    if statesList[index] not in states_combobox['values']: 
        states_combobox['values'] += (statesList[index],)

states_label.grid(row=0, column=0)
states_combobox.grid(row=1, column=0)

# Shape filter
shapesList = list(ufo.data_structures.shape_list.keys())
shapes_label = tkinter.Label(event_info_frame, text="Shape")
shape_selected = tkinter.StringVar()
shapes_combobox = ttk.Combobox(event_info_frame, values=[""], textvariable=shape_selected, state="readonly")
for index in range(len(shapesList)):
    if shapesList[index] not in shapes_combobox['values']: 
        shapes_combobox['values'] += (shapesList[index],)

shapes_label.grid(row=0, column=1)
shapes_combobox.grid(row=1, column=1)

# Next sighting prediction
stats_list = list(ufo.data_structures.get_stats_for_all_states().keys())
prediction_label = tkinter.Label(event_info_frame, text="Predicted next sighting")
# TODO: Get prediction from ufolex.
prediction_entry = tkinter.Entry(event_info_frame)
#prediction_entry.configure(state='normal')
#prediction_entry.insert('end', ufo.data_structures.get_stats_for_all_states()[states_combobox.get()])
#prediction_entry.configure(state='disabled')
prediction_label.grid(row=0, column=2)
prediction_entry.grid(row=1, column=2)


# Events info
# Sightings Frame
event_table_frame = tkinter.LabelFrame(frame, text="Event Details")
event_table_frame.grid(row=3, column=0)

sightings_info_label = tkinter.Label(event_info_frame, text="Sightings info")
sightings_elements = ['Link', 'Date', 'Time', 'City', 'State', 'Country', 'Shape', 'Duration', 'Summary', 'Posted', 'Images']

#Ejemplo de vista                            1                                   2         3         4          5        6       7        8                          9                           10       11
#sightings_list = ['https://nuforc.org/webreports/reports/168/S168773.html', '6/19/22', '01:20', 'Cordova', 'ALABAMA', 'USA', 'Light', '10 min', 'Bright object with light ring trailing it', '6/22/22', 'Yes',
#                  'https://nuforc.org/webreports/reports/168/S168673.html', '6/14/22', '20:35', 'Guntersville', 'ALABAMA', 'USA', 'Light', 'About 70 minutes', 'A sphere/ball of light hovering above the water.', '6/22/22', 'Yes']

sightings_list = (ufo.data_structures.event_list)

# for every element in event.
def filter(self):
    # Remove old table content
    for widgets in event_table_frame.winfo_children():
        widgets.destroy()

    # No filter
    if (states_combobox.get() == '' and shapes_combobox.get() == ''):
        for i in range(int(len(sightings_elements))):
            e = tkinter.Label(event_table_frame, text = sightings_elements[i])
            e.grid(row=3, column=i)

        for i in range(int(len(sightings_list)/11)):
            for j in range(11):
                e = tkinter.Entry(event_table_frame)
                e.grid(row=i+4, column=j)
                e.insert('end', sightings_list[i*11+j])
                e.configure(state='disabled')
        filtered_list = sightings_list

    # filtered
    filtered_list = sightings_list
    if (not states_combobox.get() == ''):
        filtered_list = filter_events_list_by_state(states_combobox.get(), filtered_list)
        prediction_entry.configure(state='normal')
        prediction_entry.delete(0, 'end')
        prediction_entry.insert('0', (ufo.data_structures.get_stats_for_all_states()[states_combobox.get()], '%'))
        prediction_entry.configure(state='disabled')
    if (not shapes_combobox.get() == ''):
        filtered_list = filter_events_list_by_shape(shapes_combobox.get(), filtered_list)

    for i in range(int(len(sightings_elements))):
        e = tkinter.Label(event_table_frame, text =  sightings_elements[i])
        e.grid(row=3, column=i)

    for i in range(int(len(filtered_list)/11)):
        for j in range(11):
            e = tkinter.Entry(event_table_frame)
            e.grid(row=i+4, column=j)
            e.insert('end', filtered_list[i*11+j])
            e.configure(state='disabled')
states_combobox.bind('<<ComboboxSelected>>', filter)
shapes_combobox.bind('<<ComboboxSelected>>', filter)

for i in range(int(len(sightings_elements))):
    e = tkinter.Label(event_table_frame, text = sightings_elements[i])
    e.grid(row=3, column=i)

for i in range(int(len(sightings_list)/11)):
    for j in range(11):
        e = tkinter.Entry(event_table_frame)
        e.grid(row=i+4, column=j)
        e.insert('end', sightings_list[i*11+j])
        e.configure(state='disabled')
sightings_info_label.grid(row=2, column=0)

# Plots
def state_plot():
    # Display this plot in a new window with full screen.
    state_plot_window = tkinter.Toplevel()
    state_plot_window.title("State plot")
    # Make the window full screen
    state_plot_window.geometry("950x600")
    state_plot_window.resizable(True, True)

    f = Figure(figsize=(5,4), dpi=100)
    ax = f.add_subplot(111)

    data = state_list
    states = data.keys()
    values = data.values()

    ax.bar(states, values)
    ax.set_title('Sightings per state')

    length = len(states)
    ind = numpy.arange(length)  # the x locations for the groups
    width = .64

    # Reduce the height of the plot
    f.subplots_adjust(bottom=0.5)

    ax.set_xticks(ind + width / 1.5)
    ax.set_xticklabels(states, rotation=90)

    canvas = FigureCanvasTkAgg(f, master=state_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def shape_plot():
    # Display this plot in a new window with full screen.
    shape_plot_window = tkinter.Toplevel()
    shape_plot_window.title("Shape plot")
    # Make the window full screen
    shape_plot_window.geometry("950x600")
    shape_plot_window.resizable(True, True)

    f = Figure(figsize=(5,4), dpi=100)
    ax = f.add_subplot(111)

    data = shape_list
    shapes = data.keys()
    values = data.values()

    ax.bar(shapes, values)
    ax.set_title('Sightings per shape')

    # Count elements in shapes
    length = len(shapes)
    ind = numpy.arange(length)  # the x locations for the groups
    width = .64

    # Reduce the height of the plot
    f.subplots_adjust(bottom=0.5)

    ax.set_xticks(ind + width / 1.5)
    ax.set_xticklabels(shapes, rotation=90)

    canvas = FigureCanvasTkAgg(f, master=shape_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# Create a button to show the plot on new window and bind it to the function state_plot
plot_button = tkinter.Button(event_info_frame, text="State Plot", command=state_plot)
plot_button.grid(row=3, column=0)

plot_button = tkinter.Button(event_info_frame, text="Shapes Plot", command=shape_plot)
plot_button.grid(row=3, column=1)

# TODO: Move to main file (ufolex)
window.mainloop()
