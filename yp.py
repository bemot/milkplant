import simpy
import random
import matplotlib.pyplot as plt
import os
import subprocess
import sys

PRODUCTION_PLAN = {
    'Classic': 300,
    'Fruit': 200,
    'Greek': 200,
    'Strawberry': 100,
    'Vanilla': 50,
    'Chocolate': 150,
    'Honey': 100,
    'Blueberry': 80,
    'Raspberry': 120,
    'Mango': 90,
    'Coconut': 70,
    'Lemon': 60,
    'Peach': 110,
    'Pineapple': 130,
    'Green Tea': 40,
    'Matcha': 30,
    'Coffee': 50,
    'Almond': 280,
    'Hazelnut': 60,
}

LINE_CAPACITY = {
    'Line 1': 0.5,
    'Line 2': 0.6,
    'Line 3': 0.55,
    'Line 4': 0.58,
    'Line 5': 0.52,
}

LINE_CLEANING_TIME = {
    'Line 1': 30,
    'Line 2': 20,
    'Line 3': 25,
    'Line 4': 20,
    'Line 5': 22,
}

TOTAL_TIME_LIMIT = 1440  # 24 hours in minutes
gantt_data = []

def simulate_production():
    pass  # Stub for compatibility

def draw_gantt_chart():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Pre-assign consistent colors to all yogurt types
    yogurt_types = sorted(PRODUCTION_PLAN.keys())
    color_cycle = plt.cm.get_cmap('tab20', len(yogurt_types))
    colors = {yogurt: color_cycle(i) for i, yogurt in enumerate(yogurt_types)}

    gantt_data_sorted = sorted(gantt_data, key=lambda x: x[0])
    y_labels = list(sorted(set(line for line, _, _, _ in gantt_data_sorted)))
    y_positions = {label: i for i, label in enumerate(y_labels)}
    
    used_yogurts = set()

    for i, (line, start, end, yogurt) in enumerate(gantt_data_sorted):
        color = colors[yogurt]
        # Only add label first time this yogurt appears
        label = yogurt if yogurt not in used_yogurts else ""
        used_yogurts.add(yogurt)
        
        ax.barh(y_positions[line], end - start, left=start, height=0.4,
                label=label, color=color)
        label_text = f"{yogurt}\n{round(start)}–{round(end)}"
        ax.text(start + (end - start)/2, y_positions[line], label_text,
                va='center', ha='center', fontsize=7, color='white')

    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(y_positions.keys()))
    ax.set_xlabel("Minutes")
    ax.set_title("Yogurt Production Gantt Chart by Line")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize='small')
    plt.tight_layout()
    plt.savefig("gantt_chart.png")
    plt.close()