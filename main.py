import tkinter as tk

from controller.Controller import Controller
from model.QuantumCalculator import QuantumCalculator
from view.MainWindow import MainWindow

root = tk.Tk()
quantum_calculator = QuantumCalculator()
controller = Controller(quantum_calculator)
app = MainWindow(root, controller)
root.mainloop()