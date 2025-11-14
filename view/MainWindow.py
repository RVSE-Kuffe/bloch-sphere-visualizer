import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.canvas_widget = None

        self.root.title("Qubit Bloch Gömb Szerkesztő")
        self.root.geometry("800x850")
        self.root.minsize(750, 700)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.image_frame = ttk.Frame(self.main_frame, padding=10)
        self.image_frame.grid(row=0, column=0, sticky="nsew")

        self.footer_frame = ttk.Frame(self.main_frame, padding=10, relief=tk.RAISED, borderwidth=2)
        self.footer_frame.grid(row=1, column=0, sticky="ew")

        self._create_image_placeholder()
        self._create_footer_widgets()
        self._set_picture()

    def _create_image_placeholder(self):
        self.placeholder_label = ttk.Label(
            self.image_frame,
            text="[ A Qiskit Bloch-gömb itt fog megjelenni ]",
            anchor=tk.CENTER,
            relief=tk.SUNKEN,
            font=("Segoe UI", 16)
        )
        self.placeholder_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas_widget = self.placeholder_label

    def _create_footer_widgets(self):
        basis_group = ttk.LabelFrame(self.footer_frame, text="Alapállapotok")
        basis_group.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
        
        btn_set_zero = ttk.Button(basis_group, text="|0⟩ beállít", command=self._set_zero)
        btn_set_zero.pack(padx=10, pady=5, ipady=5)
        
        btn_set_one = ttk.Button(basis_group, text="|1⟩ beállít", command=self._set_one)
        btn_set_one.pack(padx=10, pady=5, ipady=5)

        amplitude_group = ttk.LabelFrame(self.footer_frame, text="Egyéni Amplitúdók (α, β)")
        amplitude_group.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)

        alpha_frame = ttk.Frame(amplitude_group)
        alpha_frame.pack(padx=5, pady=5)
        
        ttk.Label(alpha_frame, text="α =").pack(side=tk.LEFT, padx=(5,2))
        self.alpha_real_entry = ttk.Entry(alpha_frame, width=6)
        self.alpha_real_entry.pack(side=tk.LEFT)
        ttk.Label(alpha_frame, text="+").pack(side=tk.LEFT, padx=3)
        self.alpha_imag_entry = ttk.Entry(alpha_frame, width=6)
        self.alpha_imag_entry.pack(side=tk.LEFT)
        ttk.Label(alpha_frame, text="j").pack(side=tk.LEFT, padx=(2,5))

        self.alpha_real_entry.insert(0, "1.0")
        self.alpha_imag_entry.insert(0, "0.0")

        beta_frame = ttk.Frame(amplitude_group)
        beta_frame.pack(padx=5, pady=5)

        ttk.Label(beta_frame, text="β =").pack(side=tk.LEFT, padx=(5,2))
        self.beta_real_entry = ttk.Entry(beta_frame, width=6)
        self.beta_real_entry.pack(side=tk.LEFT)
        ttk.Label(beta_frame, text="+").pack(side=tk.LEFT, padx=3)
        self.beta_imag_entry = ttk.Entry(beta_frame, width=6)
        self.beta_imag_entry.pack(side=tk.LEFT)
        ttk.Label(beta_frame, text="j").pack(side=tk.LEFT, padx=(2,5))
        
        self.beta_real_entry.insert(0, "0.0")
        self.beta_imag_entry.insert(0, "0.0")

        display_frame = ttk.Frame(self.footer_frame)
        display_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
        
        display_btn = ttk.Button(display_frame, text="Amplitúdók Beállítása", command=self._set_base_sphere)
        display_btn.pack(expand=True, fill=tk.BOTH, padx=5, ipady=5)

        gate_group = ttk.LabelFrame(self.footer_frame, text="Kapuk Alkalmazása")
        gate_group.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)

        gate_frame_row1 = ttk.Frame(gate_group)
        gate_frame_row1.pack(padx=5, pady=2)
        
        gate_frame_row2 = ttk.Frame(gate_group)
        gate_frame_row2.pack(padx=5, pady=2)

        gates_row1 = ['X', 'Y', 'Z', 'H']
        gates_row2 = ['S', 'T', 'P']

        for gate in gates_row1:
            btn = ttk.Button(gate_frame_row1, text=gate, width=4, command=lambda g = gate: self._apply_gate(g))
            btn.pack(side=tk.LEFT, padx=3, pady=3, ipady=2)

        for gate in gates_row2:
            btn = ttk.Button(gate_frame_row2, text=gate, width=4, command=lambda g = gate: self._apply_gate(g))
            btn.pack(side=tk.LEFT, padx=3, pady=3, ipady=2)

    def _set_base_sphere(self):
        success = self.controller.set_base_bloch_sphere(self.alpha_real_entry.get(), self.alpha_imag_entry.get(), self.beta_real_entry.get(), self.beta_imag_entry.get())

        if not success:
            messagebox.showerror(
                'Hiba', 
                "Érvénytelen amplitúdók! Az állapotot nem sikerült beállítani."
            )
            self._update_entries_from_state()
            return

        self._set_picture()

    def _apply_gate(self, gate):
        self.controller.apply_gate(gate)
        self._set_picture()    
        self._update_entries_from_state()

    def _set_picture(self):
        if self.canvas_widget:
            self.canvas_widget.destroy()

        picture_figure = self.controller.get_sphere_image()
        
        canvas = FigureCanvasTkAgg(picture_figure, master=self.image_frame)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        plt.close()
    
    def _set_zero(self):
        self.alpha_real_entry.delete(0, tk.END)
        self.alpha_imag_entry.delete(0, tk.END)
        self.beta_real_entry.delete(0, tk.END)
        self.beta_imag_entry.delete(0, tk.END)

        self.alpha_real_entry.insert(0, "1.0")
        self.alpha_imag_entry.insert(0, "0.0")
        self.beta_real_entry.insert(0, "0.0")
        self.beta_imag_entry.insert(0, "0.0")

    def _set_one(self):
        self.alpha_real_entry.delete(0, tk.END)
        self.alpha_imag_entry.delete(0, tk.END)
        self.beta_real_entry.delete(0, tk.END)
        self.beta_imag_entry.delete(0, tk.END)

        self.alpha_real_entry.insert(0, "0.0")
        self.alpha_imag_entry.insert(0, "0.0")
        self.beta_real_entry.insert(0, "1.0")
        self.beta_imag_entry.insert(0, "0.0")

    def _update_entries_from_state(self):
        state = self.controller.state_vector
        alpha = state[0]
        beta = state[1]
        
        self.alpha_real_entry.delete(0, tk.END)
        self.alpha_imag_entry.delete(0, tk.END)
        self.beta_real_entry.delete(0, tk.END)
        self.beta_imag_entry.delete(0, tk.END)
        
        self.alpha_real_entry.insert(0, f"{alpha.real:.4f}")
        self.alpha_imag_entry.insert(0, f"{alpha.imag:.4f}")
        self.beta_real_entry.insert(0, f"{beta.real:.4f}")
        self.beta_imag_entry.insert(0, f"{beta.imag:.4f}")           