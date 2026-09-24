import pandas as pd


def analyze_root_causes(df, target_column):
    """
    Analyze categorical dimensions to identify groups
    associated with unusually high or low target values.
    """

    if target_column not in df.columns:
        return []

    if not pd.api.types.is_numeric_dtype(df[target_column]):
        return []

    numeric_series = df[target_column].dropna()

    if numeric_series.empty:
        return []

    overall_mean = numeric_series.mean()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    results = []

    for column in categorical_columns:

        if column == target_column:
            continue

        # Avoid extremely high-cardinality columns
        if df[column].nunique(dropna=True) > 50:
            continue

        grouped = (
            df.groupby(column, dropna=True)[target_column]
            .agg(["mean", "count"])
            .reset_index()
        )

        # Only consider groups with enough observations
        grouped = grouped[grouped["count"] >= 3]

        if grouped.empty:
            continue

        grouped["difference"] = (
            grouped["mean"] - overall_mean
        )

        grouped["difference_percent"] = (
            grouped["difference"]
            / overall_mean
            * 100
        )

        # Find highest and lowest performing groups
        highest = grouped.loc[grouped["mean"].idxmax()]
        lowest = grouped.loc[grouped["mean"].idxmin()]

        results.append({
            "column": column,
            "highest_group": str(highest[column]),
            "highest_mean": round(float(highest["mean"]), 2),
            "highest_count": int(highest["count"]),
            "highest_difference_percent": round(
                float(highest["difference_percent"]), 2
            ),
            "lowest_group": str(lowest[column]),
            "lowest_mean": round(float(lowest["mean"]), 2),
            "lowest_count": int(lowest["count"]),
            "lowest_difference_percent": round(
                float(lowest["difference_percent"]), 2
            )
        })

    # Sort dimensions by the largest difference
    results.sort(
        key=lambda x: max(
            abs(x["highest_difference_percent"]),
            abs(x["lowest_difference_percent"])
        ),
        reverse=True
    )

    return results