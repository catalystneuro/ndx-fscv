# -*- coding: utf-8 -*-
from pathlib import Path

from pynwb import NWBDatasetSpec
from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBLinkSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-fscv""",
        version="""0.1.0""",
        doc="""This NWB extension defines data types for Fast-Scan Cyclic Voltammetry (FSCV), a neurochemical recording
        technique. It supports storing the applied triangular ramp waveform, measured electrochemical current, and
        derived cyclic voltammograms used to study dopamine and other neuromodulator dynamics.""",
        author=[
            "Ben Dichter",
            "Szonja Weigl",
        ],
        contact=[
            "ben.dicther@catalystneuro.com",
            "szonja.weigl@catalystneuro.com",
        ],
    )
    ns_builder.include_namespace("core")

    fscv_response_series = NWBGroupSpec(
        neurodata_type_def="FSCVResponseSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to store the raw FSCV current measurements recorded over time, linked to "
        "electrodes and excitation waveform.",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc=(
                    "The data values. It should be a 2D array where the first dimension represents time points "
                    "and the second dimension represents measured current from the electrodes."
                ),
                dtype="float64",
                shape=[
                    None,
                    None,
                ],
                dims=[
                    "num_timepoints",
                    "num_electrodes",
                ],
                attributes=[
                    NWBAttributeSpec(
                        name="unit",
                        doc="Unit of the data values, should be 'amperes'.",
                        dtype="text",
                        value="amperes",
                    ),
                ],
            ),
            NWBDatasetSpec(
                name="electrodes",
                neurodata_type_inc="DynamicTableRegion",
                doc="A reference to the electrodes table region this data comes from.",
            ),
        ],
        links=[
            NWBLinkSpec(
                name="excitation_series",
                target_type="FSCVExcitationSeries",
                doc="Link to the excitation waveform applied during FSCV.",
            )
        ],
        attributes=[
            NWBAttributeSpec(
                name="current_to_voltage_factor",
                doc="The factor used to multiply each data value to convert measured current to voltage.",
                dtype="float64",
                required=False,
            ),
        ],
    )

    fscv_excitation_series = NWBGroupSpec(
        neurodata_type_def="FSCVExcitationSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to store the applied FSCV excitation waveform over time.",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="The applied ramp voltage values. It should be a 1D array representing the voltage over time.",
                dtype="float64",
                shape=[
                    None,
                ],
                attributes=[
                    NWBAttributeSpec(
                        name="unit",
                        doc="Unit of the data values, should be 'volts'.",
                        dtype="text",
                        value="volts",
                    ),
                ],
            )
        ],
        attributes=[
            NWBAttributeSpec(
                name="scan_frequency",
                doc="The frequency at which the excitation waveform (e.g. triangular ramp) is applied, in hertz.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="sweep_rate",
                doc="The voltage sweep rate during a single scan, in volts per second. "
                "This represents the rate of potential change within each scan.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="waveform_shape",
                doc="The shape of the waveform, e.g., 'Triangle', 'N-shape', 'Sawhorse'.",
                dtype="text",
            ),
        ],
    )

    fscv_background_subtracted_series = NWBGroupSpec(
        neurodata_type_def="FSCVBackgroundSubtractedSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to store FSCV data with background subtraction applied.",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc=(
                    "The corrected data values after background subtraction. "
                    "It should be a 2D array where the first dimension represents time points "
                    "and the second dimension represents measured current from the electrodes."
                ),
                dtype="float64",
                shape=[
                    None,
                    None,
                ],
                dims=[
                    "num_timepoints",
                    "num_electrodes",
                ],
                attributes=[
                    NWBAttributeSpec(
                        name="unit",
                        doc="Unit of the data values, should be 'amperes'.",
                        dtype="text",
                        value="amperes",
                    ),
                ],
            ),
        ],
        links=[
            NWBLinkSpec(name="response_series", target_type="FSCVResponseSeries", doc="The link to the raw FSCV data.")
        ],
    )

    new_data_types = [fscv_response_series, fscv_excitation_series, fscv_background_subtracted_series]

    # export the spec to yaml files in the root spec folder
    output_dir = str((Path(__file__).parent.parent.parent / "spec").absolute())
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
