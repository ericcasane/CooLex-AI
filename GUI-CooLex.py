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


robot = CooLex_Robot.CooLex() # Create a new instance of the robot
dispenser = CooLex_Dispenser.DispenserAgent() # Create a new instance of the dispenser

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


def clear_screen():
    for widget in app.winfo_children():
        widget.destroy()


def create_order_page():
    clear_screen()
    title_label()
    ctk.CTkLabel(app, text="Escull la base").pack()
    base_option = (create_segmented_button(app, base_ingredients, True))
    base_option.pack()

    ctk.CTkLabel(app, text="Escull la proteïna").pack()
    protein_option = create_segmented_button(app, protein_ingredients)
    protein_option.pack()

    ctk.CTkLabel(app, text="Escull els toppings (3 a escollir)").pack()
    toppings_frame = tk.Frame(app, bg="#242424")  # Create a new frame to hold the topping options
    toppings_frame.pack()

    topping_options = []
    for i in range(3):
        topping_option = create_segmented_button(toppings_frame, toppings)
        topping_option.grid(row=0, column=i, padx=5)  # Place the option in the grid
        topping_options.append(topping_option)

    ctk.CTkLabel(app, text="Escull la salsa").pack()
    sauce_option = create_segmented_button(app, sauces)
    sauce_option.pack()

    button = ctk.CTkButton(app, text="Realitzar comanda",
                           command=lambda: process_order_and_show_info(base_option, protein_option, topping_options,
                                                                       sauce_option))
    button.configure(font=("Arial", 16), fg_color="green", hover_color="dark green")
    button.pack(pady=20)


def process_order_and_show_info(base_option, protein_option, topping_options, sauce_option):
    # Get the index of the selected option
    def get_selected_index(ingredients, selected_option):
        return next(i for i, v in enumerate(ingredients) if v.name == selected_option.get())

    base_index = get_selected_index(base_ingredients, base_option)
    protein_index = get_selected_index(protein_ingredients, protein_option)
    topping_indices = [get_selected_index(toppings, topping_option) for topping_option in topping_options]
    sauce_index = get_selected_index(sauces, sauce_option)
    print("Base:", base_index, "Protein:", protein_index, "Toppings:", topping_indices, "Sauce:", sauce_index)

    order_info = robot.process_order(base_index, protein_index, topping_indices, sauce_index)

    clear_screen()
    title_label()
    ctk.CTkLabel(app, text="Comanda completada amb èxit!", font=("Arial", 20)).pack(pady=20)
    ctk.CTkLabel(app, text="Ordre dels ingredients afegits:").pack()
    for i in range(len(order_info)):
        info_label = ctk.CTkLabel(app, text=str(i+1) + ". " + order_info[i])
        info_label.pack()

    new_order_button = ctk.CTkButton(app, text="Nova Comanda", command=create_order_page)
    new_order_button.configure(font=("Arial", 16), fg_color="green", hover_color="dark green")
    new_order_button.pack(pady=20)


# Call the function to create the order page
create_order_page()
# Start the main loop
app.mainloop()
