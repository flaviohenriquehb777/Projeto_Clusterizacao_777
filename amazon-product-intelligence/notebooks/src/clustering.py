"""KMeans clustering utilities for product segmentation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class KMeansArtifacts:
    """Artifacts produced by a fitted KMeans pipeline."""

    pipeline: Pipeline
    labels: pd.Series
    pca_2d: pd.DataFrame


def _build_pipeline(n_clusters: int, *, random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("kmeans", KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")),
        ]
    )


def score_k_range(
    df: pd.DataFrame,
    *,
    features: list[str],
    k_values: Iterable[int] = range(2, 11),
    random_state: int = 42,
) -> pd.DataFrame:
    """Compute inertia and silhouette for a range of k values."""
    x = df[features].copy()
    rows: list[dict[str, float]] = []
    for k in k_values:
        pipe = _build_pipeline(k, random_state=random_state)
        pipe.fit(x)
        inertia = float(pipe.named_steps["kmeans"].inertia_)

        x_scaled = pipe.named_steps["scaler"].transform(
            pipe.named_steps["imputer"].transform(x)
        )
        labels = pipe.named_steps["kmeans"].labels_
        sil = float(silhouette_score(x_scaled, labels)) if k > 1 and len(x_scaled) > k else np.nan
        rows.append({"k": int(k), "inertia": inertia, "silhouette": sil})
    return pd.DataFrame(rows)


def fit_kmeans_pipeline(
    df: pd.DataFrame,
    *,
    features: list[str],
    n_clusters: int,
    random_state: int = 42,
) -> KMeansArtifacts:
    """Fit KMeans pipeline and compute a 2D PCA projection for visualization."""
    x = df[features].copy()
    pipe = _build_pipeline(n_clusters, random_state=random_state)
    pipe.fit(x)

    labels = pd.Series(pipe.named_steps["kmeans"].labels_, index=df.index, name="cluster").astype(int)
    x_scaled = pipe.named_steps["scaler"].transform(pipe.named_steps["imputer"].transform(x))
    pca = PCA(n_components=2, random_state=random_state)
    coords = pca.fit_transform(x_scaled)
    pca_2d = pd.DataFrame(coords, columns=["pca_1", "pca_2"], index=df.index)
    return KMeansArtifacts(pipeline=pipe, labels=labels, pca_2d=pca_2d)


def save_pipeline(pipeline: Pipeline, path: str) -> None:
    """Persist a fitted pipeline to disk."""
    dump(pipeline, path)


def name_clusters(
    df_products: pd.DataFrame,
    *,
    cluster_col: str = "cluster",
    price_col: str = "discounted_price_clean",
    discount_col: str = "discount_pct_clean",
    rating_col: str = "rating_clean",
    rating_count_col: str = "rating_count_clean",
) -> dict[int, str]:
    """Generate business-friendly names for clusters based on centroid-like summaries."""
    g = df_products.groupby(cluster_col)
    summary = g[[price_col, discount_col, rating_col, rating_count_col]].mean(numeric_only=True)

    price_rank = summary[price_col].rank(method="dense")
    discount_rank = summary[discount_col].rank(method="dense")
    rating_rank = summary[rating_col].rank(method="dense")
    volume_rank = summary[rating_count_col].rank(method="dense")

    names: dict[int, str] = {}
    for cluster_id in summary.index:
        pr = price_rank.loc[cluster_id]
        dr = discount_rank.loc[cluster_id]
        rr = rating_rank.loc[cluster_id]
        vr = volume_rank.loc[cluster_id]

        if pr >= price_rank.max() and rr >= rating_rank.max():
            names[int(cluster_id)] = "premium bem avaliado"
        elif dr >= discount_rank.max() and pr <= price_rank.min():
            names[int(cluster_id)] = "barato com alto desconto"
        elif vr >= volume_rank.max() and rr <= rating_rank.min():
            names[int(cluster_id)] = "popular problemático"
        elif rr >= rating_rank.max() and vr <= volume_rank.min():
            names[int(cluster_id)] = "hidden gems"
        else:
            names[int(cluster_id)] = "segmento misto"
    return names

