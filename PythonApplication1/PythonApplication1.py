import tkinter as tk
from tkinter import ttk, messagebox
import re

# Function to parse the input text and calculate DPS
def calculate_dps(input_text):
    try:
        # Extract Physical Damage (min-max)
        physical_damage_match = re.search(r"Physical Damage: (\d+)-(\d+)", input_text)
        physical_min = int(physical_damage_match.group(1)) if physical_damage_match else 0
        physical_max = int(physical_damage_match.group(2)) if physical_damage_match else 0

        # Extract Elemental Damage (all min-max values)
        elemental_damage_matches = re.findall(r"Elemental Damage: (\d+)-(\d+)", input_text)
        elemental_damage = [(int(match[0]), int(match[1])) for match in elemental_damage_matches]

        # Extract additional flat elemental damages (e.g., Adds X to Y Damage)
        additional_damage_matches = re.findall(r"Adds (\d+) to (\d+) [A-Za-z]+ Damage", input_text)
        additional_damage = [(int(match[0]), int(match[1])) for match in additional_damage_matches]

        # Extract Attacks per Second
        attack_speed_match = re.search(r"Attacks per Second: ([\d.]+)", input_text)
        attack_speed = float(attack_speed_match.group(1)) if attack_speed_match else 1.0

        # Combine all damage ranges
        total_min_damage = physical_min + sum(dmg[0] for dmg in elemental_damage + additional_damage)
        total_max_damage = physical_max + sum(dmg[1] for dmg in elemental_damage + additional_damage)

        # Calculate DPS
        avg_damage = (total_min_damage + total_max_damage) / 2
        dps = avg_damage * attack_speed

        return {
            "Total Min Damage": total_min_damage,
            "Total Max Damage": total_max_damage,
            "Average Damage": avg_damage,
            "Attack Speed": attack_speed,
            "DPS": dps
        }
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while calculating DPS: {e}")
        return None

# Function to handle button click
def on_calculate():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Required", "Please paste the item details into the text box.")
        return

    result = calculate_dps(input_text)
    if result:
        result_text.set(f"DPS: {result['DPS']:.2f}\n"
                        f"Total Min Damage: {result['Total Min Damage']}\n"
                        f"Total Max Damage: {result['Total Max Damage']}\n"
                        f"Average Damage: {result['Average Damage']:.2f}\n"
                        f"Attack Speed: {result['Attack Speed']:.2f}")

# Function to clear the text box
def on_clear():
    text_input.delete("1.0", tk.END)
    result_text.set("")

# Create the main application window
app = tk.Tk()
app.title("DPS Calculator")
app.geometry("500x400")

# Input Text Area
label_input = tk.Label(app, text="Paste Item Details Below:")
label_input.pack(pady=5)

text_input = tk.Text(app, height=10, width=60)
text_input.pack(pady=5)

# Buttons Frame
buttons_frame = tk.Frame(app)
buttons_frame.pack(pady=10)

# Calculate Button
btn_calculate = ttk.Button(buttons_frame, text="Calculate DPS", command=on_calculate)
btn_calculate.grid(row=0, column=0, padx=5)

# Clear Button
btn_clear = ttk.Button(buttons_frame, text="Clear Input", command=on_clear)
btn_clear.grid(row=0, column=1, padx=5)

# Output Label
result_text = tk.StringVar()
label_result = tk.Label(app, textvariable=result_text, justify=tk.LEFT, anchor="w")
label_result.pack(pady=10, fill=tk.BOTH)

# Run the application
app.mainloop()
