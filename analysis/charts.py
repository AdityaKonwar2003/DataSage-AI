import os

import plotly.express as px
import plotly.graph_objects as go


def generate_charts(df, recommendations):
    """
    Generate Plotly charts based on recommendations.
    """

    figures = []

    for chart in recommendations:

        chart_type = chart["type"]

        try:

            # ---------------- LINE ---------------- #

            if chart_type == "line":

                fig = px.line(
                    df,
                    x=chart["x"],
                    y=chart["y"],
                    title=chart["title"],
                    markers=True
                )

            # ---------------- BAR ---------------- #

            elif chart_type == "bar":

                grouped = (
                    df.groupby(chart["x"])[chart["y"]]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    grouped,
                    x=chart["x"],
                    y=chart["y"],
                    title=chart["title"]
                )

            # ---------------- PIE ---------------- #

            elif chart_type == "pie":

                grouped = (
                    df.groupby(chart["names"])[chart["values"]]
                    .sum()
                    .reset_index()
                )

                fig = px.pie(
                    grouped,
                    names=chart["names"],
                    values=chart["values"],
                    title=chart["title"],
                    hole=0.4
                )

            # ---------------- SCATTER ---------------- #

            elif chart_type == "scatter":

                fig = px.scatter(
                    df,
                    x=chart["x"],
                    y=chart["y"],
                    title=chart["title"]
                )

            # ---------------- HISTOGRAM ---------------- #

            elif chart_type == "histogram":

                fig = px.histogram(
                    df,
                    x=chart["x"],
                    title=chart["title"]
                )

            # ---------------- BOX ---------------- #

            elif chart_type == "box":

                fig = px.box(
                    df,
                    y=chart["y"],
                    title=chart["title"]
                )

            # ---------------- HEATMAP ---------------- #

            elif chart_type == "heatmap":

                corr = df.select_dtypes(include="number").corr()

                fig = px.imshow(
                    corr,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale="RdBu_r",
                    title="Correlation Heatmap"
                )

            else:
                continue

            fig.update_layout(height=500)

            # -------------------------------------------------
            # Save chart for PDF (don't stop app if it fails)
            # -------------------------------------------------

            try:

                os.makedirs("report/charts", exist_ok=True)

                chart_index = len(figures) + 1

                fig.write_image(
                    f"report/charts/chart_{chart_index}.png",
                    width=1200,
                    height=700
                )

            except Exception as e:

                pass

            # Always keep the figure for Streamlit
            figures.append(fig)

        except Exception as e:

            print(f"Chart generation failed: {e}")

            continue

    return figures