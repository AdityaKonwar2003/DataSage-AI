import pandas as pd
from analysis.correlation import analyze_correlations


def get_dataset_summary(df):

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (KB)": round(df.memory_usage(deep=True).sum() / 1024, 2)
    }

    return summary


def get_column_types(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })


def get_descriptive_statistics(df):
    """
    Returns descriptive statistics only for numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    stats = pd.DataFrame({
        "Mean": numeric_df.mean(),
        "Median": numeric_df.median(),
        "Minimum": numeric_df.min(),
        "Maximum": numeric_df.max(),
        "Std Dev": numeric_df.std()
    })

    return stats.round(2)

import pandas as pd


def build_ai_summary(df, dataset_info, semantic_info):

    summary = []

    summary.append("DATASET OVERVIEW")
    summary.append("----------------------------")

    summary.append(f"Rows: {len(df)}")
    summary.append(f"Columns: {len(df.columns)}")

    summary.append(
        f"Missing Values: {df.isnull().sum().sum()}"
    )

    summary.append(
        f"Duplicate Rows: {df.duplicated().sum()}"
    )

    summary.append("")
    summary.append("DESCRIPTIVE STATISTICS")
    summary.append("----------------------------")
    for col in semantic_info["kpi"]:
        try:
            summary.append(f"{col}")
            summary.append(
            f"Average: {df[col].mean():.2f}"
        )

            summary.append(
            f"Minimum: {df[col].min():.2f}"
        )

            summary.append(
            f"Maximum: {df[col].max():.2f}"
        )

            summary.append("")

        except:
            pass
    # ---------------- KPI ---------------- #

    if semantic_info["kpi"]:

        summary.append("KPI Columns:")

        for col in semantic_info["kpi"]:
            summary.append(f"- {col}")

        summary.append("")

    # ---------------- CATEGORY ---------------- #

    if semantic_info["category"]:

        summary.append("Category Columns:")

        for col in semantic_info["category"]:
            summary.append(f"- {col}")

        summary.append("")

    # ---------------- DATE ---------------- #

    if semantic_info["date"]:

        summary.append(
            f"Date Column: {semantic_info['date']}"
        )

        summary.append("")

    # ---------------- TOP VALUES ---------------- #

    for cat in semantic_info["category"][:2]:

        try:

            top = df[cat].value_counts().idxmax()

            summary.append(
                f"Most Common {cat}: {top}"
            )

        except:

            pass
    # ---------------- CORRELATION ---------------- #

    correlation = analyze_correlations(df)
    if correlation:
        summary.append("")
        summary.append("CORRELATION ANALYSIS")
        summary.append("----------------------------")

        if correlation["positive"]:
            p = correlation["positive"]

            summary.append(
            f"Strongest Positive: "
            f"{p['Column 1']} ↔ {p['Column 2']} "
            f"({p['Correlation']})"
        )

        if correlation["negative"]:
            n = correlation["negative"]

            summary.append(
            f"Strongest Negative: "
            f"{n['Column 1']} ↔ {n['Column 2']} "
            f"({n['Correlation']})"
        )


    return "\n".join(summary)

