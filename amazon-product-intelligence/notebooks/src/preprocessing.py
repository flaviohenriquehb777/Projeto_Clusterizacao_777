"""Data loading, cleaning, and feature engineering utilities.

The dataset contains product and review columns. This module provides:
- A raw loader with stable dtypes
- Cleaning helpers for price/discount/count fields
- Feature engineering used across notebooks
- A product-level table (one row per product_id) for PSI/clustering
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd


PriceBand = Literal["budget", "mid", "premium", "luxury"]
DiscountBand = Literal["low", "medium", "high"]
ReviewsBand = Literal["low", "medium", "high"]


def load_raw_dataset(csv_path: Path) -> pd.DataFrame:
    """Load the raw Amazon dataset from CSV.

    Args:
        csv_path: Path to dados_amazon.csv.

    Returns:
        Raw dataframe as read from disk.
    """
    df = pd.read_csv(csv_path, low_memory=False)
    return df


def _to_float_currency(value: object) -> float | np.floating | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return np.nan
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return np.nan
    s = s.replace("₹", "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan


def _to_float_percent(value: object) -> float | np.floating | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return np.nan
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return np.nan
    s = s.replace("%", "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return np.nan


def _to_int_count(value: object) -> int | np.integer | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return np.nan
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return np.nan
    s = s.replace(",", "").strip()
    try:
        return int(float(s))
    except ValueError:
        return np.nan


def extract_categories(category_value: object) -> tuple[str | None, str | None]:
    """Extract main_category and sub_category from the 'category' field.

    The column commonly uses a pipe-separated taxonomy (e.g. "Electronics|Wearable Technology|...").
    """
    if category_value is None or (isinstance(category_value, float) and np.isnan(category_value)):
        return (None, None)
    parts = [p.strip() for p in str(category_value).split("|") if p.strip()]
    if not parts:
        return (None, None)
    main = parts[0]
    sub = parts[1] if len(parts) > 1 else None
    return (main, sub)


@dataclass(frozen=True)
class FeatureBins:
    """Binning configuration used by feature engineering."""

    price_budget_max: float = 500.0
    price_mid_max: float = 2000.0
    price_premium_max: float = 10000.0
    discount_low_max: float = 20.0
    discount_medium_max: float = 50.0
    reviews_low_max: int = 100
    reviews_medium_max: int = 1000


def add_engineered_features(df: pd.DataFrame, bins: FeatureBins | None = None) -> pd.DataFrame:
    """Return a copy of df with cleaned numeric columns and engineered features."""
    bins = bins or FeatureBins()
    out = df.copy()

    out["discounted_price_clean"] = out["discounted_price"].map(_to_float_currency)
    out["actual_price_clean"] = out["actual_price"].map(_to_float_currency)
    out["discount_pct_clean"] = out["discount_percentage"].map(_to_float_percent)
    out["rating_count_clean"] = out["rating_count"].map(_to_int_count)
    out["rating_clean"] = pd.to_numeric(out.get("rating"), errors="coerce")

    main_sub = out["category"].map(extract_categories)
    out["main_category"] = [ms[0] for ms in main_sub]
    out["sub_category"] = [ms[1] for ms in main_sub]

    out["economia_absoluta"] = out["actual_price_clean"] - out["discounted_price_clean"]

    def price_band(p: float | None) -> PriceBand | None:
        if p is None or (isinstance(p, float) and np.isnan(p)):
            return None
        if p < bins.price_budget_max:
            return "budget"
        if p < bins.price_mid_max:
            return "mid"
        if p < bins.price_premium_max:
            return "premium"
        return "luxury"

    def discount_band(d: float | None) -> DiscountBand | None:
        if d is None or (isinstance(d, float) and np.isnan(d)):
            return None
        if d < bins.discount_low_max:
            return "low"
        if d <= bins.discount_medium_max:
            return "medium"
        return "high"

    def reviews_band(c: int | None) -> ReviewsBand | None:
        if c is None or (isinstance(c, float) and np.isnan(c)):
            return None
        if c < bins.reviews_low_max:
            return "low"
        if c <= bins.reviews_medium_max:
            return "medium"
        return "high"

    out["faixa_preco"] = out["discounted_price_clean"].map(price_band)
    out["faixa_desconto"] = out["discount_pct_clean"].map(discount_band)
    out["volume_reviews_bin"] = out["rating_count_clean"].map(reviews_band)
    return out


def build_product_table(df_reviews: pd.DataFrame) -> pd.DataFrame:
    """Build a product-level table (unique product_id) from a review-level dataset.

    The raw file may contain multiple rows per product due to multiple reviews.
    For PSI/clustering, we keep the first non-null representation per product and
    enrich with review-row counts.
    """
    df = df_reviews.copy()
    df["review_rows"] = 1

    agg = {
        "product_name": "first",
        "category": "first",
        "main_category": "first",
        "sub_category": "first",
        "discounted_price_clean": "first",
        "actual_price_clean": "first",
        "discount_pct_clean": "first",
        "rating_clean": "first",
        "rating_count_clean": "first",
        "economia_absoluta": "first",
        "faixa_preco": "first",
        "faixa_desconto": "first",
        "volume_reviews_bin": "first",
        "img_link": "first",
        "product_link": "first",
        "review_rows": "sum",
    }
    products = df.groupby("product_id", dropna=False, as_index=False).agg(agg)
    return products


def build_processed_datasets(
    raw_csv_path: Path,
    processed_dir: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create processed datasets and persist them to data/processed.

    Writes:
    - base_processada.csv: review-level cleaned base
    - base_produtos.csv: product-level base for PSI/clustering
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    df_raw = load_raw_dataset(raw_csv_path)
    df_processed = add_engineered_features(df_raw)
    df_products = build_product_table(df_processed)

    df_processed.to_csv(processed_dir / "base_processada.csv", index=False)
    df_products.to_csv(processed_dir / "base_produtos.csv", index=False)
    return df_processed, df_products

