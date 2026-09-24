class PetriNetMachine:
    def __init__(self):
        # Marquage initial : 1 jeton en P1 (Repos) et 5 jetons en P3 (Gobelets)
        self.places = {
            "P1": 1,
            "P2": 0,
            "P3": 5,
            "P4": 0,
            "P5": 0,
            "P6": 0
        }
        
        # Matrice Pré (Consommation de jetons par transition)
        self.pre = {
            "t1": {"P1": 1},
            "t2": {"P2": 1, "P3": 1},
            "t3": {"P4": 1, "P5": 1},
            "t4": {"P6": 1}
        }
        
        # Matrice Post (Production de jetons par transition)
        self.post = {
            "t1": {"P2": 1},
            "t2": {"P4": 1, "P5": 1},
            "t3": {"P6": 1},
            "t4": {"P1": 1}
        }

    def can_fire(self, t_name: str) -> bool:
        """Vérifie si les conditions sont réunies pour franchir la transition."""
        if t_name not in self.pre:
            return False
        for place, weight in self.pre[t_name].items():
            if self.places[place] < weight:
                return False
        return True

    def fire(self, t_name: str) -> bool:
        """Exécute le franchissement de la transition si elle est tirabilité."""
        if not self.can_fire(t_name):
            return False
            
        # Retrait des jetons des places amont
        for place, weight in self.pre[t_name].items():
            self.places[place] -= weight
            
        # Ajout des jetons dans les places aval
        for place, weight in self.post[t_name].items():
            self.places[place] += weight
            
        return True

    def restock_cups(self, amount: int = 5):
        """Recharge le stock de gobelets."""
        self.places["P3"] += amount