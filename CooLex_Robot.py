from aima3.search import Problem, astar_search

import CooLex_Dispenser
dispenser = CooLex_Dispenser.DispenserAgent() # Create a new instance of the dispenser

class ToppingProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def actions(self, state):
        _, remaining_toppings = state
        return list(range(len(remaining_toppings)))

    def result(self, state, action):
        position, remaining_toppings = state
        next_position = remaining_toppings[action].get_position()
        next_remaining_toppings = tuple(remaining_toppings[:action] + remaining_toppings[action+1:])
        return (next_position, next_remaining_toppings)

    def goal_test(self, state):
        _, remaining_toppings = state
        return len(remaining_toppings) == 0

    def h(self, node):
        position, remaining_toppings = node.state
        if not remaining_toppings:
            return 0
        return min(abs(position[0] - topping.get_position()[0]) + abs(position[1] - topping.get_position()[1]) for topping in remaining_toppings)

class CooLex:
    def __init__(self):
        self.initial_position = (310, 310)  # initial position of the robot
        self.delivery_position = (410, 610)
        self.position = self.initial_position

    def move_to(self, position):
        self.position = (position[0], position[1])
        print(f"Moved to {position[0]} at position {position[1]}.")

    def process_step(self, dispenser):
        self.move_to(dispenser.get_position())
        dispenser.dispense()

    def process_order(self, base_choice, protein_choice, topping_choices, sauce_choice):
        # Step-by-step actions
        actions = ["Taking a bowl", "Adding base", "Adding protein", "Adding toppings", "Adding sauce", "Delivery"]
        ingredients_order = []

        # Step 1: Taking a bowl
        print("Taking a bowl.")
        actual_dispenser = dispenser.bowls
        self.move_to(actual_dispenser.get_position())
        actual_dispenser.dispense()

        # Step 2: Adding base
        base = dispenser.ingredients['base'][base_choice]
        print(f"Adding {base.name}.")
        self.process_step(base)
        ingredients_order.append(base.name)

        # Step 3: Adding protein
        protein = dispenser.ingredients['protein'][protein_choice]
        print(f"Adding {protein.name}.")
        self.process_step(protein)
        ingredients_order.append(protein.name)

        # Step 4: Adding toppings
        topping_dispensers = [dispenser.ingredients['toppings'][choice] for choice in topping_choices]  # Get the topping dispensers
        problem = ToppingProblem((self.position, tuple(topping_dispensers)), None) # Create a new problem instance
        solution = astar_search(problem) # Solve the problem with A* search method
        if solution is not None:
            for action in solution.solution():
                topping = topping_dispensers[action]
                print(f"Adding {topping.name}.")
                self.process_step(topping)
                ingredients_order.append(topping.name)

        # Step 5: Adding sauce
        sauce = dispenser.ingredients['sauces'][sauce_choice]
        print(f"Adding {sauce.name}.")
        self.process_step(sauce)
        ingredients_order.append(sauce.name)

        # Step 6: Delivery
        self.move_to(self.delivery_position)
        print("Order ready for delivery.")
        return ingredients_order



coolex = CooLex()
