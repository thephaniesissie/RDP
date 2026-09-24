class PetriNetMachine:
    def __init__(self):
        # Marquage initial : 1 jeton en P1 (repos) et 5 jetons en P3 (stock gobelets)
        self.places = {
            "P1": 1,
            "P2": 0,
            "P3": 5,
            "P4": 0,
            "P5": 0,
            "P6": 0
        }
        
        # Matrice Pré (places amont requises)
        self.pre = {
            "t1": {"P1": 1},
            "t2": {"P2": 1, "P3": 1},
            "t3": {"P4": 1, "P5": 1},
            "t4": {"P6": 1}
        }
        
        # Matrice Post (places aval produites)
        self.post = {
            "t1": {"P2": 1},
            "t2": {"P4": 1, "P5": 1},
            "t3": {"P6": 1},
            "t4": {"P1": 1}
        }

    def can_fire(self, t_name: str) -> bool:
        """Vérifie si la transition est franchissable selon la matrice Pré."""
        if t_name not in self.pre:
            return False
        for place, weight in self.pre[t_name].items():
            if self.places[place] < weight:
                return False
        return True

    def fire(self, t_name: str) -> bool:
        """Franchit la transition si elle est franchissable."""
        if not self.can_fire(t_name):
            return False
            
        # Retrait des jetons selon la matrice Pré
        for place, weight in self.pre[t_name].items():
            self.places[place] -= weight
            
        # Ajout des jetons selon la matrice Post
        for place, weight in self.post[t_name].items():
            self.places[place] += weight
            
        return True

    def restock_cups(self, amount: int = 5):
        """Recharge le stock de gobelets (place P3)."""
        self.places["P3"] += amount