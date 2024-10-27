import time
from datetime import datetime
import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from tkinter import filedialog
from datetime import datetime
from random import sample
from os.path import isfile

from src.engine.engine import Engine
from src.worlds.world import available_worlds


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(1072, 603)
        self.title("Bisbille des Galaxies")
        self.grid_propagate(False)
        self.frame = Window(self)
        self.frame.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.beamage_filename = ""
        self.score_foldername = ""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        self.mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=self.mode_menu)
        self.mode_menu.add_command(label="Sélectionner fichier Beamage", command=self.select_beamage_file)
        self.mode_menu.add_command(label="Imprimer fichier Beamage", command=self.print_beamage_file)
        self.mode_menu.entryconfig("Imprimer fichier Beamage", state=tk.DISABLED)
        self.mode_menu.add_command(label="Sélectionner fichier score", command=self.select_score_folder)
        self.mode_menu.add_command(label="Imprimer fichier score", command=self.print_score_folder)
        self.mode_menu.entryconfig("Imprimer fichier score", state=tk.DISABLED)

    def select_beamage_file(self):
        self.beamage_filename = filedialog.askopenfilename(initialdir="/", title="Sélectionner fichier Beamage",
            filetypes = (("Fichiers texte", "*.txt"), ("Tout fichiers", "*.*")))
        self.frame.focus_force()
        if self.beamage_filename == "":
            self.mode_menu.entryconfig("Imprimer fichier Beamage", state=tk.DISABLED)
        else:
            self.mode_menu.entryconfig("Imprimer fichier Beamage", state=tk.NORMAL)

    def print_beamage_file(self):
        tk.messagebox.showinfo(title="Fichier beamage", message=f"{self.beamage_filename}")

    def select_score_folder(self):
        self.score_foldername = filedialog.askdirectory(initialdir="/", title="Sélectionner un dossier")
        self.frame.focus_force()
        if self.score_foldername == "":
            self.mode_menu.entryconfig("Imprimer fichier score", state=tk.DISABLED)
        else:
            self.mode_menu.entryconfig("Imprimer fichier score", state=tk.NORMAL)

    def print_score_folder(self):
        tk.messagebox.showinfo(title="Fichier score", message=f"{self.score_foldername}")

class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.n_players = 4
        self.team_number = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Load background image and set up panel
        self.image = Image.open("src/engine/textures/title_screen_1.png")
        self.image_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image)
        self.background.grid(column=0, row=0, columnspan=3, rowspan=3, sticky="nsew")
        self.bind("<Configure>", self.resize_background)
        self.background.lower()

        # Create a frame for buttons to manage their layout
        button_frame = tk.Frame(self, bg="black")
        button_frame.grid(column=1, row=1, sticky="nsew")

        # Configure the button frame to stretch
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1, minsize=100)
        button_frame.columnconfigure(2, weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=1)
        button_frame.rowconfigure(2, weight=1)

        # Buttons: they will now stay centered
        self.decrease_button = tk.Button(
            button_frame, text="-", font=("menlo", 35), bg="white", fg="black", command=self.decrease_players
        )
        self.decrease_button.grid(column=0, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.increase_button = tk.Button(
            button_frame, text="+", font=("menlo", 35), bg="white", fg="black", command=self.increase_players
        )
        self.increase_button.grid(column=2, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.n_players_label = tk.Label(button_frame, text=self.n_players, font=("menlo", 35), bg="white", fg="black")
        self.n_players_label.grid(column=1, row=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.start_button = tk.Button(button_frame, text="START", font=("menlo", 35), bg="white", fg="black",
                                      command=self.start)
        self.start_button.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=(10, 10), pady=(10, 10))
        
        self.team_number_label = tk.Label(button_frame, text="Équipe #", font=("menlo", 35), bg="white", fg="black")
        self.team_number_label.grid(column=0, row=2, columnspan=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.team_number = tk.Entry(
            button_frame, font=("menlo", 35), bg="white", fg="black", justify="right", width=2,
            validate="key", validatecommand=(self.master.register(Window.validate_team_number_entry), "%P")
        )
        self.team_number.grid(column=2, row=2, sticky="nse", padx=(10, 10), pady=(10, 10))

    @staticmethod
    def validate_team_number_entry(value):
        if len(value) <= 2 and value.isdigit() or len(value) == 0:
            return True
        else:
            return False

    def increase_players(self):
        if self.n_players < len(available_worlds):
            self.n_players += 1
            self.update_n_players_label()

    def decrease_players(self):
        self.n_players = max(1, self.n_players - 1)
        self.update_n_players_label()

    def update_n_players_label(self):
        self.n_players_label.config(text=self.n_players)

    def resize_background(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the background image to match the new window size
        self.image = self.image_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)

        # Update the label with the resized background image
        self.background.configure(image=self.background_image)

    def start(self):
        # self.master.beamage_filename = ""
        # if False: pass
        # self.master.beamage_filename = r"C:\Users\Proprio\Documents\Mathieu\bisbille_des_galaxies\beamage.txt"
        if self.master.beamage_filename == "":
            tk.messagebox.showwarning(title="Error", message="Aucun fichier Beamage n'a été donné.")
        elif self.master.score_foldername == "":
            tk.messagebox.showwarning(title="Error", message="Aucun fichier score n'a été donné.")
        elif self.team_number.get() == "":
            tk.messagebox.showwarning(title="Error", message="Aucun numéro d'équipe n'a été donné.")
        else:
            score_filename = f"{self.master.score_foldername}/bisbille_scores.csv"
            if not isfile(score_filename):
                with open(score_filename, "w") as f:
                    f.write("equipe,nombre de joueurs,temps total (s),temps par joueur (s),temps de debut\n")

            engine = Engine(
                beamage_filename=self.master.beamage_filename,
                dev_mode=False
            )
            chosen_worlds = sample(available_worlds, self.n_players)
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_time = []
            for world in chosen_worlds:
                engine.set_world(world())
                time.sleep(1)
                start = time.time()
                engine.run()
                stop = time.time()
                total_time.append(stop - start)

            engine.quit()
            with open(score_filename, "a") as f:
                total = sum(total_time)
                line = f"{self.team_number.get()},{self.n_players},{total},{total/self.n_players},{start_time}\n"
                print(line, end="")
                f.write(line)

            tk.messagebox.showinfo(title="Résultat", message=f"Temps total : {total:.1f}s")
            self.focus_force()


if __name__ == "__main__":
    app = App()
    app.mainloop()
