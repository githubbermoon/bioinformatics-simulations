#!/usr/bin/env python3
"""Simulate a Type-1 Coherent Feed-Forward Loop (C1-FFL).

This script compares two inputs:
1) a short pulse (noise)
2) a long pulse (real signal)

The target gene Z uses an AND gate of X and Y, producing sign-sensitive delay:
Z turns on only when X remains high long enough for Y to accumulate.
"""

from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def hill_activation(s: float, k: float, n: float) -> float:
    """Standard activating Hill function."""
    s_n = s**n
    return s_n / (k**n + s_n)


def pulse_signal(t: float, start: float, end: float, amplitude: float = 1.0) -> float:
    """Piecewise-constant input signal X(t)."""
    return amplitude if start <= t <= end else 0.0


def c1_ffl_ode(
    t: float,
    state: np.ndarray,
    pulse_start: float,
    pulse_end: float,
    params: dict[str, float],
) -> list[float]:
    """ODE system for Type-1 coherent FFL with AND gate at Z."""
    y, z = state
    x = pulse_signal(t, pulse_start, pulse_end, params["x_amp"])

    hy = hill_activation(x, params["k_xy"], params["n_xy"])
    hx = hill_activation(x, params["k_xz"], params["n_xz"])
    hyz = hill_activation(y, params["k_yz"], params["n_yz"])

    dy_dt = params["alpha_y"] * hy - params["beta_y"] * y
    dz_dt = params["alpha_z"] * (hx * hyz) - params["beta_z"] * z

    return [dy_dt, dz_dt]


def run_simulation(
    t_span: tuple[float, float],
    t_eval: np.ndarray,
    pulse_start: float,
    pulse_end: float,
    params: dict[str, float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate the ODEs for a specific input pulse."""
    sol = solve_ivp(
        fun=lambda t, s: c1_ffl_ode(t, s, pulse_start, pulse_end, params),
        t_span=t_span,
        y0=[0.0, 0.0],
        t_eval=t_eval,
        method="LSODA",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.1,
    )

    if not sol.success:
        raise RuntimeError(f"ODE solve failed: {sol.message}")

    x = np.array([pulse_signal(t, pulse_start, pulse_end, params["x_amp"]) for t in t_eval])
    y = sol.y[0]
    z = sol.y[1]
    return x, y, z


def make_figure(
    t_eval: np.ndarray,
    short_results: tuple[np.ndarray, np.ndarray, np.ndarray],
    long_results: tuple[np.ndarray, np.ndarray, np.ndarray],
    out_path: str,
) -> None:
    """Plot and save the side-by-side simulation comparison."""
    x_s, y_s, z_s = short_results
    x_l, y_l, z_l = long_results

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)

    axes[0].plot(t_eval, x_s, label="X input", color="#1f77b4", linewidth=2)
    axes[0].plot(t_eval, y_s, label="Y intermediate", color="#ff7f0e", linewidth=2)
    axes[0].plot(t_eval, z_s, label="Z target", color="#2ca02c", linewidth=2)
    axes[0].set_title("Short Pulse (Noise)")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Expression (a.u.)")
    axes[0].grid(alpha=0.3)
    axes[0].legend(frameon=False)

    axes[1].plot(t_eval, x_l, label="X input", color="#1f77b4", linewidth=2)
    axes[1].plot(t_eval, y_l, label="Y intermediate", color="#ff7f0e", linewidth=2)
    axes[1].plot(t_eval, z_l, label="Z target", color="#2ca02c", linewidth=2)
    axes[1].set_title("Long Pulse (Real Signal)")
    axes[1].set_xlabel("Time")
    axes[1].grid(alpha=0.3)

    fig.suptitle("Type-1 Coherent Feed-Forward Loop: Sign-Sensitive Delay", fontsize=13)
    fig.tight_layout()
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    params = {
        "x_amp": 1.0,
        "alpha_y": 0.3,
        "beta_y": 0.05,
        "alpha_z": 1.8,
        "beta_z": 0.2,
        "k_xy": 0.9,
        "n_xy": 4.0,
        "k_xz": 0.35,
        "n_xz": 4.0,
        "k_yz": 2.8,
        "n_yz": 8.0,
    }

    t0, tf = 0.0, 120.0
    t_eval = np.linspace(t0, tf, 2401)

    short_results = run_simulation(
        t_span=(t0, tf),
        t_eval=t_eval,
        pulse_start=10.0,
        pulse_end=25.0,
        params=params,
    )
    long_results = run_simulation(
        t_span=(t0, tf),
        t_eval=t_eval,
        pulse_start=10.0,
        pulse_end=85.0,
        params=params,
    )

    _, _, z_short = short_results
    _, _, z_long = long_results
    max_z_short = float(np.max(z_short))
    max_z_long = float(np.max(z_long))
    activation_ratio = max_z_long / max(max_z_short, 1e-12)
    sign_sensitive_delay_confirmed = max_z_long > 5.0 * max(max_z_short, 1e-6)

    make_figure(t_eval, short_results, long_results, out_path="ffl_simulation.png")

    verification_payload = {
        "metrics": {
            "max_z_short_pulse": max_z_short,
            "max_z_long_pulse": max_z_long,
            "activation_ratio": activation_ratio,
        },
        "assertions": {
            "sign_sensitive_delay_confirmed": sign_sensitive_delay_confirmed,
        },
    }
    with open("verification.json", "w", encoding="utf-8") as verification_file:
        json.dump(verification_payload, verification_file, indent=2, sort_keys=True)
        verification_file.write("\n")

    print("Saved figure: ffl_simulation.png")
    print("Saved verification: verification.json")
    print(f"Short pulse max(Z): {max_z_short:.4f}")
    print(f"Long pulse max(Z):  {max_z_long:.4f}")
    print(f"Activation ratio:   {activation_ratio:.4f}")
    if sign_sensitive_delay_confirmed:
        print("Result: C1-FFL rejects short transient input and responds to sustained input.")
    else:
        print("Warning: parameter choice does not clearly separate short vs long response.")


if __name__ == "__main__":
    main()
