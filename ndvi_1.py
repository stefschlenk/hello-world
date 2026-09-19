import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def generate_ndvi_map(red_band, nir_band, output_filename="ndvi_map.png"):
    """
    Berechnet den NDVI aus dem Rot-Band (B4) und NIR-Band (B8) 
    und speichert ein eingefärbtes Satellitenbild.
    """
    # 1. Mathematische NDVI-Formel (Pixel für Pixel)
    # Vermeidung von Division durch Null mit np.errstate
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (nir_band - red_band) / (nir_band + red_band)
        # Ungültige Werte (z. B. 0/0) durch NaN ersetzen
        ndvi = np.nan_to_num(ndvi, nan=0.0)

    # 2. Eigene Farbkarte definieren (von Rot über Gelb nach Dunkelgrün)
    # Rot = karg/beaut/wasser, Gelb = wenig Bewuchs, Grün = gesunde Vegetation
    colors = ["#d73027", "#f46d43", "#fdae61", "#fee08b", "#d9ef8b", "#a6d96a", "#66bd63", "#1a9850"]
    custom_cmap = LinearSegmentedColormap.from_list("ndvi_cmap", colors)

    # 3. Bild & Visualisierung erstellen
    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    
    # NDVI Matrix anzeigen (Wertebereich fix von -0.2 bis 0.8 begrenzen für klaren Kontrast)
    im = ax.imshow(ndvi, cmap=custom_cmap, vmin=-0.1, vmax=0.8)
    
    # Farbskala an der Seite hinzufügen
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('NDVI (Vegetationsindex)', rotation=270, labelpad=15)

    # Titel und Achsenbeschriftung
    plt.title("NDVI Vegetations-Analyse", fontsize=14, fontweight='bold')
    plt.axis('off')  # Pixelseitenränder ausblenden

    # 4. Bild als PNG speichern (z. B. für E-Mail oder Telegram)
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close()

    # 5. Einen statistischen Mittelwert für den Text-Bericht ausgeben
    mean_ndvi = np.mean(ndvi)
    print(f"Bild gespeichert unter: {output_filename}")
    print(f"Durchschnittlicher NDVI auf der Parzelle: {mean_ndvi:.2f}")

    return mean_ndvi

# ---------------------------------------------------------
# BEISPIEL-TEST: Simulation von Satellitendaten
# (In der Praxis kommen 'red_band' und 'nir_band' von der Copernicus API)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Erstelle ein zufälliges Test-Raster (z. B. 100 x 100 Pixel)
    np.random.seed(42)
    sample_red = np.random.uniform(0.02, 0.15, (100, 100))  # Rot-Reflektion
    sample_nir = np.random.uniform(0.15, 0.50, (100, 100))  # NIR-Reflektion

    # NDVI berechnen und Bild generieren
    generate_ndvi_map(sample_red, sample_nir, "ndvi_beispiel.png")
