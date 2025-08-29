from medical_data_visualizer import draw_cat_plot, draw_heat_map

if __name__ == "__main__":
    # Genera ambas figuras y las muestra si corres local
    fig1 = draw_cat_plot()
    fig2 = draw_heat_map()
    print("Figuras creadas: cat plot y heat map (no mostradas en entorno headless).")
