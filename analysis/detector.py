import pandas as pd


def detect_dataset(df):
    """
    Analyze the uploaded dataset and detect its structure.
    """

    numeric_columns = list(
        df.select_dtypes(include=["number"]).columns
    )

    categorical_columns = list(
        df.select_dtypes(include=["object", "category"]).columns
    )

    datetime_columns = []

    # Try detecting date columns
    for col in df.columns:

        if "date" in col.lower():

            try:
                df[col] = pd.to_datetime(df[col])
                datetime_columns.append(col)
            except:
                pass

    return {
        "numeric": numeric_columns,
        "categorical": categorical_columns,
        "datetime": datetime_columns
    }