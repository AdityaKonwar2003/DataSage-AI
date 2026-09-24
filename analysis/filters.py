import pandas as pd


def apply_filters(df, filters):
    """
    Apply selected categorical filters to a DataFrame.

    Args:
        df: Original DataFrame
        filters: Dictionary containing column/value selections

    Returns:
        Filtered DataFrame
    """

    filtered_df = df.copy()

    for column, selected_values in filters.items():

        if column not in filtered_df.columns:
            continue

        if not selected_values:
            continue

        filtered_df = filtered_df[
            filtered_df[column].isin(selected_values)
        ]

    return filtered_df


def get_filter_options(df):
    """
    Return categorical columns and their unique values.
    """

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    filter_options = {}

    for column in categorical_columns:

        # Avoid filters with too many unique values
        if df[column].nunique(dropna=True) <= 30:

            values = (
                df[column]
                .dropna()
                .unique()
                .tolist()
            )

            filter_options[column] = sorted(
                values,
                key=lambda x: str(x)
            )

    return filter_options

