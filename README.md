# ndx-fscv Extension for NWB

This NWB extension defines data types for Fast-Scan Cyclic Voltammetry (FSCV), a neurochemical recording technique used
to study dopamine and other neuromodulator dynamics. It supports storing the applied triangular ramp waveform and the
measured electrochemical current.

## Installation

```bash
pip install ndx-fscv
```

## Usage

Below is a minimal example of how to use the extension to add FSCV data to an NWB file:

```python
from datetime import datetime

import numpy as np
from dateutil.tz import tzutc
from pynwb import NWBFile, NWBHDF5IO

from ndx_fscv import FSCVExcitationSeries, FSCVResponseSeries

# Create NWBFile
nwbfile = NWBFile(
    session_description="FSCV experiment",
    identifier="FSCV123",
    session_start_time=datetime(2024, 1, 1, tzinfo=tzutc()),
)

# Create FSCVExcitationSeries
applied_voltages = np.random.randn(100,)  # example data with 100 time points
excitation_series = FSCVExcitationSeries(
    name="fscv_excitation_series",
    description="The applied FSCV excitation waveform over time.",
    data=applied_voltages,
    rate=25_000.0,
    scan_frequency=10.0,
    sweep_rate=400.0,
    waveform_shape="Triangle",
    unit="volts",
)

# Create device and electrode group
device = nwbfile.create_device(
    name="fscv_device",
    description="A 4-channel FSCV device.",
)
electrode_group = nwbfile.create_electrode_group(
    name="fscv_electrode_group",
    description="The electrode group for the FSCV electrodes.",
    device=device,
    location="brain region",
)

# Add the electrodes to the NWBFile
for _ in range(4):
    nwbfile.add_electrode(group=electrode_group, location="brain region")

# Create an electrode table region referencing the first electrode
electrodes = nwbfile.create_electrode_table_region(region=[0, 1, 2, 3], description="FSCV electrodes")

# Create FSCVResponseSeries
measured_currents = np.random.randn(100, 4)  # example data with 100 time points and 4 electrodes
response_series = FSCVResponseSeries(
    name="fscv_response_series",
    description="The measured FSCV response currents over time.",
    data=measured_currents,
    rate=25_000.0,
    electrodes=electrodes,
    excitation_series=excitation_series,
    unit="amperes",
)

# Add to NWBFile
nwbfile.add_acquisition(excitation_series)
nwbfile.add_acquisition(response_series)

# Write to file
with NWBHDF5IO("example_fscv.nwb", "w") as io:
    io.write(nwbfile)

```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
