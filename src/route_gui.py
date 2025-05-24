import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from route_mind import create_graph, a_star, draw_graph
import os


NAVY = "#2c304d"
PURPLE = "#7d3951"
TOMATO = "#e94e77"
PEACH = "#fca96c"
TEXT_COLOR = "white"


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("RouteMind - Smart Route Finder")
app.geometry("800x600")
app.configure(fg_color=NAVY)

bg_image_path = "background.png"
if os.path.exists(bg_image_path):
    img = Image.open(bg_image_path).resize((800, 600))
    bg_image = CTkImage(light_image=img, dark_image=img, size=(800, 600))
    background_label = ctk.CTkLabel(app, image=bg_image, text="")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    print(" Background image not found!")


G = create_graph()
nodes = list(G.nodes)

#Input Validation
def validate_range(value, label):
    if not value.strip().isdigit():
        raise ValueError(f"{label} must be a number between 0 and 10.")
    num = int(value.strip())
    if num < 0 or num > 10:
        raise ValueError(f"{label} must be between 0 and 10.")
    return num

#Result
def show_result_window(path, cost):
    result_win = ctk.CTkToplevel(app)
    result_win.title("Best Route Result")
    result_win.geometry("600x400")
    result_win.configure(fg_color=NAVY)

    result_path = "result.png"
    if os.path.exists(result_path):
        result_img = Image.open(result_path).resize((600, 400))
        result_bg = CTkImage(light_image=result_img, dark_image=result_img)
        label_bg = ctk.CTkLabel(result_win, image=result_bg, text="")
        label_bg.image = result_bg
        label_bg.place(x=0, y=0, relwidth=1, relheight=1)

    ctk.CTkLabel(result_win, text="Best Route", font=ctk.CTkFont(size=20, weight="bold"),
                 text_color=PEACH).pack(pady=20)

    ctk.CTkLabel(result_win, text=f"Route: {' → '.join(path)}", text_color=TEXT_COLOR,
                 font=ctk.CTkFont(size=16)).pack(pady=10)

    ctk.CTkLabel(result_win, text=f"Estimated Cost: {round(cost, 2)}", text_color=TEXT_COLOR,
                 font=ctk.CTkFont(size=16)).pack(pady=10)

    ctk.CTkButton(result_win, text="Show Map", command=lambda: draw_graph(G, path),
                  fg_color=TOMATO, hover_color=PEACH).pack(pady=20)

def run_route():
    try:
        src = source_var.get().strip()
        dest = dest_var.get().strip()

        if not src or not dest:
            raise ValueError("Please select both source and destination.")

        if src == dest:
            raise ValueError("Source and destination must be different.")

        traffic = validate_range(traffic_entry.get(), "Traffic Level")
        weather = validate_range(weather_entry.get(), "Weather Level")
        road = validate_range(road_entry.get(), "Road Quality")
        time = validate_range(time_entry.get(), "Time of Day")

        road_type_val = road_type_var.get().strip()
        if road_type_val not in ['0', '1', '2']:
            raise ValueError("Road type must be selected.")
        road_type = int(road_type_val)

       
        path, cost = a_star(G, src, dest, traffic, weather, road, time, road_type)
        show_result_window(path, cost)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Fuzzy Logic Error", f"Error: {e}")


form = ctk.CTkFrame(app, corner_radius=15, fg_color=PURPLE)
form.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkLabel(form, text="RouteMind", font=ctk.CTkFont(size=22, weight="bold"), text_color=PEACH).grid(
    row=0, column=0, columnspan=2, pady=(20, 10))

def add_input(label, row, var_type="entry", values=None):
    ctk.CTkLabel(form, text=label, text_color="white").grid(row=row, column=0, padx=10, pady=5, sticky="w")
    if var_type == "entry":
        entry = ctk.CTkEntry(form, width=200)
        entry.grid(row=row, column=1, padx=10)
        return entry
    elif var_type == "dropdown":
        combo = ctk.CTkComboBox(form, values=values)
        combo.grid(row=row, column=1, padx=10)
        return combo


source_var = ctk.StringVar()
dest_var = ctk.StringVar()
road_type_var = ctk.StringVar()

source_entry = add_input("Select Source:", 1, "dropdown", nodes)
source_entry.configure(variable=source_var)

dest_entry = add_input("Select Destination:", 2, "dropdown", nodes)
dest_entry.configure(variable=dest_var)

traffic_entry = add_input("Traffic Level (0–10):", 3)
weather_entry = add_input("Weather Level (0–10):", 4)
road_entry = add_input("Road Quality (0–10):", 5)
time_entry = add_input("Time of Day (0 = Early, 10 = Night):", 6)

road_type_dropdown = add_input("Road Type (0=Street, 1=Main, 2=Highway):", 7, "dropdown", ["0", "1", "2"])
road_type_dropdown.configure(variable=road_type_var)


ctk.CTkButton(form, text="Find Best Route", command=run_route,
              fg_color=TOMATO, hover_color=PEACH).grid(columnspan=2, pady=15)

app.mainloop()
