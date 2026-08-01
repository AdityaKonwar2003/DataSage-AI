import pandas as pd


def clean_data(df):
    """
    Cleans the uploaded dataset and returns:
    - cleaned dataframe
    - cleaning report
    """

    report = []

    # -------------------------------
    # Remove extra spaces in column names
    # -------------------------------
    old_columns = list(df.columns)

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    if old_columns != list(df.columns):
        report.append("✅ Cleaned column names.")

    # -------------------------------
    # Remove duplicate rows
    # -------------------------------
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        df = df.drop_duplicates()
        report.append(f"✅ Removed {duplicates} duplicate rows.")
    else:
        report.append("✅ No duplicate rows found.")

    # -------------------------------
    # Detect missing values
    # -------------------------------
    missing = df.isnull().sum()

    missing_columns = missing[missing > 0]

    if len(missing_columns) > 0:

        report.append(
            f"⚠️ Missing values found in {len(missing_columns)} column(s)."
        )

    else:

        report.append("✅ No missing values found.")

    # -------------------------------
    # Convert possible date columns
    # -------------------------------

    converted = []

    for col in df.columns:

        if "date" in col.lower():

            try:

                df[col] = pd.to_datetime(df[col])

                converted.append(col)

            except:

                pass

    if converted:

        report.append(
            f"✅ Converted date column(s): {', '.join(converted)}"
        )

    return df, report