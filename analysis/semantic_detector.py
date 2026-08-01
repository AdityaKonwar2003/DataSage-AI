import pandas as pd


def detect_semantics(df):
    """
     Identify business semantics such as KPIs,
    categories, date columns and identifiers.
    """

    semantic = {
        "date": None,
        "kpi": [],
        "category": [],
        "identifier": [],
        "other_numeric": []
    }

    for col in df.columns:

        name = col.lower()

        # ---------------- DATE ---------------- #

        if any(word in name for word in [
            "date",
            "time",
            "day",
            "month",
            "year"
        ]):

            semantic["date"] = col
            continue

        # ---------------- IDENTIFIER ---------------- #

        if any(word in name for word in [
            "id",
            "code",
            "number",
            "index"
        ]):

            semantic["identifier"].append(col)
            continue

        # ---------------- NUMERIC ---------------- #

        if pd.api.types.is_numeric_dtype(df[col]):

            if any(word in name for word in [
                "sales",
                "revenue",
                "profit",
                "income",
                "amount",
                "price",
                "cost",
                "quantity",
                "qty",
                "unit",
                "salary",
                "score",
                "marks"
            ]):

                semantic["kpi"].append(col)

            else:

                semantic["other_numeric"].append(col)

            continue

        # ---------------- CATEGORY ---------------- #

        semantic["category"].append(col)

    return semantic