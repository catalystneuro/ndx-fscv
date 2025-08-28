"""Mock objects for testing the ndx-fscv extension."""

from typing import Optional

import numpy as np
from pynwb.testing.mock.ecephys import mock_ElectrodesTable
from pynwb.testing.mock.file import mock_NWBFile
from pynwb import NWBFile
from pynwb.testing.mock.utils import name_generator

from ndx_fscv import FSCVResponseSeries, FSCVExcitationSeries


def mock_FSCVExcitationSeries(
    name: Optional[str] = None,
    description: str = "A mock FSCV excitation series to be used for testing.",
    scan_frequency: float = 10.0,
    sweep_rate: float = 400.0,
    waveform_shape: str = "Triangle",
    sampling_frequency: float = 2140.0,
    nwbfile: Optional[NWBFile] = None,
) -> FSCVExcitationSeries:
    """
    Create a mock FSCVExcitationSeries for testing.

    Parameters
    ----------
    name : str, optional
        Name of the excitation series.
    description : str
        Description of the excitation series.
    sampling_frequency : float
        Sampling frequency (Hz).
    scan_frequency : float
        Frequency at which the ramp is scanned (Hz).
    sweep_rate : float
        Voltage sweep rate (V/s).
    waveform_shape : str
        Shape of the waveform (e.g., 'Triangle', 'N-shape', 'Sawhorse').
    nwbfile : NWBFile, optional
        NWBFile to attach the series to.

    Returns
    -------
    FSCVExcitationSeries
    """
    data = np.linspace(-1, 1, 100)
    excitation_series = FSCVExcitationSeries(
        name=name or name_generator("fscv_excitation_series"),
        description=description,
        data=data,
        rate=sampling_frequency,
        unit="volts",
        scan_frequency=scan_frequency,
        sweep_rate=sweep_rate,
        waveform_shape=waveform_shape,
    )
    if nwbfile is not None:
        nwbfile.add_stimulus(excitation_series)
    return excitation_series


def mock_FSCVResponseSeries(
    name: Optional[str] = None,
    description: str = "A mock FSCV response series to be used for testing.",
    number_of_electrodes: int = 4,
    number_of_samples: int = 100,
    current_to_voltage_factor: float = 0.5,
    sampling_frequency: float = 2140.0,
    excitation_series: Optional[FSCVExcitationSeries] = None,
    nwbfile: Optional[NWBFile] = None,
) -> FSCVResponseSeries:
    """
    Create a mock FSCVResponseSeries for testing.

    Parameters
    ----------
    name : str, optional
        Name of the response series.
    description : str
        Description of the response series.
    number_of_electrodes : int
        Number of electrodes.
    number_of_samples : int
        Number of samples.
    current_to_voltage_factor : float
        Factor to convert measured current to voltage.
    sampling_frequency : float
        Sampling frequency (Hz).
    excitation_series : FSCVExcitationSeries, optional
        Excitation waveform series.
    nwbfile : NWBFile, optional
        NWBFile to attach the series to.

    Returns
    -------
    FSCVResponseSeries
    """
    if nwbfile is None:
        nwbfile = mock_NWBFile()

    _ = mock_ElectrodesTable(n_rows=number_of_electrodes, nwbfile=nwbfile)
    fscv_electrodes = nwbfile.create_electrode_table_region(
        region=list(range(0, number_of_electrodes)),
        description="FSCV electrodes",
    )
    if excitation_series is None:
        excitation_series = mock_FSCVExcitationSeries(nwbfile=nwbfile)
    data = np.random.rand(number_of_samples, number_of_electrodes)
    fscv_response_series = FSCVResponseSeries(
        name=name or name_generator("fscv_response_series"),
        description=description,
        data=data,
        rate=sampling_frequency,
        unit="amperes",
        electrodes=fscv_electrodes,
        excitation_series=excitation_series,
        current_to_voltage_factor=current_to_voltage_factor,
    )
    nwbfile.add_acquisition(fscv_response_series)

    return fscv_response_series
