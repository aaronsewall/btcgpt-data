import pandas as pd
import json
import urllib.request
import numpy as np
import os

# Download latest output.json
url = "https://raw.githubusercontent.com/btcgpt/data/main/output.json"
filename = os.path.join(
    os.path.expanduser("~"), "src/github.com/aaronsewall/btcgpt-data/output.json"
)
urllib.request.urlretrieve(url, filename)


def direction(price_diff: float) -> str:
    """Determine price direction given a price diff"""
    if pd.isna(price_diff):
        return np.nan
    elif price_diff == 0:
        return "same"
    elif price_diff > 0:
        return "up"
    return "down"


# Read in output.json
with open(filename) as f:
    output = json.load(f)

# Create series of actual, pred past for hour, day and week models.
hour_actual_s = pd.Series({l["x"]: l["y"] for l in output["hour"]["actual"]}, name="price_actual")
hour_pred_past_s = pd.Series(
    {l["x"]: l["y"] for l in output["hour"]["pred_past"]}, name="price_pred_past"
)
day_actual_s = pd.Series({l["x"]: l["y"] for l in output["day"]["actual"]}, name="price_actual")
day_pred_past_s = pd.Series(
    {l["x"]: l["y"] for l in output["day"]["pred_past"]}, name="price_pred_past"
)
week_actual_s = pd.Series({l["x"]: l["y"] for l in output["week"]["actual"]}, name="price_actual")
week_pred_past_s = pd.Series(
    {l["x"]: l["y"] for l in output["week"]["pred_past"]}, name="price_pred_past"
)

# Create dataframes for hour, day and week historical models.
hour_historical_df = pd.concat([hour_pred_past_s, hour_actual_s], axis="columns").assign(
    price_pred_diff=lambda df: df.price_pred_past - df.price_actual.shift(1),
    price_actual_diff=lambda df: df.price_actual - df.price_actual.shift(1),
    price_diff=lambda df: (df.price_pred_diff - df.price_actual_diff).abs(),
    pred_direction=lambda df: df.price_pred_diff.apply(direction),
    actual_direction=lambda df: df.price_actual_diff.apply(direction),
    correct=lambda df: df.pred_direction == df.actual_direction,
)
day_historical_df = pd.concat([day_pred_past_s, day_actual_s], axis="columns").assign(
    price_pred_diff=lambda df: df.price_pred_past - df.price_actual.shift(1),
    price_actual_diff=lambda df: df.price_actual - df.price_actual.shift(1),
    pred_direction=lambda df: df.price_pred_diff.apply(direction),
    actual_direction=lambda df: df.price_actual_diff.apply(direction),
    correct=lambda df: df.pred_direction == df.actual_direction,
)
week_historical_df = pd.concat([week_pred_past_s, week_actual_s], axis="columns").assign(
    price_pred_diff=lambda df: df.price_pred_past - df.price_actual.shift(1),
    price_actual_diff=lambda df: df.price_actual - df.price_actual.shift(1),
    pred_direction=lambda df: df.price_pred_diff.apply(direction),
    actual_direction=lambda df: df.price_actual_diff.apply(direction),
    correct=lambda df: df.pred_direction == df.actual_direction,
)

print(f"Hour correct pct: {hour_historical_df.correct.sum()/hour_historical_df.correct.size}")
print(f"Day correct pct: {day_historical_df.correct.sum()/day_historical_df.correct.size}")
print(f"Week correct pct: {week_historical_df.correct.sum()/week_historical_df.correct.size}")
