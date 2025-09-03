"""Plotting functions for FSCV data."""

import numpy as np

from ndx_fscv import FSCVResponseSeries, FSCVExcitationSeries

try:
    from matplotlib import pyplot as plt
except ImportError:
    raise ImportError(
        "Please install the matplotlib package to use the plot module, e.g., via 'pip install matplotlib'"
    )


def plot_series(
    response_series: FSCVResponseSeries,
    excitation_series: FSCVExcitationSeries,
    start_time: float = None,
    stop_time: float = None,
):
    """
    Plot the FSCV response and excitation series over a specified time window.

    Parameters
    ----------
    response_series : FSCVResponseSeries
        The FSCV response series containing current data measured in amperes.
    excitation_series : FSCVExcitationSeries
        The FSCV excitation series containing voltage data measured in volts.
    start_time : float, optional
        The start time for the plot (in seconds). If None, uses the start of the data.
    stop_time : float, optional
        The stop time for the plot (in seconds). If None, uses the end of the data.
    """
    current_data = np.array(response_series.data)  # shape: (n_samples, n_electrodes) or (n_samples,)
    voltage_data = np.array(excitation_series.data)  # shape: (n_samples,)
    timestamps = np.array(response_series.timestamps)

    if start_time is None:
        start_time = float(timestamps[0])
    if stop_time is None:
        stop_time = float(timestamps[-1])

    idx = np.where((timestamps >= start_time) & (timestamps <= stop_time))[0]
    if len(idx) == 0:
        raise ValueError("No data points found in the specified time range.")

    t_window = timestamps[idx]
    v_window = voltage_data[idx]
    c_window = current_data[idx]

    fig, (ax_voltage, ax_current) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax_voltage.plot(t_window, v_window, color="black")
    ax_voltage.set_ylabel("Applied Voltage (V)")
    ax_voltage.set_title("FSCV Excitation Series")

    num_electrodes = c_window.shape[1] if c_window.ndim > 1 else 1
    if num_electrodes == 1:
        c_window = c_window[:, np.newaxis]  # Make it 2D for consistency

    electrode_labels = response_series.electrodes["id"]
    colors = plt.get_cmap("tab10")(np.arange(num_electrodes) % 10)
    for i in range(num_electrodes):
        ax_current.plot(
            t_window,
            c_window[:, i],
            color=colors[i],
            linewidth=2,
            label=f"Electrode{electrode_labels[i]}",
        )
    ax_current.set_ylabel("Measured Current (A)")
    ax_current.set_title("FSCV Response Series")
    ax_current.set_xlabel("Time (s)")
    if num_electrodes > 1:
        plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


def plot_cv(
    response_series: FSCVResponseSeries,
    excitation_series: FSCVExcitationSeries,
    start_scan_index: int = 0,
    num_scans: int = 1,
):
    """
    Plot the cyclic voltammogram (CV) for one or more consecutive scans for all electrodes.

    Parameters
    ----------
    response_series : FSCVResponseSeries
        The FSCV response series containing current data measured in amperes.
    excitation_series : FSCVExcitationSeries
        The FSCV excitation series containing voltage data measured in volts.
    start_scan_index : int
        The index of the first scan to plot (0-based).
    num_scans : int
        The number of consecutive scans to plot.
    """
    current_data = np.array(response_series.data)  # shape: (n_samples, n_electrodes) or (n_samples,)
    voltage_data = np.array(excitation_series.data)  # shape: (n_samples,)
    timestamps = np.array(response_series.timestamps)

    scans_per_second = float(excitation_series.scan_frequency)
    total_samples = current_data.shape[0]

    samples_per_scan = int(len(current_data) // (round(timestamps[-1] - timestamps[0]) * scans_per_second))
    number_of_scans = total_samples // samples_per_scan

    # Validate scan indices
    if start_scan_index < 0 or (start_scan_index + num_scans) > number_of_scans:
        raise ValueError(
            f"Scan range out of bounds: start_scan_index={start_scan_index}, num_scans={num_scans}, "
            f"total_scans={number_of_scans}"
        )

    # Prepare data for plotting
    num_electrodes = current_data.shape[1] if current_data.ndim > 1 else 1
    if num_electrodes == 1:
        current_data = current_data[:, np.newaxis]

    electrode_labels = response_series.electrodes["id"][:]
    colors = plt.get_cmap("tab10")(np.arange(num_scans) % 10)

    fig, axes = plt.subplots(num_electrodes, 1, figsize=(10, 6 * num_electrodes), sharex=True, sharey=True)
    if num_electrodes == 1:
        axes = [axes]

    for e in range(num_electrodes):
        ax = axes[e]
        for s in range(num_scans):
            scan_idx = start_scan_index + s
            start = scan_idx * samples_per_scan
            end = start + samples_per_scan
            voltage_scan = voltage_data[start:end]
            current_scan = current_data[start:end, e]
            ax.plot(voltage_scan, current_scan, color=colors[s], alpha=0.7, label=f"Scan {scan_idx}")
        ax.set_title(f"CV for Electrode{electrode_labels[e]}")

        ax.set_ylabel("Measured Current (A)")
        ax.legend(loc="best")
        ax.grid()
    ax.set_xlabel("Applied Voltage (V)")
    plt.tight_layout()
    plt.show()
