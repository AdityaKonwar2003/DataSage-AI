import pandas as pd


def get_chart_insight(chart, df):

    chart_type = chart["type"]

    # ---------------- LINE CHART ---------------- #

    if chart_type == "line":

        column = chart["y"]

        series = pd.to_numeric(df[column], errors="coerce").dropna()

        if series.empty:
            return "No numeric data available for trend analysis."

        start = series.iloc[0]
        end = series.iloc[-1]

        if end > start:
            trend = "increased"
        elif end < start:
            trend = "decreased"
        else:
            trend = "remained stable"

        return (
            f"📈 **Trend Analysis**\n\n"
            f"The **{column}** has **{trend}** over time.\n\n"
            f"Start: **{start:.2f}**\n"
            f"End: **{end:.2f}**"
        )

    # ---------------- BAR CHART ---------------- #

    elif chart_type == "bar":

        category = chart["x"]
        value = chart["y"]

        series = pd.to_numeric(df[value], errors="coerce")

        grouped = (
            pd.DataFrame({
                category: df[category],
                value: series
            })
            .dropna()
            .groupby(category)[value]
            .sum()
            .sort_values(ascending=False)
        )

        if grouped.empty:
            return "No valid numeric data found."

        highest = grouped.idxmax()
        highest_value = grouped.max()

        lowest = grouped.idxmin()
        lowest_value = grouped.min()

        return (
            f"📊 **Category Analysis**\n\n"
            f"🏆 Highest Category: **{highest}**\n"
            f"Value: **{highest_value:.2f}**\n\n"
            f"📉 Lowest Category: **{lowest}**\n"
            f"Value: **{lowest_value:.2f}**"
        )

    # ---------------- PIE CHART ---------------- #

    elif chart_type == "pie":

        category = chart["names"]
        value = chart["values"]

        series = pd.to_numeric(df[value], errors="coerce")

        grouped = (
            pd.DataFrame({
                category: df[category],
                value: series
            })
            .dropna()
            .groupby(category)[value]
            .sum()
            .sort_values(ascending=False)
        )

        if grouped.empty:
            return "No numeric values available for pie chart."

        top = grouped.idxmax()

        total = grouped.sum()

        if total == 0:
            return "Cannot calculate percentage."

        percent = grouped.max() / total * 100

        return (
            f"🥧 **Distribution Insight**\n\n"
            f"**{top}** contributes **{percent:.1f}%** of the total."
        )

    # ---------------- SCATTER ---------------- #

    elif chart_type == "scatter":

        x = chart["x"]
        y = chart["y"]

        x_series = pd.to_numeric(df[x], errors="coerce")
        y_series = pd.to_numeric(df[y], errors="coerce")

        corr = x_series.corr(y_series)

        if pd.isna(corr):
            return "Not enough numeric data to calculate correlation."

        if corr >= 0.7:
            relation = "strong positive"
        elif corr >= 0.3:
            relation = "moderate positive"
        elif corr <= -0.7:
            relation = "strong negative"
        elif corr <= -0.3:
            relation = "moderate negative"
        else:
            relation = "weak"

        return (
            f"📉 **Relationship Analysis**\n\n"
            f"There is a **{relation} relationship** between "
            f"**{x}** and **{y}**.\n\n"
            f"Correlation = **{corr:.2f}**"
        )

    # ---------------- HISTOGRAM ---------------- #

    elif chart_type == "histogram":

        column = chart["x"]

        series = pd.to_numeric(df[column], errors="coerce").dropna()

        if series.empty:
            return "No numeric data."

        mean = series.mean()
        median = series.median()

        if mean > median:
            skew = "right-skewed"
        elif mean < median:
            skew = "left-skewed"
        else:
            skew = "approximately symmetric"

        return (
            f"📦 **Distribution Analysis**\n\n"
            f"Average: **{mean:.2f}**\n\n"
            f"Median: **{median:.2f}**\n\n"
            f"The data appears **{skew}**."
        )

    # ---------------- BOX PLOT ---------------- #

    elif chart_type == "box":

        column = chart["y"]

        series = pd.to_numeric(df[column], errors="coerce").dropna()

        if series.empty:
            return "No numeric data."

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = series[
            (series < lower) |
            (series > upper)
        ].count()

        return (
            f"📦 **Outlier Analysis**\n\n"
            f"Detected **{outliers}** potential outliers."
        )

    # ---------------- HEATMAP ---------------- #

    elif chart_type == "heatmap":

        return (
            "🔥 **Correlation Analysis**\n\n"
            "The heatmap highlights positive and negative relationships "
            "between numeric variables."
        )

    return "No insight available."

def build_chart_context(chart, df):

    chart_type = chart["type"]

    context = []

    context.append(f"Chart Type: {chart_type}")

    if chart_type == "bar":

        category = chart["x"]
        value = chart["y"]

        grouped = (
            df.groupby(category)[value]
            .sum()
            .sort_values(ascending=False)
        )

        context.append(f"Category Column: {category}")
        context.append(f"Value Column: {value}")

        context.append("Top Categories:")

        for index, val in grouped.head(5).items():
            context.append(f"{index}: {val}")

    elif chart_type == "pie":

        category = chart["names"]
        value = chart["values"]

        grouped = (
            df.groupby(category)[value]
            .sum()
            .sort_values(ascending=False)
        )

        context.append(f"Category Column: {category}")
        context.append(f"Value Column: {value}")

        context.append("Distribution:")

        for index, val in grouped.items():
            context.append(f"{index}: {val}")

    elif chart_type == "line":

        context.append(
            f"Trend Column: {chart['y']}"
        )

    elif chart_type == "scatter":

        context.append(
            f"Variables: {chart['x']} vs {chart['y']}"
        )

    return "\n".join(context)
