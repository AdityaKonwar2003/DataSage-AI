import pandas as pd


def detect_anomalies(df):
    """
    Detect numerical anomalies using the IQR method.

    Returns:
        anomaly_data: DataFrame containing rows with anomalies
        anomaly_summary: Summary of anomalies by column
    """

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if not numeric_columns:
        return pd.DataFrame(), []

    anomaly_rows = set()
    anomaly_summary = []

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        # Calculate Q1 and Q3
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        # Interquartile Range
        iqr = q3 - q1

        # Lower and upper limits
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Find anomalies
        mask = (df[column] < lower_bound) | (df[column] > upper_bound)

        anomaly_indices = df.index[mask]

        if len(anomaly_indices) > 0:

            anomaly_rows.update(anomaly_indices.tolist())

            anomaly_summary.append({
                "Column": column,
                "Anomalies": len(anomaly_indices),
                "Lower Bound": round(lower_bound, 2),
                "Upper Bound": round(upper_bound, 2)
            })

    # Get complete rows containing anomalies
    if anomaly_rows:
        anomaly_data = df.loc[sorted(anomaly_rows)].copy()
    else:
        anomaly_data = pd.DataFrame()

    return anomaly_data, anomaly_summary