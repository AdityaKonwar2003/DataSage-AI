import pandas as pd


def analyze_question(df, question):
    """
    Analyze a user question using the actual dataset
    and return factual context for the LLM.
    """

    question_lower = question.lower()

    context = []

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    context.append("DATASET INFORMATION")
    context.append(f"Rows: {len(df)}")
    context.append(f"Columns: {len(df.columns)}")

    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    context.append("\nAVAILABLE COLUMNS")

    for col in df.columns:
        context.append(
            f"- {col} ({df[col].dtype})"
        )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # =====================================================
    # NUMERIC QUESTION
    # =====================================================

    for col in numeric_columns:

        col_lower = col.lower()

        if col_lower in question_lower:

            series = df[col].dropna()

            if series.empty:
                continue

            if any(word in question_lower for word in [
                "average",
                "mean"
            ]):

                context.append(
                    f"\n{col} Statistics"
                )

                context.append(
                    f"Average: {series.mean():.2f}"
                )

                context.append(
                    f"Minimum: {series.min():.2f}"
                )

                context.append(
                    f"Maximum: {series.max():.2f}"
                )

            elif any(word in question_lower for word in [
                "maximum",
                "highest",
                "largest",
                "max"
            ]):

                context.append(
                    f"\n{col} Maximum"
                )

                context.append(
                    f"Maximum value: {series.max():.2f}"
                )

                max_index = series.idxmax()

                context.append(
                    f"Corresponding row: "
                    f"{df.loc[max_index].to_dict()}"
                )

            elif any(word in question_lower for word in [
                "minimum",
                "lowest",
                "smallest",
                "min"
            ]):

                context.append(
                    f"\n{col} Minimum"
                )

                context.append(
                    f"Minimum value: {series.min():.2f}"
                )

                min_index = series.idxmin()

                context.append(
                    f"Corresponding row: "
                    f"{df.loc[min_index].to_dict()}"
                )

            elif any(word in question_lower for word in [
                "total",
                "sum"
            ]):

                context.append(
                    f"\n{col} Total"
                )

                context.append(
                    f"Total: {series.sum():.2f}"
                )

    # =====================================================
    # CATEGORY QUESTIONS
    # =====================================================

    for col in categorical_columns:

        if col.lower() not in question_lower:
            continue

        if any(word in question_lower for word in [
            "most",
            "highest",
            "top",
            "popular"
        ]):

            counts = (
                df[col]
                .value_counts()
                .head(10)
            )

            context.append(
                f"\nMost Common Values in {col}"
            )

            for value, count in counts.items():

                context.append(
                    f"{value}: {count}"
                )

    # =====================================================
    # CORRELATION QUESTIONS
    # =====================================================

    if any(word in question_lower for word in [
        "correlation",
        "relationship",
        "related"
    ]):

        if len(numeric_columns) >= 2:

            correlation = (
                df[numeric_columns]
                .corr()
                .round(2)
            )

            context.append(
                "\nCORRELATION MATRIX"
            )

            context.append(
                correlation.to_string()
            )

    # =====================================================
    # MISSING DATA
    # =====================================================

    if any(word in question_lower for word in [
        "missing",
        "null",
        "incomplete"
    ]):

        missing = df.isnull().sum()

        context.append(
            "\nMISSING VALUES"
        )

        for col, count in missing.items():

            if count > 0:

                context.append(
                    f"{col}: {count}"
                )

    # =====================================================
    # FALLBACK
    # =====================================================

    if len(context) <= 5:

        context.append(
            "\nNo specific calculation was identified "
            "for this question."
        )

        context.append(
            "Use the available dataset information "
            "to determine whether the question can "
            "be answered."
        )

    return "\n".join(context)