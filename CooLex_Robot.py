from aima3.search import Problem, astar_search
import CooLex_Dispenser

dispenser = CooLex_Dispenser.DispenserAgent()  # Create a new instance of the dispenser


# Define the Problem class for the robot
class ActionProblem(Problem):
    def __init__(self, initial, actions):
        super().__init__(initial)
        self.action_list = sorted(actions, key=lambda x: x[1])  # Order the actions by priority

    def actions(self, state):  # Get the possible actions for the current state
        # Find the current action based on the current state
        current_action = next((action for action in self.action_list if action[0] == state), None)
        if current_action:  # If a current action is found
            next_actions = [action for action in self.action_list if
                            action[1] == current_action[1] + 1]  # Get the next actions
            return next_actions  # Return the next actions
        else:
            return [self.action_list[0]]  # If no current action is found, return the first action

    def result(self, state, action):  # Get the result of applying an action to the current state
        return action[0]  # The new position is the position of the action

    def goal_test(self, state):  # Check if the goal state is reached
        # The goal is reached when the state is equal to the last state in the action list
        return state == self.action_list[-1][0]

    def h(self, node): # Heuristic function to estimate the cost to reach the goal
        if not self.action_list:  # If there are no actions, return 0
            return 0
        # Multiply the distance from Manhattan by the priority of the action
        return self.action_list[0][1] * (
                    abs(node.state[0] - self.action_list[0][0][0]) + abs(node.state[1] - self.action_list[0][0][1]))


# Define the CooLex class for the robot agent
class CooLex:
    def __init__(self, dispenser):
        self.initial_position = (310, 310)  # Initial position of the robot
        self.delivery_position = (410, 610)  # Delivery position
        self.position = self.initial_position  # Current position of the robot
        self.dispenser = dispenser  # Dispenser reference

    # Method to process an order step by step
    def process_order(self, base_choice, protein_choice, topping_choices, sauce_choice):
        print("Nueva orden recibida. Procesando...")
        topping_names = [dispenser.ingredients['toppings'][choice].name for choice in topping_choices]
        print("Detalles del pedido:"
              "\n\t- Base:", dispenser.ingredients['base'][base_choice].name,
              "\n\t- Proteína:", dispenser.ingredients['protein'][protein_choice].name,
              "\n\t- Toppings:", ', '.join(topping_names),
              "\n\t- Salsa:", dispenser.ingredients['sauces'][sauce_choice].name)

        # Create a list of all actions with their priorities
        actions = [
            (dispenser.bowls.get_position(), 1),
            (dispenser.ingredients['base'][base_choice].get_position(), 2),
            (dispenser.ingredients['protein'][protein_choice].get_position(), 3),
            *[(dispenser.ingredients['toppings'][choice].get_position(), 4) for choice in topping_choices],
            (dispenser.ingredients['sauces'][sauce_choice].get_position(), 5),
            (self.delivery_position, 6)
        ]
        problem = ActionProblem(self.position, actions)  # Create a new problem instance
        solution = astar_search(problem)  # Retrieve the solution using A* search
        order_info = []  # List to store the order of actions
        if solution is not None:
            print("Solución:", solution.solution())
            path = solution.path()  # Get the path from the root to the solution
            for i, node in enumerate(path):
                print(f"Paso {i + 1}: {node.state}")  # Print the step number and the position
                self.move_to(node.state)  # Move to the position
                dispenser_at_position = self.get_dispenser_at_position(node.state)  # Get the dispenser at the position
                if dispenser_at_position: # If a dispenser is found
                    dispenser_at_position.dispense()  # Dispense the ingredient
                    order_info.append(dispenser_at_position.name)  # Add the name of the action to the list
                    print(f"-> Dispensado {dispenser_at_position.name}.")
        else:
            print("No se encontró una solución para procesar la orden.")

        self.move_to(self.initial_position)  # Move back to the initial position
        return order_info  # Return the list of actions

    # Method to get the dispenser at a specific position
    def get_dispenser_at_position(self, position):
        for dispenser_list in self.dispenser.ingredients.values():
            for dispenser in dispenser_list:
                if dispenser.get_position() == position:
                    return dispenser
        if position == self.dispenser.bowls.get_position():
            return self.dispenser.bowls
        return None

    # Method to move the robot to a specific position
    def move_to(self, position):
        print(f"-> Moviendo de {self.position} a {position}.")
        self.position = (position[0], position[1])
