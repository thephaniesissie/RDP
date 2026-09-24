import tkinter as tk
from tkinter import messagebox
from petri_net import PetriNetMachine

class PetriNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Réseau de Petri - Distributeur de Café")
        self.root.geometry("850x650")
        self.root.configure(bg="#2c3e50")

        self.net = PetriNetMachine()

        # Titre
        title = tk.Label(
            root,
            text="Distributeur de Café - Réseau de Petri",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        title.pack(pady=10)

        # Zone Canvas
        self.canvas = tk.Canvas(root, width=800, height=480, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Repositionnement des places pour un tracé fluide
        self.place_coords = {
            "P1": (400, 50),   # Repos
            "P2": (400, 150),  # Pièce insérée
            "P3": (150, 220),  # Stock gobelets
            "P4": (280, 290),  # Gobelet distribué
            "P5": (520, 290),  # Préparation café
            "P6": (400, 390),  # Boisson prête
        }

        # Coordonnées des transitions
        self.trans_coords = {
            "t1": (400, 100),
            "t2": (400, 220),
            "t3": (400, 340),
            "t4": (400, 440),
        }

        # Panneau de contrôle (Boutons)
        btn_frame = tk.Frame(root, bg="#2c3e50")
        btn_frame.pack(pady=10)

        self.btn_t1 = tk.Button(
            btn_frame, text="t1: Insérer pièce", command=lambda: self.trigger_transition("t1"), font=("Arial", 10, "bold"), bg="#27ae60", fg="white", padx=10
        )
        self.btn_t1.grid(row=0, column=0, padx=5)

        self.btn_t2 = tk.Button(
            btn_frame, text="t2: Sélectionner café", command=lambda: self.trigger_transition("t2"), font=("Arial", 10, "bold"), bg="#2980b9", fg="white", padx=10
        )
        self.btn_t2.grid(row=0, column=1, padx=5)

        self.btn_t3 = tk.Button(
            btn_frame, text="t3: Verser café", command=lambda: self.trigger_transition("t3"), font=("Arial", 10, "bold"), bg="#e67e22", fg="white", padx=10
        )
        self.btn_t3.grid(row=0, column=2, padx=5)

        self.btn_t4 = tk.Button(
            btn_frame, text="t4: Retirer boisson", command=lambda: self.trigger_transition("t4"), font=("Arial", 10, "bold"), bg="#8e44ad", fg="white", padx=10
        )
        self.btn_t4.grid(row=0, column=3, padx=5)

        self.btn_restock = tk.Button(
            btn_frame, text="Recharger gobelets (+5)", command=self.restock_cups, font=("Arial", 10), bg="#7f8c8d", fg="white", padx=10
        )
        self.btn_restock.grid(row=0, column=4, padx=15)

        self.draw_net()

    def draw_net(self):
        """Redessine le réseau de Petri et met à jour les boutons."""
        self.canvas.delete("all")

        # Arcs du réseau
        arcs = [
            ("P1", "t1"), ("t1", "P2"),
            ("P2", "t2"), ("P3", "t2"),
            ("t2", "P4"), ("t2", "P5"),
            ("P4", "t3"), ("P5", "t3"),
            ("t3", "P6"), ("P6", "t4")
        ]

        # Dessin des arcs simples
        for start, end in arcs:
            x1, y1 = self.place_coords.get(start, self.trans_coords.get(start))
            x2, y2 = self.place_coords.get(end, self.trans_coords.get(end))
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="#7f8c8d")

        # Arc courbe de t4 vers P1 (Retour à zéro)
        x_t4, y_t4 = self.trans_coords["t4"]
        x_p1, y_p1 = self.place_coords["P1"]
        self.canvas.create_line(x_t4, y_t4, x_t4 + 280, y_t4, x_p1 + 280, y_p1, x_p1, y_p1, smooth=True, arrow=tk.LAST, width=2, fill="#7f8c8d")

        # Dessin des Transitions (Rectangles)
        for t_name, (x, y) in self.trans_coords.items():
            is_enabled = self.net.can_fire(t_name)
            color = "#2ecc71" if is_enabled else "#e74c3c"
            self.canvas.create_rectangle(x - 25, y - 10, x + 25, y + 10, fill=color, outline="#2c3e50", width=2)
            self.canvas.create_text(x, y, text=t_name, fill="white", font=("Arial", 10, "bold"))

        # Dessin des Places (Cercles)
        labels = {
            "P1": "P1 (Repos)",
            "P2": "P2 (Pièce)",
            "P3": "P3 (Stock Gobelets)",
            "P4": "P4 (Gobelet dist.)",
            "P5": "P5 (Prép. café)",
            "P6": "P6 (Boisson prête)",
        }

        for p_name, (x, y) in self.place_coords.items():
            self.canvas.create_oval(x - 22, y - 22, x + 22, y + 22, fill="#ecf0f1", outline="#34495e", width=2)
            self.canvas.create_text(x, y - 30, text=labels[p_name], fill="#2c3e50", font=("Arial", 9, "bold"))

            # Jetons
            tokens = self.net.places[p_name]
            if tokens == 1:
                self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="#e74c3c")
            elif tokens > 1:
                self.canvas.create_text(x, y, text=str(tokens), fill="#c0392b", font=("Arial", 11, "bold"))

        # Mise à jour de l'état des boutons
        self.btn_t1.config(state=tk.NORMAL if self.net.can_fire("t1") else tk.DISABLED)
        self.btn_t2.config(state=tk.NORMAL if self.net.can_fire("t2") else tk.DISABLED)
        self.btn_t3.config(state=tk.NORMAL if self.net.can_fire("t3") else tk.DISABLED)
        self.btn_t4.config(state=tk.NORMAL if self.net.can_fire("t4") else tk.DISABLED)

    def trigger_transition(self, t_name: str):
        if self.net.fire(t_name):
            self.draw_net()
        else:
            messagebox.showwarning("Action impossible", f"La transition {t_name} ne peut pas être franchie.")

    def restock_cups(self):
        self.net.restock_cups(5)
        self.draw_net()

if __name__ == "__main__":
    root = tk.Tk()
    app = PetriNetGUI(root)
    root.mainloop()