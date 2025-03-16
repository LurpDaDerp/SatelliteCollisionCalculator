import numpy as np
import time
import tkinter as tk
from tkinter import ttk
import pygame
from threading import Thread

SATELLITE_RADIUS = 2  # in meters
ORBITAL_ALTITUDE = 700  # in km
UPDATE_FREQUENCY = 1000  # How often to update the live results
LIVE_RUN = False  # Whether to run indefinitely

# Calculated Variables
DEBRIS_PATH_WIDTH = 50
DEBRIS_ALTITUDE_VARIATION = 20
DEBRIS_MIN_RADIUS = 0.01
DEBRIS_MAX_RADIUS = 20
DEBRIS_MIN_VELOCITY = 1
DEBRIS_MAX_VELOCITY = 15
DEBRIS_DENSITY_VARIATION = [0.1, 1, 5]
ORBITAL_INCLINATION_RANGE = 180
SATELLITE_MOBILITY = True
SATELLITE_SHIELD_PROB_REDUCTION = 0.1

# Global UI Variables
hit_count = 0
total_steps = 0

# UI Labels for Variables
current_altitude = 0
current_distance = 0
current_radius = 0
current_velocity = 0
current_inclination = 0
current_collision_chance = 0

def debris_probability_live():
    global hit_count, total_steps, current_altitude, current_distance, current_radius, current_velocity, current_inclination, current_collision_chance
    hit_count = 0
    total_steps = 0

    while LIVE_RUN:
        for _ in range(UPDATE_FREQUENCY):
            total_steps += 1

            # Randomly generate debris altitude variation
            debris_altitude_variation = np.random.uniform(-DEBRIS_ALTITUDE_VARIATION, DEBRIS_ALTITUDE_VARIATION)
            debris_altitude = ORBITAL_ALTITUDE + debris_altitude_variation
            current_altitude = debris_altitude  # Update for UI

            # Randomly generate horizontal distance from satellite
            debris_horizontal_distance = np.random.uniform(0, DEBRIS_PATH_WIDTH)
            current_distance = debris_horizontal_distance  # Update for UI

            # Randomly generate debris size
            debris_radius = np.random.uniform(DEBRIS_MIN_RADIUS, DEBRIS_MAX_RADIUS)
            current_radius = debris_radius  # Update for UI

            # Randomly generate debris speed
            debris_velocity = np.random.uniform(DEBRIS_MIN_VELOCITY, DEBRIS_MAX_VELOCITY)
            current_velocity = debris_velocity  # Update for UI

            # Randomly adjust debris density
            debris_density_factor = np.random.choice(DEBRIS_DENSITY_VARIATION)

            # Randomly generate orbital inclination
            debris_inclination = np.random.uniform(0, ORBITAL_INCLINATION_RANGE)
            current_inclination = debris_inclination  # Update for UI

            # Check if satellite can maneuver
            if SATELLITE_MOBILITY:
                if np.random.rand() < 0.5:
                    continue  # Successfully dodged

            # Collision Angle
            collision_angle = np.abs(debris_inclination - 90)
            collision_angle_factor = 1 if collision_angle < 30 else 0.5

            # Adjust collision probability based on satellite shielding
            collision_probability_reduction = SATELLITE_SHIELD_PROB_REDUCTION if SATELLITE_SHIELD_PROB_REDUCTION else 1
            collision_chance = debris_density_factor * collision_angle_factor * (1 - collision_probability_reduction)
            current_collision_chance = collision_chance  # Update for UI

            if debris_horizontal_distance <= (SATELLITE_RADIUS + debris_radius) and np.random.rand() < collision_chance:
                hit_count += 1

        # Update UI timer
        probability_of_hit = hit_count / total_steps
        update_ui(probability_of_hit * 100)

        time.sleep(0.05)

# UI Updater
def update_ui(probability):
    if 'root' in globals():
        result_label.config(text=f"Current Probability of Collision: {probability:.5f}%")
        altitude_label.config(text=f"Current Altitude: {current_altitude:.2f} km")
        distance_label.config(text=f"Distance of Nearest Debris {current_distance:.2f} m")
        radius_label.config(text=f"Nearest Debris Size (Radius): {current_radius:.2f} m")
        velocity_label.config(text=f"Nearest Debris Speed: {current_velocity:.2f} km/s")
        inclination_label.config(text=f"Nearest Debris Inclination: {current_inclination:.2f} degrees")
        collision_chance_label.config(text=f"Collision Chance: {current_collision_chance:.5f}")
        root.update_idletasks()

# Start simulation
def start_simulation():
    global LIVE_RUN
    LIVE_RUN = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    # Start simulation in new thread
    simulation_thread = Thread(target=debris_probability_live)
    simulation_thread.daemon = True  # Allows thread to exit when the main program does
    simulation_thread.start()

# Stop simulation
def stop_simulation():
    global LIVE_RUN
    LIVE_RUN = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

root = tk.Tk()

root.title("Space Debris Collision Simulation")

# UI

start_button = ttk.Button(root, text="Start Simulation", command = start_simulation)
start_button.grid(row=0, column=1, padx=10, pady=10)

stop_button = ttk.Button(root, text="Stop Simulation", command = stop_simulation, state=tk.DISABLED)
stop_button.grid(row=0, column=2, padx=10, pady=10)

result_label = ttk.Label(root, text="Current Probability of Collision: N/A")
result_label.grid(row=1, column=1, columnspan=4, padx=10, pady=10)
result_label.config(font=('Helvetica', 15))

# Labels
altitude_label = ttk.Label(root, text="Current Altitude: N/A")
altitude_label.grid(row=2, column=1, columnspan=4, padx=15, pady=15)
altitude_label.config(font=('Helvetica', 15))

distance_label = ttk.Label(root, text="Current Distance from Satellite: N/A")
distance_label.grid(row=3, column=1, columnspan=4, padx=15, pady=15)
distance_label.config(font=('Helvetica', 15))

radius_label = ttk.Label(root, text="Nearest Debris Size (Radius): N/A")
radius_label.grid(row=4, column=1, columnspan=4, padx=15, pady=15)
radius_label.config(font=('Helvetica', 15))

velocity_label = ttk.Label(root, text="Debris Speed: N/A")
velocity_label.grid(row=5, column=1, columnspan=4, padx=15, pady=15)
velocity_label.config(font=('Helvetica', 15))

inclination_label = ttk.Label(root, text="Debris Inclination: N/A")
inclination_label.grid(row=6, column=1, columnspan=4, padx=15, pady=15)
inclination_label.config(font=('Helvetica', 15))

collision_chance_label = ttk.Label(root, text="Collision Chance: N/A")
collision_chance_label.grid(row=7, column=1, columnspan=4, padx=15, pady=15)
collision_chance_label.config(font=('Helvetica', 15))

# Start GUI event loop
root.mainloop()
