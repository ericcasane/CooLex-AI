import tkinter as tk
import customtkinter as ctk

import CooLex_Dispenser
import CooLex_Robot
ctk.set_appearance_mode("dark")  # Set the appearance mode to dark

app = ctk.CTk()  # Create the main window
app.geometry("600x450")  # Set the size of the window
app.title("CooLex - The Bowl Robot")  # Set the title of the window


def title_label():
    label = ctk.CTkLabel(app, text="CooLex - The Bowl Robot", font=("Helvetica", 30, "bold"))  # Create a label
    label.pack(pady=20)  # Add padding on the top and bottom


dispenser = CooLex_Dispenser.DispenserAgent() # Create a new instance of the dispenser
robot = CooLex_Robot.CooLex(dispenser) # Create a new instance of the robot

# Get the ingredients from the dispenser
base_ingredients = dispenser.get_base_ingredients()
protein_ingredients = dispenser.get_protein_ingredients()
toppings = dispenser.get_toppings()
sauces = dispenser.get_sauces()


# Create a segmented button with the given options
def create_segmented_button(parent, options, SegmentedButton=False):
    if SegmentedButton:
        segmented_button = ctk.CTkSegmentedButton(parent, values=[option.name for option in options])
    else:
        segmented_button = ctk.CTkOptionMenu(parent, values=[option.name for option in options])
    segmented_button.set(options[0].name)  # Set the default value
    return segmented_button


def clear_screen():  # Function to clear the screen
    for widget in app.winfo_children():  # Iterate over all the widgets in the window and destroy them
        widget.destroy()


def create_order_page():  # Function to create the order page
    clear_screen()  # Clear the screen
    title_label()  # Add the title label
    ctk.CTkLabel(app, text="Escull la base").pack()  # Add a label for the base ingredients
    base_option = (create_segmented_button(app, base_ingredients, True))  # Create a segmented button for the base ingredients
    base_option.pack()  # Add the segmented button to the window

    ctk.CTkLabel(app, text="Escull la proteïna").pack()  # Add a label for the protein ingredients
    protein_option = create_segmented_button(app, protein_ingredients)  # Create an option menu for the protein ingredients
    protein_option.pack()  # Add the option menu to the window

    ctk.CTkLabel(app, text="Escull els toppings (3 a escollir)").pack()  # Add a label for the toppings
    toppings_frame = tk.Frame(app, bg="#242424")  # Create a new frame to hold the topping options
    toppings_frame.pack()  # Add the frame to the window

    topping_options = []
    for i in range(3):  # Create 3 segmented buttons for the toppings
        topping_option = create_segmented_button(toppings_frame, toppings)  # Create a segmented button for the toppings
        topping_option.grid(row=0, column=i, padx=5)  # Place the option in the grid
        topping_options.append(topping_option)  # Add the option to the list

    ctk.CTkLabel(app, text="Escull la salsa").pack()  # Add a label for the sauces
    sauce_option = create_segmented_button(app, sauces)  # Create an option menu for the sauces
    sauce_option.pack()  # Add the option menu to the window

    # Create a button to process the order that calls the process_order_and_show_info function on click
    button = ctk.CTkButton(app, text="Realitzar comanda",
                           command=lambda: process_order_and_show_info(base_option, protein_option, topping_options,
                                                                       sauce_option))
    button.configure(font=("Arial", 16), fg_color="green", hover_color="dark green")
    button.pack(pady=20)


# Function to process the order and show the information
def process_order_and_show_info(base_option, protein_option, topping_options, sauce_option):
    # Get the index of the selected option
    def get_selected_index(ingredients, selected_option):
        return next(i for i, v in enumerate(ingredients) if v.name == selected_option.get())

    # Get the index of the selected options
    base_index = get_selected_index(base_ingredients, base_option)
    protein_index = get_selected_index(protein_ingredients, protein_option)
    topping_indices = [get_selected_index(toppings, topping_option) for topping_option in topping_options]
    sauce_index = get_selected_index(sauces, sauce_option)

    # Process the order to the robot agent and get the order of actions done
    order_info = robot.process_order(base_index, protein_index, topping_indices, sauce_index)

    clear_screen()
    title_label()
    ctk.CTkLabel(app, text="Comanda completada amb èxit!", font=("Arial", 20)).pack(pady=20)
    ctk.CTkLabel(app, text="Ordre de la prepaparió del bowl:").pack()
    for i in range(len(order_info)):  # Display the order of actions numbered
        info_label = ctk.CTkLabel(app, text=str(i+1) + ". " + order_info[i])
        info_label.pack()

    new_order_button = ctk.CTkButton(app, text="Nova Comanda", command=create_order_page)  # Create a button to place a new order
    new_order_button.configure(font=("Arial", 16), fg_color="green", hover_color="dark green")
    new_order_button.pack(pady=20)


# Call the function to create the order page
create_order_page()
# Start the main loop
app.mainloop()