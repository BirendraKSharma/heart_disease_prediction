import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import pandas as pd

MODEL_PATH = 'hd.pkl'
FEATURES = [
    "Age",
    "Sex [1=Male, 0=Female]",
    "ChestPainType [0:ATA, 1:NAP, 2:ASY, 3:TA]",
    "RestingBP",
    "Cholesterol",
    "FastingBS [1/0]",
    "RestingECG [0:Normal, 1:ST, 2:LVH]",
    "MaxHR",
    "ExerciseAngina [1=No, 0=Yes]",
    "Oldpeak",
    "ST_Slope [0:Up, 1:Flat, 2:Down]"
]
COLUMNS = [
    'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
    'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'
]
DEFAULTS = ["42", "0", "0", "110", "180", "0", "0", "160", "1", "0.0", "0"]

def predict_heart_disease(values, model_path=MODEL_PATH):
    try:
        # Convert values to correct types
        processed = [
            int(values[0]),  # Age
            int(values[1]),  # Sex
            int(values[2]),  # ChestPainType
            int(values[3]),  # RestingBP
            int(values[4]),  # Cholesterol
            int(values[5]),  # FastingBS
            int(values[6]),  # RestingECG
            int(values[7]),  # MaxHR
            int(values[8]),  # ExerciseAngina
            float(values[9]),# Oldpeak
            int(values[10])  # ST_Slope
        ]
        df = pd.DataFrame([processed], columns=COLUMNS)
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        prediction = model.predict(df)
        return "No Disease" if prediction[0] == 0 else "Disease"
    except Exception as e:
        return f"error::{str(e)}"

def on_predict():
    values = [entry.get().strip() for entry in entries]
    if any(v == "" for v in values):
        result_var.set("Please fill all fields.")
        result_label.config(foreground="orange")
        return
    result = predict_heart_disease(values)
    if result.startswith("error::"):
        messagebox.showerror("Prediction Error", result[7:])
        result_var.set("Prediction failed.")
        result_label.config(foreground="orange")
    elif result == "Disease":
        result_var.set("Prediction: Heart Disease Detected")
        result_label.config(foreground="red")
    else:
        result_var.set("Prediction: No Heart Disease")
        result_label.config(foreground="green")

# --- GUI Setup ---
root = tk.Tk()
root.title("Heart Disease Predictor")
root.geometry("520x600")
root.configure(bg="#f4f6fa")

style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#f4f6fa')
style.configure('TLabel', background='#f4f6fa', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 11, 'bold'))
style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background='#f4f6fa')

main_frame = ttk.Frame(root, padding=24, style='TFrame')
main_frame.pack(fill="both", expand=True)

header_label = ttk.Label(main_frame, text="Heart Disease Prediction Tool", style='Header.TLabel')
header_label.grid(row=0, column=0, columnspan=2, pady=(0, 18))

entries = []
for i, (label_text, default) in enumerate(zip(FEATURES, DEFAULTS)):
    ttk.Label(main_frame, text=label_text).grid(row=i+1, column=0, sticky="w", pady=6, padx=(0, 10))
    entry = ttk.Entry(main_frame, width=18)
    entry.grid(row=i+1, column=1, pady=6)
    entry.insert(0, default)
    entries.append(entry)

predict_btn = ttk.Button(main_frame, text="Predict", command=on_predict)
predict_btn.grid(row=len(FEATURES)+1, column=0, columnspan=2, pady=(18, 8))

result_var = tk.StringVar()
result_label = ttk.Label(main_frame, textvariable=result_var, font=("Segoe UI", 12, "bold"))
result_label.grid(row=len(FEATURES)+2, column=0, columnspan=2, pady=(10,0))

# Optional: Set focus to first entry
entries[0].focus()

root.mainloop()