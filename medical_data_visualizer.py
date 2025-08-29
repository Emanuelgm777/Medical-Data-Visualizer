import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1) Cargar datos
df = pd.read_csv("medical_examination.csv")

# 2) Columna overweight (IMC > 25 => 1, si no 0)
#    height en metros
bmi = df["weight"] / (df["height"] / 100) ** 2
df["overweight"] = (bmi > 25).astype(int)

# 3) Normalización colesterol y gluc: 0 = bueno, 1 = malo
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)

def draw_cat_plot():
    """
    Categorical plot:
    - Variables: cholesterol, gluc, smoke, alco, active, overweight
    - Dividido por cardio en columnas
    - Cuenta valores (0/1) por variable
    """
    # 4) Melt a formato largo
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"],
    )

    # 5) Agrupar y re-formatear (contar por cardio/variable/value)
    df_cat = (
        df_cat.groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )

    # 6) catplot (bar) con seaborn
    g = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar",
        height=5,
        aspect=1
    )
    g.set_axis_labels("variable", "total")
    g._legend.set_title("value")

    # 7) Obtener figura
    fig = g.fig

    return fig


def draw_heat_map():
    """
    Heatmap:
    - Limpiar datos:
      * ap_lo <= ap_hi
      * height entre 2.5 y 97.5 percentil
      * weight entre 2.5 y 97.5 percentil
    - Matriz de correlación con máscara triángulo superior
    """
    # 8) Limpiar
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))
    ].copy()

    # 9) Correlación
    corr = df_heat.corr(numeric_only=True)

    # 10) Máscara triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 11) Figura y 12) Heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    return fig
