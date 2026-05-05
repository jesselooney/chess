# Written with assistance from Google Gemini.

import altair as alt
import pandas as pd
from pathlib import Path

PLAYERS = [
    "random",
    "nega-pieces-1",
    "nega-center-1",
    "nega-aggro-1",
    "nega-attack-1",
    "nega-pieces-2",
    "nega-center-2",
    "nega-aggro-2",
    "nega-attack-2",
    "nega-pieces-3",
    "nega-center-3",
    "nega-aggro-3",
    "nega-attack-3",
    "mcts-05-10k-random",
    "mcts-10-10k-random",
    "mcts-full-1k-random",
    "mcts-05-10k-epsilon-75",
    "mcts-10-10k-epsilon-75",
    "mcts-05-10k-epsilon-95",
    "mcts-10-10k-epsilon-95",
]

PLOT_CONFIGS = [
    {
        "input": "data/heatmap_score_mean.csv",
        "output": "plots/heatmap_score_mean.svg",
        "value_col": "score_mean",
        "title": "Mean Game Score",
        "scale_type": "linear",
    },
    {
        "input": "data/heatmap_time_ratio_mean.csv",
        "output": "plots/heatmap_time_ratio_mean.svg",
        "value_col": "time_ratio_mean",
        "title": "Mean Time Ratio",
        "scale_type": "log",
    },
]


def generate_matchup_heatmap(
    df: pd.DataFrame, value_col: str, title: str, scale_type: str = "linear"
) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X(
                "black:N",
                sort=PLAYERS,
                title="Black Player",
                scale=alt.Scale(domain=PLAYERS),
            ),
            y=alt.Y(
                "white:N",
                sort=PLAYERS,
                scale=alt.Scale(domain=PLAYERS, reverse=True),
                title="White Player",
            ),
            color=alt.Color(
                f"{value_col}:Q",
                scale=alt.Scale(type=scale_type, scheme="viridis"),
                title=title,
            ),
            tooltip=["black:N", "white:N", f"{value_col}:Q"],
        )
        .properties(width=500, height=500)
    )


def main():
    # Ensure output directory exists
    Path("plots").mkdir(parents=True, exist_ok=True)

    for index, config in enumerate(PLOT_CONFIGS):
        try:
            df = pd.read_csv(config["input"])

            chart = generate_matchup_heatmap(
                df, config["value_col"], config["title"], config["scale_type"]
            )

            chart.save(config["output"])
            print(f"Wrote {config['output']}")

        except FileNotFoundError:
            print(f"Error: Could not find {config['input']}")
        except Exception as e:
            print(f"Error while processing config {index}: {e}")


if __name__ == "__main__":
    main()
