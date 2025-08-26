"""Test in-memory Python API constructors for ndx-fscv extension."""

from ndx_fscv.testing.mock import (
    mock_FSCVResponseSeries,
    mock_FSCVExcitationSeries,
    mock_FSCVBackgroundSubtractedSeries,
)

from pynwb.testing import TestCase


class TestFSCVSeriesConstructor(TestCase):
    """Simple unit test for creating FSCV response series."""

    def setUp(self):
        """Set up any state specific to the execution of the given class."""

        self.name = "test_fscv_response_series"
        self.description = "A mock FSCV response series to be used for testing."
        self.number_of_electrodes = 4
        self.number_of_samples = 100
        self.current_to_voltage_factor = 0.5
        self.sampling_frequency = 25_000.0

    def test_fscv_response_series(self):
        """Test that the constructor for FSCVResponseSeries sets values as expected."""
        response_series = mock_FSCVResponseSeries(
            name=self.name,
            description=self.description,
            number_of_electrodes=self.number_of_electrodes,
            number_of_samples=self.number_of_samples,
            current_to_voltage_factor=self.current_to_voltage_factor,
            sampling_frequency=self.sampling_frequency,
        )

        self.assertEqual(response_series.name, self.name)
        self.assertEqual(response_series.description, self.description)
        self.assertEqual(response_series.unit, "amperes")
        self.assertEqual(response_series.data.shape[1], self.number_of_electrodes)
        self.assertEqual(response_series.data.shape[0], self.number_of_samples)
        self.assertEqual(response_series.rate, self.sampling_frequency)
        self.assertEqual(response_series.current_to_voltage_factor, self.current_to_voltage_factor)
        self.assertIsNotNone(response_series.electrodes)
        self.assertIsNotNone(response_series.excitation_series)
        self.assertEqual(response_series.excitation_series.unit, "volts")


class TestFSCVExcitationSeriesConstructor(TestCase):
    """Simple unit test for creating FSCV excitation series."""

    def setUp(self):
        """Set up any state specific to the execution of the given class."""
        self.name = "test_fscv_excitation_series"
        self.description = "A mock FSCV excitation series to be used for testing."
        self.sampling_frequency = 2140.0
        self.scan_frequency = 10.0
        self.sweep_rate = 400.0
        self.waveform_shape = "Triangle"

    def test_fscv_excitation_series(self):
        """Test that the constructor for FSCVExcitationSeries sets values as expected."""

        excitation_series = mock_FSCVExcitationSeries(
            name=self.name,
            description=self.description,
            sampling_frequency=self.sampling_frequency,
            scan_frequency=self.scan_frequency,
            waveform_shape=self.waveform_shape,
            sweep_rate=self.sweep_rate,
        )

        self.assertEqual(excitation_series.name, self.name)
        self.assertEqual(excitation_series.description, self.description)
        self.assertEqual(excitation_series.unit, "volts")
        self.assertEqual(excitation_series.scan_frequency, self.scan_frequency)
        self.assertEqual(excitation_series.sweep_rate, self.sweep_rate)
        self.assertEqual(excitation_series.waveform_shape, self.waveform_shape)


class TestFSCVBackgroundSubtractedSeriesConstructor(TestCase):
    """Simple unit test for creating FSCV background-subtracted series."""

    def setUp(self):
        """Set up any state specific to the execution of the given class."""
        self.name = "test_fscv_background_subtracted_series"
        self.description = "A mock FSCV background-subtracted series to be used for testing."
        self.number_of_electrodes = 4
        self.sampling_frequency = 500.0

    def test_fscv_background_subtracted_series(self):
        """Test that the constructor for FSCVBackgroundSubtractedSeries sets values as expected."""

        background_subtracted_series = mock_FSCVBackgroundSubtractedSeries(
            name=self.name,
            description=self.description,
            number_of_electrodes=self.number_of_electrodes,
            sampling_frequency=self.sampling_frequency,
        )

        self.assertEqual(background_subtracted_series.name, self.name)
        self.assertEqual(background_subtracted_series.description, self.description)
        self.assertEqual(background_subtracted_series.unit, "amperes")
        self.assertEqual(background_subtracted_series.data.shape[1], self.number_of_electrodes)
        self.assertEqual(background_subtracted_series.data.shape[0], 100)
        self.assertEqual(background_subtracted_series.rate, self.sampling_frequency)
        self.assertIsNotNone(background_subtracted_series.response_series)
        self.assertEqual(background_subtracted_series.response_series.unit, "amperes")
