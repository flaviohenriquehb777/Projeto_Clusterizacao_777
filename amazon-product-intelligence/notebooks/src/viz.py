"""Reusable visualization helpers (Plotly + Matplotlib/Seaborn)."""

from __future__ import annotations

from typing import Iterable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PLOTLY_TEMPLATE = "plotly_dark"


def bar_products_by_category(df: pd.DataFrame, *, category_col: str = "main_category") -> go.Figure:
    counts = (
        df[category_col]
        .fillna("Unknown")
        .value_counts()
        .rename_axis(category_col)
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    fig = px.bar(counts, x=category_col, y="count", template=PLOTLY_TEMPLATE, title="Products by Category")
    fig.update_layout(xaxis_title="", yaxis_title="Products")
    return fig


def box_price_by_category(
    df: pd.DataFrame,
    *,
    price_col: str = "discounted_price_clean",
    category_col: str = "main_category",
) -> go.Figure:
    fig = px.box(
        df.dropna(subset=[price_col]),
        x=category_col,
        y=price_col,
        points="outliers",
        template=PLOTLY_TEMPLATE,
        title="Price Distribution by Category",
    )
    fig.update_layout(xaxis_title="", yaxis_title="Discounted Price (₹)")
    return fig


def scatter_price_vs_discount(
    df: pd.DataFrame,
    *,
    price_col: str = "discounted_price_clean",
    discount_col: str = "discount_pct_clean",
    color_col: str = "faixa_desconto",
    hover_cols: Iterable[str] = ("product_name", "main_category"),
) -> go.Figure:
    cols = [price_col, discount_col, color_col, *hover_cols]
    d = df[cols].copy()
    fig = px.scatter(
        d,
        x=price_col,
        y=discount_col,
        color=color_col,
        hover_data=list(hover_cols),
        template=PLOTLY_TEMPLATE,
        title="Price vs Discount",
    )
    fig.update_layout(xaxis_title="Discounted Price (₹)", yaxis_title="Discount (%)")
    return fig


def scatter_rating_vs_reviews(
    df: pd.DataFrame,
    *,
    rating_col: str = "rating_clean",
    reviews_col: str = "rating_count_clean",
    size_col: str = "discounted_price_clean",
    color_col: str = "main_category",
    hover_cols: Iterable[str] = ("product_name",),
) -> go.Figure:
    cols = [rating_col, reviews_col, size_col, color_col, *hover_cols]
    d = df[cols].copy()
    fig = px.scatter(
        d,
        x=reviews_col,
        y=rating_col,
        size=size_col,
        color=color_col,
        hover_data=list(hover_cols),
        template=PLOTLY_TEMPLATE,
        title="Rating vs Review Volume",
    )
    fig.update_layout(xaxis_title="Rating Count", yaxis_title="Rating")
    fig.update_xaxes(type="log")
    return fig


def indicator_gauge(value: float, *, title: str, min_v: float = 0.0, max_v: float = 100.0) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=float(value),
            title={"text": title},
            gauge={"axis": {"range": [min_v, max_v]}},
        )
    )
    fig.update_layout(template=PLOTLY_TEMPLATE, height=250)
    return fig

