import pandas as pd


def analyze_correlations(df):
    """
    Analyze correlations between numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    relationships = []

    cols = corr.columns

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):

            value = round(corr.iloc[i, j], 2)

            relationships.append({
                "Column 1": cols[i],
                "Column 2": cols[j],
                "Correlation": value
            })

    relationships.sort(
        key=lambda x: abs(x["Correlation"]),
        reverse=True
    )

    positive = None
    negative = None

    for r in relationships:

        if r["Correlation"] > 0 and positive is None:
            positive = r

        if r["Correlation"] < 0 and negative is None:
            negative = r

        if positive and negative:
            break

    return {
        "matrix": corr,
        "table": relationships,
        "positive": positive,
        "negative": negative
    }