"""Mock objects for testing the ndx-fscv extension."""

from typing import Optional

import numpy as np
from pynwb.testing.mock.ecephys import mock_ElectrodesTable
from pynwb.testing.mock.file import mock_NWBFile

from ndx_fscv import FSCVResponseSeries, FSCVExcitationSeries, FSCVBackgroundSubtractedSeries
from pynwb import NWBFile
from pynwb.testing.mock.utils import name_generator


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


def mock_FSCVBackgroundSubtractedSeries(
    name: Optional[str] = None,
    description: str = "A mock FSCV background-subtracted series to be used for testing.",
    number_of_electrodes: int = 4,
    sampling_frequency: float = 2140.0,
    response_series: Optional[FSCVResponseSeries] = None,
    nwbfile: Optional[NWBFile] = None,
) -> FSCVBackgroundSubtractedSeries:
    """
    Create a mock FSCVBackgroundSubtractedSeries for testing.

    Parameters
    ----------
    name : str, optional
        Name of the background-subtracted series.
    description : str
        Description of the series.
    number_of_electrodes : int
        Number of electrodes.
    sampling_frequency : float
        Sampling frequency (Hz).
    response_series : FSCVResponseSeries, optional
        Reference to raw FSCVResponseSeries.
    nwbfile : NWBFile, optional
        NWBFile to attach the series to.

    Returns
    -------
    FSCVBackgroundSubtractedSeries
    """
    if response_series is None:
        response_series = mock_FSCVResponseSeries(
            number_of_electrodes=number_of_electrodes,
            sampling_frequency=sampling_frequency,
            nwbfile=nwbfile,
        )
    data = np.random.rand(100, number_of_electrodes)
    bkg_series = FSCVBackgroundSubtractedSeries(
        name=name or name_generator("fscv_background_subtracted_series"),
        description=description,
        data=data,
        rate=sampling_frequency,
        unit="amperes",
        response_series=response_series,
    )
    if nwbfile is not None:
        nwbfile.add_acquisition(bkg_series)
    return bkg_series
