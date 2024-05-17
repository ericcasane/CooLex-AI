class DispenserAgent:
    def __init__(self):
        self.bowls = Dispenser("Bowls", 650, 660, 80, 1)  # Bowls as a dispenser
        self.ingredients = {
            'base': [
                Dispenser("Arròs", 610, 10, 20000, 250),
                Dispenser("Arròs Earth Mama", 640, 10, 20000, 250),
                Dispenser("Quinoa", 670, 10, 20000, 250)
            ],
            'protein': [
                Dispenser("Pollastre rostit al carbó", 450, 10, 16000, 200),
                Dispenser("Gall dindi fumat al carbó", 480, 10, 16000, 200),
                Dispenser("Proteïna vegetal", 510, 10, 16000, 200),
                Dispenser("Vedella gallega al carbó", 540, 10, 16000, 200),
                Dispenser("Salmó fumat amb fusta", 570, 10, 16000, 200)
            ],
            'toppings': [
                Dispenser("Tomàquet cherry", 140, 10, 8000, 100),
                Dispenser("Bolets shiitake", 170, 10, 8000, 100),
                Dispenser("Moniato", 200, 10, 8000, 100),
                Dispenser("Nous", 230, 10, 8000, 100),
                Dispenser("Pinya fumada", 260, 10, 8000, 100),
                Dispenser("Mango", 290, 10, 8000, 100),
                Dispenser("Alvocat", 320, 10, 8000, 100),
                Dispenser("Cigrons picants", 350, 10, 8000, 100),
                Dispenser("Formatge fumat", 380, 10, 8000, 100),
                Dispenser("Carbassa", 410, 10, 8000, 100)
            ],
            'sauces': [
                Dispenser("Crema vegetariana amb jalapeny i alfàbrega triturada", 100, 10, 6000, 75),
                Dispenser("Crema vegetariana amb remolatxa", 40, 10, 6000, 75),
                Dispenser("Crema de tartufata amb bolets i tòfona negra", 70, 10, 6000, 75),
                Dispenser("Crema de chimichurri amb suc de taronja", 100, 10, 6000, 75)
            ]
        }

    def get_base_ingredients(self):
        return self.ingredients['base']

    def get_protein_ingredients(self):
        return self.ingredients['protein']

    def get_toppings(self):
        return self.ingredients['toppings']

    def get_sauces(self):
        return self.ingredients['sauces']


class Dispenser:
    def __init__(self, name, positionX, positionY, quantity, amount_to_bowl):
        self.name = name
        self.initial_quantity = quantity
        self.current_quantity = quantity
        self.positionX = positionX
        self.positionY = positionY
        self.amount_to_bowl = amount_to_bowl

    def dispense(self):
        if self.current_quantity >= self.amount_to_bowl:
            self.current_quantity -= self.amount_to_bowl
            print(f"Dispensed {self.amount_to_bowl} of {self.name}.")
            return True
        else:
            print(f"Insufficient quantity of {self.name}.")
            return False

    def get_position(self):
        return self.positionX, self.positionY

    def check_stock(self):
        return self.current_quantity >= 0.2 * self.initial_quantity

    def restock_alert(self):
        if self.current_quantity < 0.2 * self.initial_quantity:
            print(f"Alert: Stock of {self.name} is below 20%.")
