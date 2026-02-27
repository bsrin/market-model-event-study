import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = "analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use("dark_background")

PRIMARY_RED = "#E10600"
BAND_COLOR = "#880000"
GRID_COLOR = "#444444"
TEXT_COLOR = "#FFFFFF"


def plot_average_path(avg_df, ticker, event_name="Event"):
    fig, ax = plt.subplots(figsize=(10, 6))

    # The Average Path (MCAR)
    ax.plot(
        avg_df.index,
        avg_df["mcar"],
        color=PRIMARY_RED,
        linewidth=2.5,
        label="Mean Cumulative Abnormal Return"
    )

    # 95% Confidence Intervals (1.96 * Standard Error)
    ci_upper = avg_df["mcar"] + (1.96 * avg_df["std_error"])
    ci_lower = avg_df["mcar"] - (1.96 * avg_df["std_error"])

    ax.fill_between(
        avg_df.index,
        ci_lower,
        ci_upper,
        color=BAND_COLOR,
        alpha=0.3,
        label="95% Confidence Interval"
    )

    # Crosshairs
    ax.axvline(0, color="#888888", linestyle="--", linewidth=1.2)
    ax.axhline(0, color="#555555", linestyle=":", linewidth=1)

    ax.set_title(f"Cumulative Abnormal Returns Around {event_name} - {ticker}", fontsize=16, color=TEXT_COLOR, pad=15)
    ax.set_xlabel("Trading Days Relative to Event", fontsize=13, color=TEXT_COLOR)
    ax.set_ylabel("Cumulative Abnormal Return (CAR)", fontsize=13, color=TEXT_COLOR)

    ax.grid(color=GRID_COLOR, alpha=0.3)
    ax.tick_params(colors=TEXT_COLOR)
    legend = ax.legend(loc="upper left", frameon=False)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.tight_layout()
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/{ticker}_car_plot.png", dpi=300)
    plt.show()