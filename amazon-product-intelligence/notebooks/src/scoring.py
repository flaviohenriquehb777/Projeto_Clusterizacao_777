"""Product Score Index (PSI) implementation.

PSI combines:
- normalized rating (weight default 40%)
- normalized log(review volume) (weight default 35%)
- normalized discount percentage (weight default 25%)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PSIWeights:
    """Weights for PSI components. Must sum to 1.0."""

    rating: float = 0.40
    rating_count_log: float = 0.35
    discount_pct: float = 0.25

    def validate(self) -> None:
        total = float(self.rating + self.rating_count_log + self.discount_pct)
        if not np.isclose(total, 1.0, atol=1e-6):
            raise ValueError(f"PSI weights must sum to 1.0, got {total}.")


def _minmax(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    min_v = s.min(skipna=True)
    max_v = s.max(skipna=True)
    if pd.isna(min_v) or pd.isna(max_v) or float(max_v) == float(min_v):
        return pd.Series(np.zeros(len(s), dtype=float), index=s.index)
    return (s - min_v) / (max_v - min_v)


def compute_psi(
    df: pd.DataFrame,
    *,
    rating_col: str = "rating_clean",
    rating_count_col: str = "rating_count_clean",
    discount_pct_col: str = "discount_pct_clean",
    weights: PSIWeights | None = None,
) -> pd.Series:
    """Compute PSI for each row in df.

    Args:
        df: Input dataframe (usually product-level).
        rating_col: Column with rating numeric.
        rating_count_col: Column with rating_count numeric.
        discount_pct_col: Column with discount percentage numeric.
        weights: PSI weights.

    Returns:
        A float series in [0, 100] (scaled for readability).
    """
    w = weights or PSIWeights()
    w.validate()

    rating_norm = _minmax(df[rating_col])
    rating_count_log_norm = _minmax(np.log1p(pd.to_numeric(df[rating_count_col], errors="coerce")))
    discount_norm = _minmax(df[discount_pct_col])

    psi_0_1 = (
        w.rating * rating_norm
        + w.rating_count_log * rating_count_log_norm
        + w.discount_pct * discount_norm
    )
    return (psi_0_1 * 100.0).astype(float)


def add_psi_column(
    df: pd.DataFrame,
    *,
    psi_col: str = "PSI",
    weights: PSIWeights | None = None,
) -> pd.DataFrame:
    """Return a copy of df with a PSI column added."""
    out = df.copy()
    out[psi_col] = compute_psi(out, weights=weights)
    return out

