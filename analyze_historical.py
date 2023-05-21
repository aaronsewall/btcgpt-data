import pandas as pd
import json
import numpy as np
import os

filepath = os.path.join(
    os.path.expanduser("~"), "src/github.com/aaronsewall/btcgpt-data/content-dumps"
)


def direction(price_diff: float) -> np.nan:
    if pd.isna(price_diff):
        return np.nan
    elif price_diff == 0:
        return "same"
    elif price_diff > 0:
        return "up"
    return "down"


outputs = []

for file_ in sorted(os.listdir(filepath), key=lambda x: int(x.split("_")[0]), reverse=True):
    with open(os.path.join(filepath, file_)) as f:
        outputs.append(json.load(f))

hour_actuals_dict = {
    l["x"]: l["y"] for o in [o["hour"]["actual"] for o in outputs if "hour" in o] for l in o
}
hour_pred_pasts_dict = {
    l["x"]: l["y"] for o in [o["hour"]["pred_past"] for o in outputs if "hour" in o] for l in o
}

day_actuals_dict = {
    l["x"]: l["y"] for o in [o["day"]["actual"] for o in outputs if "day" in o] for l in o
}
day_pred_pasts_dict = {
    l["x"]: l["y"] for o in [o["day"]["pred_past"] for o in outputs if "day" in o] for l in o
}

week_actuals_dict = {
    l["x"]: l["y"] for o in [o["week"]["actual"] for o in outputs if "week" in o] for l in o
}
week_pred_pasts_dict = {
    l["x"]: l["y"] for o in [o["week"]["pred_past"] for o in outputs if "week" in o] for l in o
}
total_hour_actuals_df = pd.Series(hour_actuals_dict, name="price_actual")
total_hour_pred_pasts_df = pd.Series(hour_pred_pasts_dict, name="price_pred_past")
total_day_actuals_df = pd.Series(day_actuals_dict, name="price_actual")
total_day_pred_pasts_df = pd.Series(day_pred_pasts_dict, name="price_pred_past")
total_week_actuals_df = pd.Series(week_actuals_dict, name="price_actual")
total_week_pred_pasts_df = pd.Series(week_pred_pasts_dict, name="price_pred_past")

total_hour_historical_df = pd.concat(
    [total_hour_actuals_df, total_hour_pred_pasts_df], axis="columns"
).assign(
    price_pred_diff=lambda df: df.price_pred_past - df.price_actual.shift(1),
    price_actual_diff=lambda df: df.price_actual - df.price_actual.shift(1),
    price_diff_abs=lambda df: (df.price_pred_diff - df.price_actual_diff).abs(),
    pred_direction=lambda df: df.price_pred_diff.apply(direction),
    actual_direction=lambda df: df.price_actual_diff.apply(direction),
    correct=lambda df: df.pred_direction == df.actual_direction,
)
total_day_historical_df = pd.concat(
    [total_day_actuals_df, total_day_pred_pasts_df], axis="columns"
).assign(
    price_pred_diff=lambda df: df.price_pred_past - df.price_actual.shift(1),
    price_actual_diff=lambda df: df.price_actual - df.price_actual.shift(1),
    price_diff_abs=lambda df: (df.price_pred_diff - df.price_actual_diff).abs(),
    pred_direction=lambda df: df.price_pred_diff.apply(direction),
    actual_direction=lambda df: df.price_actual_diff.apply(direction),
    correct=lambda df: df.pred_direction == df.actual_direction,
)
total_week_historical_df = pd.concat(
    [total_week_actuals_df, total_week_pred_pasts_df], axis="columns"
).assign(
    price_pred_diff=lambda df: df.price_pred_past - df.price_actual.shift(1),
    price_actual_diff=lambda df: df.price_actual - df.price_actual.shift(1),
    price_diff_abs=lambda df: (df.price_pred_diff - df.price_actual_diff).abs(),
    pred_direction=lambda df: df.price_pred_diff.apply(direction),
    actual_direction=lambda df: df.price_actual_diff.apply(direction),
    correct=lambda df: df.pred_direction == df.actual_direction,
)
print(f"Hour correct pct: {total_hour_historical_df.correct.sum()/total_hour_historical_df.correct.size}")
print(f"Day correct pct: {total_day_historical_df.correct.sum()/total_day_historical_df.correct.size}")
print(f"Week correct pct: {total_week_historical_df.correct.sum()/total_week_historical_df.correct.size}")
