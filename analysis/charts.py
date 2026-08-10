import os

import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go


def generate_charts(df, recommendations):
    """
    Generate interactive Plotly charts for Streamlit
    and static PNG charts for PDF reports.
    """

    figures = []

    # Create PDF chart directory
    os.makedirs("report/charts", exist_ok=True)

    for chart in recommendations:

        chart_type = chart["type"]

        try:

            # =====================================================
            # LINE
            # =====================================================

            if chart_type == "line":

                fig = px.line(
                    df,
                    x=chart["x"],
                    y=chart["y"],
                    title=chart["title"],
                    markers=True
                )

            # =====================================================
            # BAR
            # =====================================================

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

            # =====================================================
            # PIE
            # =====================================================

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

            # =====================================================
            # SCATTER
            # =====================================================

            elif chart_type == "scatter":

                fig = px.scatter(
                    df,
                    x=chart["x"],
                    y=chart["y"],
                    title=chart["title"]
                )

            # =====================================================
            # HISTOGRAM
            # =====================================================

            elif chart_type == "histogram":

                fig = px.histogram(
                    df,
                    x=chart["x"],
                    title=chart["title"]
                )

            # =====================================================
            # BOX
            # =====================================================

            elif chart_type == "box":

                fig = px.box(
                    df,
                    y=chart["y"],
                    title=chart["title"]
                )

            # =====================================================
            # HEATMAP
            # =====================================================

            elif chart_type == "heatmap":

                corr = df.select_dtypes(
                    include="number"
                ).corr()

                fig = px.imshow(
                    corr,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale="RdBu_r",
                    title="Correlation Heatmap"
                )

            else:

                continue

            # =====================================================
            # PLOTLY SETTINGS
            # =====================================================

            fig.update_layout(
                height=500
            )

            # =====================================================
            # CREATE STATIC PNG FOR PDF
            # =====================================================

            chart_index = len(figures) + 1

            chart_path = (
                f"report/charts/chart_{chart_index}.png"
            )

            try:

                create_static_chart(
                    df,
                    chart,
                    chart_type,
                    chart_path
                )

            except Exception as e:

                print(
                    f"Static chart creation failed: {e}"
                )

            # =====================================================
            # KEEP PLOTLY FIGURE FOR STREAMLIT
            # =====================================================

            figures.append(fig)

        except Exception as e:

            print(
                f"Chart generation failed: {e}"
            )

            continue

    return figures


# =====================================================
# STATIC CHART GENERATOR
# =====================================================

def create_static_chart(
    df,
    chart,
    chart_type,
    output_path
):
    """
    Create a static Matplotlib PNG version
    of the recommended chart.

    This image is used by the PDF report.
    """

    plt.figure(
        figsize=(12, 7)
    )

    # =====================================================
    # LINE
    # =====================================================

    if chart_type == "line":

        plt.plot(
            df[chart["x"]],
            df[chart["y"]],
            marker="o"
        )

        plt.xlabel(
            chart["x"]
        )

        plt.ylabel(
            chart["y"]
        )

    # =====================================================
    # BAR
    # =====================================================

    elif chart_type == "bar":

        grouped = (
            df.groupby(chart["x"])[chart["y"]]
            .sum()
            .reset_index()
        )

        plt.bar(
            grouped[chart["x"]].astype(str),
            grouped[chart["y"]]
        )

        plt.xlabel(
            chart["x"]
        )

        plt.ylabel(
            chart["y"]
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

    # =====================================================
    # PIE
    # =====================================================

    elif chart_type == "pie":

        grouped = (
            df.groupby(chart["names"])[chart["values"]]
            .sum()
        )

        plt.pie(
            grouped.values,
            labels=grouped.index,
            autopct="%1.1f%%"
        )

    # =====================================================
    # SCATTER
    # =====================================================

    elif chart_type == "scatter":

        plt.scatter(
            df[chart["x"]],
            df[chart["y"]]
        )

        plt.xlabel(
            chart["x"]
        )

        plt.ylabel(
            chart["y"]
        )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    elif chart_type == "histogram":

        plt.hist(
            df[chart["x"]].dropna(),
            bins=20
        )

        plt.xlabel(
            chart["x"]
        )

        plt.ylabel(
            "Frequency"
        )

    # =====================================================
    # BOX
    # =====================================================

    elif chart_type == "box":

        plt.boxplot(
            df[chart["y"]].dropna()
        )

        plt.ylabel(
            chart["y"]
        )

    # =====================================================
    # HEATMAP
    # =====================================================

    elif chart_type == "heatmap":

        corr = df.select_dtypes(
            include="number"
        ).corr()

        plt.imshow(
            corr,
            aspect="auto"
        )

        plt.colorbar()

        plt.xticks(
            range(len(corr.columns)),
            corr.columns,
            rotation=45,
            ha="right"
        )

        plt.yticks(
            range(len(corr.columns)),
            corr.columns
        )

    # =====================================================
    # TITLE
    # =====================================================

    plt.title(
        chart.get(
            "title",
            "Data Visualization"
        )
    )

    plt.tight_layout()

    # =====================================================
    # SAVE PNG
    # =====================================================

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()