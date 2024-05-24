# CooLex - The Bowl Robot

CooLex is a system consisting of a robotic arm, an ingredient dispenser, and a user interface for processing custom bowl orders. The project is implemented in Python and utilizes the A* search algorithm to find the optimal sequence of actions for the robotic arm to follow in preparing the bowls.

## General Description

The system consists of three main components:

1. **Dispenser Agent (DispenserAgent):** Manages the dispensers for ingredients and bowls, providing methods to retrieve each type of ingredient.

2. **Robotic Agent (CooLex):** Processes incoming orders, calculates the optimal sequence of actions using the A* algorithm, and controls the movement of the robotic arm to prepare the bowls.

3. **User Interface (GUI):** Provides a graphical user interface for placing bowl orders, allowing users to select the desired base, protein, toppings, and sauce.

## Installation

1. Clone this repository to your local machine.
2. Ensure you have Python 3.x installed, along with the following libraries:
- aima3
- customtkinter

You can install the required libraries by running:
pip install aima3 customtkinter

## Usage

1. Run the `GUI_CooLex.py` file to start the user interface.
2. In the GUI window, select the desired ingredients for your bowl: base, protein, toppings, and sauce.
3. Click the "Place Order" button to submit your order.
4. The system will process the order and display information about the sequence of actions the robotic arm will follow to prepare the bowl.

## Project Structure

- `CooLex_Dispenser.py`: Contains classes for managing the ingredient and bowl dispensers.
- `CooLex_Robot.py`: Implements the CooLex robotic agent and the problem formulation for the A* algorithm.
- `GUI_CooLex.py`: Creates the graphical user interface and handles the interaction with the other components.

## Authors

- Eric Casañé (@ericcasane)
- Ismael Barroso
