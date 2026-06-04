"""
analysis/eye_diagram.py -- Eye diagram generation.

Generates eye diagrams by overlaying successive bit periods of the
received (filtered) waveform.  Matches the OptiSystem eye-diagram style
shown in Fig. 7 of the paper.

Note: All interactive rendering (Plotly heatmaps) is handled in ui/app.py.
This module only provides the pure-numpy compute_eye_diagram() function.
"""

from __future__ import annotations
import numpy as np
from config import SystemConfig, DEFAULT_CONFIG


def compute_eye_diagram(
    waveform: np.ndarray,
    config: SystemConfig = DEFAULT_CONFIG,
    n_traces: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute eye-diagram data by folding the waveform into bit periods.

    Parameters
    ----------
    waveform : np.ndarray
        Filtered electrical waveform (photocurrent or normalised voltage).
    config : SystemConfig
        System configuration (samples_per_bit).
    n_traces : int | None
        Maximum number of trace overlays.  None = use all available.

    Returns
    -------
    t_norm : np.ndarray
        Normalised time axis [0, 2] (2 bit periods for better visibility).
    traces : np.ndarray
        Array of shape (n_traces, 2 x spb) -- each row is one trace.
    density : np.ndarray
        2-D histogram (density map) of the eye diagram.
    """
    spb = config.samples_per_bit
    eye_period = 2 * spb    # 2-bit window
    n_total = len(waveform)

    #  Sliding window: step by 1 bit (spb samples) 
    # This ensures overlapping traces for a proper eye diagram.
    segments = []
    for i in range(0, n_total - eye_period, spb):
        segments.append(waveform[i : i + eye_period])
    
    traces = np.array(segments)
    if n_traces is not None:
        traces = traces[:n_traces]

    # Normalised time axis [0, 2] bit periods
    t_norm = np.linspace(0, 2, eye_period)

    # 2-D density histogram for heat-map style rendering
    all_vals = traces.flatten()
    all_t    = np.tile(t_norm, len(traces))
    y_min, y_max = all_vals.min(), all_vals.max()
    density, _, _ = np.histogram2d(
        all_t, all_vals,
        bins=[64, 128],
        range=[[0, 2], [y_min, y_max]],
    )

    return t_norm, traces, density


# ---------------------------------------------------------------------------
# Matplotlib-based plotting helpers have been removed.
# Interactive eye-diagram rendering (Plotly heatmaps) lives in ui/app.py.
# ---------------------------------------------------------------------------
