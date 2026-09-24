import pandas as pd


def recommend_charts(df, dataset_info, semantic_info):
    """
    Automatically recommend useful general-purpose charts
    for an unknown dataset.

    Priority:
    1. Semantically detected KPI/category/date columns
    2. Dataset-level numeric/category/date columns
    3. General fallback charts

    The function does not require the user to know anything
    about the dataset.
    """

    recommendations = []

    # ============================================================
    # 1. NUMERIC / KPI COLUMNS
    # ============================================================

    numeric = []

    # First use semantically detected KPI columns
    for col in semantic_info.get("kpi", []):
        if (
            col in df.columns
            and pd.api.types.is_numeric_dtype(df[col])
        ):
            numeric.append(col)

    # Fall back to all numeric columns
    if not numeric:
        numeric = [
            col for col in dataset_info.get("numeric", [])
            if col in df.columns
            and pd.api.types.is_numeric_dtype(df[col])
        ]

    # Remove duplicates while preserving order
    numeric = list(dict.fromkeys(numeric))

    # ============================================================
    # 2. CATEGORICAL COLUMNS
    # ============================================================

    categorical = []

    for col in semantic_info.get("category", []):
        if col in df.columns:
            categorical.append(col)

    # Fall back to dataset categorical columns
    if not categorical:
        categorical = [
            col for col in dataset_info.get("categorical", [])
            if col in df.columns
        ]

    categorical = list(dict.fromkeys(categorical))

    # ============================================================
    # 3. DATE / TIME COLUMNS
    # ============================================================

    datetime_cols = []

    semantic_date = semantic_info.get("date")

    if semantic_date is not None:
        if semantic_date in df.columns:
            datetime_cols.append(semantic_date)

    if not datetime_cols:
        datetime_cols = [
            col for col in dataset_info.get("datetime", [])
            if col in df.columns
        ]

    datetime_cols = list(dict.fromkeys(datetime_cols))

    # ============================================================
    # 4. GENERAL TREND CHART
    # ============================================================

    if datetime_cols and numeric:

        recommendations.append({
            "type": "line",
            "x": datetime_cols[0],
            "y": numeric[0],
            "title": f"{numeric[0]} Over Time"
        })

    # ============================================================
    # 5. GENERAL CATEGORY COMPARISON
    # ============================================================

    if categorical and numeric:

        category_column = categorical[0]

        # Avoid extremely high-cardinality columns
        if df[category_column].nunique(dropna=True) <= 30:

            recommendations.append({
                "type": "bar",
                "x": category_column,
                "y": numeric[0],
                "title": f"{numeric[0]} by {category_column}"
            })

    # ============================================================
    # 6. CATEGORY DISTRIBUTION
    # ============================================================

    if categorical and numeric:

        category_column = categorical[0]

        try:

            unique_count = df[category_column].nunique(
                dropna=True
            )

            if 2 <= unique_count <= 8:

                recommendations.append({
                    "type": "pie",
                    "names": category_column,
                    "values": numeric[0],
                    "title": f"{numeric[0]} Distribution by {category_column}"
                })

        except Exception:
            pass

    # ============================================================
    # 7. NUMERIC RELATIONSHIP
    # ============================================================

    if len(numeric) >= 2:

        recommendations.append({
            "type": "scatter",
            "x": numeric[0],
            "y": numeric[1],
            "title": f"{numeric[0]} vs {numeric[1]}"
        })

    # ============================================================
    # 8. NUMERIC DISTRIBUTION
    # ============================================================

    if numeric:

        recommendations.append({
            "type": "histogram",
            "x": numeric[0],
            "title": f"Distribution of {numeric[0]}"
        })

    # ============================================================
    # 9. OUTLIER VIEW
    # ============================================================

    if numeric:

        recommendations.append({
            "type": "box",
            "y": numeric[0],
            "title": f"Outliers in {numeric[0]}"
        })

    # ============================================================
    # 10. CORRELATION HEATMAP
    # ============================================================

    if len(numeric) >= 2:

        recommendations.append({
            "type": "heatmap",
            "title": "Correlation Heatmap"
        })

    # ============================================================
    # REMOVE DUPLICATE CHART TYPES / COMBINATIONS
    # ============================================================

    unique_recommendations = []

    seen = set()

    for recommendation in recommendations:

        key = (
            recommendation["type"],
            recommendation.get("x"),
            recommendation.get("y"),
            recommendation.get("names"),
            recommendation.get("values")
        )

        if key not in seen:

            seen.add(key)
            unique_recommendations.append(
                recommendation
            )

    # ============================================================
    # LIMIT AUTOMATIC CHARTS
    # ============================================================

    # Keep the dashboard useful without generating too many charts.
    return unique_recommendations[:7]