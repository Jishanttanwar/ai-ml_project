"""
ml_insights.py — AI/ML module for Student Expense Tracker
Author: Jishant Tanwar
Reg. No.: 25BHI10093

Implements three ML fundamentals from scratch using only NumPy:
  1. Linear Regression       — predict next month's total spend
  2. K-Means Clustering      — find spending behavior patterns
  3. Keyword Classifier      — suggest category from expense note
"""

import numpy as np
from collections import defaultdict



def _monthly_totals(expenses):
    """Aggregate expenses into monthly totals. Returns sorted list of (month_index, total)."""
    by_month = defaultdict(float)
    for e in expenses:
        month = e["date"][:7]   
        by_month[month] += e["amount"]

    sorted_months = sorted(by_month.items())
    return sorted_months


def linear_regression_predict(expenses):
    """
    Fits a simple linear regression model (y = w*x + b) using gradient descent.
    x = month index (1, 2, 3, ...)
    y = total spending in that month

    Returns a dict with:
      - monthly_data   : list of (month_label, total)
      - slope          : learned weight
      - intercept      : learned bias
      - next_month     : predicted spend for the upcoming month
      - r_squared      : model fit quality (0 to 1)
    """
    monthly = _monthly_totals(expenses)

    if len(monthly) < 2:
        return {"error": "Need at least 2 months of data to predict."}

    labels = [m[0] for m in monthly]
    x = np.array([i + 1 for i in range(len(monthly))], dtype=float)
    y = np.array([m[1] for m in monthly], dtype=float)

    # Normalize x for stable gradient descent
    x_mean, x_std = x.mean(), x.std() if x.std() != 0 else 1.0
    x_norm = (x - x_mean) / x_std

    # Initialize parameters
    w, b = 0.0, 0.0
    lr = 0.01
    epochs = 1000
    n = len(x_norm)

    for _ in range(epochs):
        y_pred = w * x_norm + b
        error = y_pred - y
        dw = (2 / n) * np.dot(error, x_norm)
        db = (2 / n) * np.sum(error)
        w -= lr * dw
        b -= lr * db

    # Predict for next month (index = len + 1)
    next_x_norm = ((len(x) + 1) - x_mean) / x_std
    next_pred = max(0.0, w * next_x_norm + b)

    # R² score
    ss_res = np.sum((y - (w * x_norm + b)) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    # Recover slope/intercept in original scale for display
    slope_orig = w / x_std
    intercept_orig = b - w * x_mean / x_std

    return {
        "monthly_data": list(zip(labels, y.tolist())),
        "slope": round(slope_orig, 2),
        "intercept": round(intercept_orig, 2),
        "next_month_label": _next_month_label(labels[-1]),
        "next_month_predicted": round(next_pred, 2),
        "r_squared": round(r2, 4)
    }


def _next_month_label(last_month_str):
    """Given 'YYYY-MM', return the following month as 'YYYY-MM'."""
    year, month = int(last_month_str[:4]), int(last_month_str[5:7])
    month += 1
    if month > 12:
        month = 1
        year += 1
    return f"{year}-{month:02d}"




def kmeans_cluster_days(expenses, k=3, max_iter=100):
    """
    Clusters daily spending totals into k groups using K-Means.
    Each day's total spend is a 1D data point.

    Returns a dict with:
      - clusters       : list of {label, centroid, days, day_count}
      - your_pattern   : text description of dominant cluster
    """
    # Build daily totals
    by_day = defaultdict(float)
    for e in expenses:
        by_day[e["date"]] += e["amount"]

    if len(by_day) < k:
        return {"error": f"Need at least {k} days of data for clustering."}

    dates = sorted(by_day.keys())
    values = np.array([by_day[d] for d in dates], dtype=float)

    # Initialize centroids using spread-out points (avoids bad random init)
    idx = np.linspace(0, len(values) - 1, k, dtype=int)
    centroids = values[idx].copy()

    labels = np.zeros(len(values), dtype=int)

    for _ in range(max_iter):
        # Assign each point to nearest centroid
        distances = np.abs(values[:, None] - centroids[None, :])  # (n, k)
        new_labels = np.argmin(distances, axis=1)

        # Recompute centroids
        new_centroids = np.array([
            values[new_labels == j].mean() if np.any(new_labels == j) else centroids[j]
            for j in range(k)
        ])

        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
        labels = new_labels

    labels = new_labels

    # Sort clusters by centroid value so cluster 0 = lowest spend
    order = np.argsort(centroids)
    cluster_names = ["Low Spend", "Moderate Spend", "High Spend"][:k]

    result_clusters = []
    for rank, orig_idx in enumerate(order):
        member_dates = [dates[i] for i in range(len(dates)) if labels[i] == orig_idx]
        result_clusters.append({
            "label": cluster_names[rank],
            "centroid": round(float(centroids[orig_idx]), 2),
            "day_count": len(member_dates),
            "days": member_dates[:5]   # show first 5 example dates
        })

    # Find dominant cluster (most days)
    dominant = max(result_clusters, key=lambda c: c["day_count"])

    return {
        "clusters": result_clusters,
        "total_days_analyzed": len(dates),
        "dominant_pattern": dominant["label"],
        "dominant_centroid": dominant["centroid"]
    }



KEYWORD_MAP = {
    "food": [
        "food", "lunch", "dinner", "breakfast", "biryani", "mess", "canteen",
        "tea", "coffee", "snack", "restaurant", "eat", "pizza", "burger",
        "meal", "tiffin", "juice", "chai", "samosa", "dosa", "thali"
    ],
    "transport": [
        "auto", "bus", "train", "cab", "uber", "ola", "metro", "rickshaw",
        "ticket", "transport", "travel", "fare", "petrol", "fuel", "bike"
    ],
    "stationery": [
        "pen", "pencil", "notebook", "book", "copy", "paper", "stationery",
        "print", "printing", "xerox", "highlighter", "file", "folder", "graph"
    ],
    "entertainment": [
        "movie", "cinema", "game", "gaming", "netflix", "hotstar", "prime",
        "show", "concert", "party", "fun", "outing", "event", "cricket",
        "match", "subscription", "spotify", "youtube"
    ],
    "medicine": [
        "medicine", "tablet", "pharmacy", "doctor", "hospital", "clinic",
        "health", "medical", "syrup", "injection", "checkup", "prescription"
    ],
    "clothing": [
        "shirt", "pant", "shoes", "clothes", "clothing", "jacket", "dress",
        "laundry", "wash", "iron", "jeans", "tshirt", "hoodie", "socks"
    ],
    "recharge": [
        "recharge", "jio", "airtel", "vi", "bsnl", "mobile", "internet",
        "data", "plan", "prepaid", "wifi", "broadband", "sim"
    ]
}


def classify_category(note):
    """
    Classifies an expense note into a category using keyword matching.
    Returns top prediction and confidence scores for all categories.
    """
    if not note or not note.strip():
        return {"prediction": "other", "confidence": 0.0, "scores": {}}

    tokens = note.lower().split()
    scores = defaultdict(int)

    for token in tokens:
        for category, keywords in KEYWORD_MAP.items():
            if token in keywords:
                scores[category] += 1
            else:
                for kw in keywords:
                    if token in kw or kw in token:
                        scores[category] += 0.5
                        break

    if not scores:
        return {"prediction": "other", "confidence": 0.0, "scores": {}}

    total = sum(scores.values())
    confidence_scores = {cat: round(val / total, 3) for cat, val in scores.items()}
    best = max(confidence_scores, key=confidence_scores.get)

    return {
        "prediction": best,
        "confidence": confidence_scores[best],
        "scores": dict(sorted(confidence_scores.items(), key=lambda x: -x[1]))
    }



def show_prediction(expenses):
    result = linear_regression_predict(expenses)
    if "error" in result:
        print(f"\n  Prediction: {result['error']}")
        return

    print("\n  Spending Trend (Linear Regression)")
    print("  " + "-" * 44)
    print(f"  {'Month':<12} {'Actual Spend':>14}")
    print("  " + "-" * 44)
    for month, total in result["monthly_data"]:
        print(f"  {month:<12} Rs.{total:>11.2f}")
    print("  " + "-" * 44)
    print(f"\n  Model: spend = {result['slope']} x month_no + {result['intercept']}")
    print(f"  R² Score : {result['r_squared']}  {'(good fit)' if result['r_squared'] > 0.7 else '(more data improves this)'}")
    print(f"\n  Predicted spend for {result['next_month_label']}: Rs.{result['next_month_predicted']:.2f}")
    print()


def show_clusters(expenses):
    result = kmeans_cluster_days(expenses)
    if "error" in result:
        print(f"\n  Clustering: {result['error']}")
        return

    print(f"\n  Spending Pattern Clusters (K-Means, k=3)")
    print(f"  Days analyzed: {result['total_days_analyzed']}")
    print("  " + "-" * 44)
    for c in result["clusters"]:
        bar = "#" * min(c["day_count"], 20)
        print(f"  {c['label']:<18} Avg Rs.{c['centroid']:>8.2f}  {c['day_count']:>3} days  {bar}")
    print("  " + "-" * 44)
    print(f"  Your dominant pattern : {result['dominant_pattern']} (avg Rs.{result['dominant_centroid']:.2f}/day)")
    print()


def show_classify(note):
    result = classify_category(note)
    print(f"\n  Category Classifier")
    print(f"  Note       : \"{note}\"")
    print(f"  Prediction : {result['prediction']}  (confidence: {result['confidence']*100:.0f}%)")
    if result["scores"]:
        print("  All scores :")
        for cat, score in result["scores"].items():
            bar = "#" * int(score * 20)
            print(f"    {cat:<16} {score*100:>5.1f}%  {bar}")
    print()