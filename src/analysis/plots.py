"""
Visualization utilities — LC profiles and NIST results plots.
"""

import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "../../results"
)
os.makedirs(RESULTS_DIR, exist_ok=True)


def plot_lc_profile(profiles: dict[str, list[int]], filename: str = "lc_profile.png"):
    """LC profile for each generator in profiles."""
    plt.figure(figsize=(10, 5))

    for label, profile in profiles.items():
        plt.plot(range(1, len(profile) + 1), profile, label=label, linewidth=1.5)

    n = max(len(p) for p in profiles.values())
    plt.plot([1, n], [0.5, n / 2], "k--", linewidth=1, label="ideal random (n/2)")

    plt.xlabel("Sequence length (bits)")
    plt.ylabel("Linear complexity")
    plt.title("Linear Complexity Profile")
    plt.legend()
    plt.tight_layout()

    path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"saved: {path}")


def plot_nist_comparison(results: dict[str, dict[str, float]], filename: str = "nist_comparison.png"):
    """Bar chart of NIST p-values per generator."""
    generators = list(results.keys())
    test_names  = list(next(iter(results.values())).keys())

    x = range(len(test_names))
    width = 0.8 / len(generators)

    fig, ax = plt.subplots(figsize=(14, 6))

    for i, gen in enumerate(generators):
        pvals = [results[gen].get(t, 0) for t in test_names]
        offset = (i - len(generators) / 2 + 0.5) * width
        ax.bar([xi + offset for xi in x], pvals, width, label=gen)

    ax.axhline(y=0.01, color="red", linestyle="--", linewidth=1, label="threshold (0.01)")

    ax.set_xticks(list(x))
    ax.set_xticklabels(test_names, rotation=30, ha="right")
    ax.set_ylabel("p-value")
    ax.set_ylim(0, 1.05)
    ax.set_title("NIST SP 800-22 — p-values by generator")
    ax.legend()
    plt.tight_layout()

    path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"saved: {path}")


def plot_lc_bar(lc_values: dict[str, int], filename: str = "lc_comparison.png"):
    """Bar chart comparing linear complexity across generators."""
    labels = list(lc_values.keys())
    values = list(lc_values.values())

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"])

    for bar, val in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.01,
            str(val),
            ha="center", va="bottom", fontsize=9
        )

    plt.ylabel("Linear complexity")
    plt.title("Linear Complexity Comparison")
    plt.tight_layout()

    path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"saved: {path}")
