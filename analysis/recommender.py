import pandas as pd


def recommend_charts(df, dataset_info, semantic_info):
    """
    Recommend the best charts for the uploaded dataset.

    Priority:
    1. Use semantic detection (Sales, Profit, Revenue, etc.)
    2. Fall back to detected numeric/date columns
    """

    recommendations = []

    # -------------------------------
    # Select KPI Columns
    # -------------------------------

    numeric = []
    for col in semantic_info["kpi"]:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric.append(col)

    if not numeric:
        numeric = dataset_info["numeric"]

    # -------------------------------
    # Select Category Columns
    # -------------------------------

    categorical = semantic_info["category"]

    if not categorical:
        categorical = dataset_info["categorical"]

    # -------------------------------
    # Select Date Column
    # -------------------------------

    datetime_cols = []

    if semantic_info["date"] is not None:
        datetime_cols.append(semantic_info["date"])

    else:
        datetime_cols = dataset_info["datetime"]

    # -------------------------------
    # LINE CHART
    # -------------------------------

    if datetime_cols and numeric:

        recommendations.append({
            "type": "line",
            "x": datetime_cols[0],
            "y": numeric[0],
            "title": f"{numeric[0]} Over Time"
        })

    # -------------------------------
    # BAR CHART
    # -------------------------------

    if categorical and numeric:

        recommendations.append({
            "type": "bar",
            "x": categorical[0],
            "y": numeric[0],
            "title": f"{numeric[0]} by {categorical[0]}"
        })

    # -------------------------------
    # PIE CHART
    # Only if category has <=10 values
    # -------------------------------

    if categorical and numeric:

        try:

            unique = df[categorical[0]].nunique()

            if unique <= 10:

                recommendations.append({
                    "type": "pie",
                    "names": categorical[0],
                    "values": numeric[0],
                    "title": f"{numeric[0]} Distribution"
                })

        except:
            pass

    # -------------------------------
    # SCATTER PLOT
    # -------------------------------

    if len(numeric) >= 2:

        recommendations.append({
            "type": "scatter",
            "x": numeric[0],
            "y": numeric[1],
            "title": f"{numeric[0]} vs {numeric[1]}"
        })

    # -------------------------------
    # HISTOGRAM
    # -------------------------------

    if numeric:

        recommendations.append({
            "type": "histogram",
            "x": numeric[0],
            "title": f"Distribution of {numeric[0]}"
        })

    # -------------------------------
    # BOX PLOT
    # -------------------------------

    if numeric:

        recommendations.append({
            "type": "box",
            "y": numeric[0],
            "title": f"Outliers in {numeric[0]}"
        })

    # -------------------------------
    # CORRELATION HEATMAP
    # (Added in next phase)
    # -------------------------------

    if len(dataset_info["numeric"]) >= 2:

        recommendations.append({
            "type": "heatmap",
            "title": "Correlation Heatmap"
        })

    return recommendations