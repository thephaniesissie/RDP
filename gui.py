import tkinter as tk
from tkinter import messagebox
from petri_net import PetriNetMachine

class PetriNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Réseau de Petri - Distributeur de Café")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e272e")

        self.net = PetriNetMachine()

        # Titre principal
        title = tk.Label(
            root,
            text="Distributeur de Café - Simulation Réseau de Petri",
            font=("Helvetica", 16, "bold"),
            bg="#1e272e",
            fg="#f5cd79",
        )
        title.pack(pady=10)

        # Zone Canvas pour le dessin du réseau
        self.canvas = tk.Canvas(root, width=860, height=520, bg="#ffffff", highlightthickness=1, highlightbackground="#05c46b")
        self.canvas.pack(pady=5)

        # Coordonnées des places (x, y)
        self.place_coords = {
            "P1": (430, 45),   # Machine en repos
            "P2": (430, 165),  # Pièce insérée
            "P3": (180, 235),  # Stock gobelets
            "P4": (300, 325),  # Gobelet distribué
            "P5": (560, 325),  # Préparation café
            "P6": (430, 425),  # Boisson prête
        }

        # Coordonnées des transitions (x, y)
        self.trans_coords = {
            "t1": (430, 105),  # Insérer pièce
            "t2": (430, 235),  # Sélectionner café
            "t3": (430, 375),  # Verser café
            "t4": (430, 480),  # Retirer boisson
        }

        # Noms complets des places et transitions
        self.place_labels = {
            "P1": "P1 (Repos)",
            "P2": "P2 (Pièce)",
            "P3": "P3 (Stock Gobelets)",
            "P4": "P4 (Gobelet dist.)",
            "P5": "P5 (Prép. café)",
            "P6": "P6 (Boisson prête)",
        }

        self.trans_labels = {
            "t1": "t1: Insérer pièce",
            "t2": "t2: Sélectionner café",
            "t3": "t3: Verser café",
            "t4": "t4: Retirer boisson",
        }

        # Panneau de contrôle des actions
        btn_frame = tk.Frame(root, bg="#1e272e")
        btn_frame.pack(pady=10)

        self.btn_t1 = tk.Button(
            btn_frame, text="t1: Insérer pièce", command=lambda: self.trigger_transition("t1"),
            font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", padx=8, state=tk.DISABLED
        )
        self.btn_t1.grid(row=0, column=0, padx=5)

        self.btn_t2 = tk.Button(
            btn_frame, text="t2: Sélectionner café", command=lambda: self.trigger_transition("t2"),
            font=("Arial", 10, "bold"), bg="#3498db", fg="white", padx=8, state=tk.DISABLED
        )
        self.btn_t2.grid(row=0, column=1, padx=5)

        self.btn_t3 = tk.Button(
            btn_frame, text="t3: Verser café", command=lambda: self.trigger_transition("t3"),
            font=("Arial", 10, "bold"), bg="#e67e22", fg="white", padx=8, state=tk.DISABLED
        )
        self.btn_t3.grid(row=0, column=2, padx=5)

        self.btn_t4 = tk.Button(
            btn_frame, text="t4: Retirer boisson", command=lambda: self.trigger_transition("t4"),
            font=("Arial", 10, "bold"), bg="#9b59b6", fg="white", padx=8, state=tk.DISABLED
        )
        self.btn_t4.grid(row=0, column=3, padx=5)

        self.btn_restock = tk.Button(
            btn_frame, text="Recharger gobelets (+5)", command=self.restock_cups,
            font=("Arial", 10, "bold"), bg="#34495e", fg="white", padx=10
        )
        self.btn_restock.grid(row=0, column=4, padx=15)

        self.draw_net()

    def draw_net(self):
        """Dessine le Réseau de Petri et met à jour l'état visuel."""
        self.canvas.delete("all")

        # 1. Arcs droits du réseau selon la matrice d'incidence
        arcs = [
            ("P1", "t1"), ("t1", "P2"),
            ("P2", "t2"), ("P3", "t2"),
            ("t2", "P4"), ("t2", "P5"),
            ("P4", "t3"), ("P5", "t3"),
            ("t3", "P6"), ("P6", "t4")
        ]

        for start, end in arcs:
            x1, y1 = self.place_coords.get(start, self.trans_coords.get(start))
            x2, y2 = self.place_coords.get(end, self.trans_coords.get(end))
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="#7f8c8d", arrowshape=(10, 12, 5))

        # Arc courbe de retour (t4 -> P1)
        x_t4, y_t4 = self.trans_coords["t4"]
        x_p1, y_p1 = self.place_coords["P1"]
        self.canvas.create_line(
            x_t4, y_t4, x_t4 + 320, y_t4, x_p1 + 320, y_p1, x_p1, y_p1,
            smooth=True, arrow=tk.LAST, width=2, fill="#e74c3c", arrowshape=(10, 12, 5)
        )

        # 2. Dessin des Transitions (Barres / Rectangles)
        for t_name, (x, y) in self.trans_coords.items():
            is_enabled = self.net.can_fire(t_name)
            fill_color = "#2ecc71" if is_enabled else "#e74c3c"
            
            # Transition
            self.canvas.create_rectangle(x - 35, y - 12, x + 35, y + 12, fill=fill_color, outline="#2c3e50", width=2)
            self.canvas.create_text(x, y, text=t_name, fill="white", font=("Arial", 10, "bold"))

        # 3. Dessin des Places (Cercles) + Jetons
        for p_name, (x, y) in self.place_coords.items():
            # Cercle de la place
            self.canvas.create_oval(x - 24, y - 24, x + 24, y + 24, fill="#ecf0f1", outline="#2c3e50", width=2)
            # Libellé au-dessus
            self.canvas.create_text(x, y - 34, text=self.place_labels[p_name], fill="#2c3e50", font=("Arial", 9, "bold"))

            # Jetons
            tokens = self.net.places[p_name]
            if tokens == 1:
                self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="#e74c3c", outline="#c0392b")
            elif tokens > 1:
                self.canvas.create_text(x, y, text=str(tokens), fill="#c0392b", font=("Arial", 12, "bold"))

        # 4. Synchronisation de l'état des boutons avec le réseau
        self.btn_t1.config(state=tk.NORMAL if self.net.can_fire("t1") else tk.DISABLED)
        self.btn_t2.config(state=tk.NORMAL if self.net.can_fire("t2") else tk.DISABLED)
        self.btn_t3.config(state=tk.NORMAL if self.net.can_fire("t3") else tk.DISABLED)
        self.btn_t4.config(state=tk.NORMAL if self.net.can_fire("t4") else tk.DISABLED)

    def trigger_transition(self, t_name: str):
        """Déclenche le franchissement d'une transition."""
        if self.net.fire(t_name):
            self.draw_net()
        else:
            messagebox.showwarning("Franchissement impossible", f"La transition {t_name} n'est pas tirable.")

    def restock_cups(self):
        """Ajoute 5 gobelets au stock P3."""
        self.net.restock_cups(5)
        self.draw_net()

if __name__ == "__main__":
    root = tk.Tk()
    app = PetriNetGUI(root)
    root.mainloop()