from datetime import datetime, UTC

from pynwb import NWBHDF5IO
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing import TestCase, remove_test_file

from ndx_fscv.testing.mock import (
    mock_FSCVExcitationSeries,
    mock_FSCVResponseSeries,
    mock_FSCVBackgroundSubtractedSeries,
)


class TestFSCVSeriesSimpleRoundtrip(TestCase):
    def setUp(self):
        self.nwbfile_path = "test_fscv_response_series_roundtrip.nwb"
        self.nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))

    def tearDown(self):
        remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        # Create mock FSCVExcitationSeries and FSCVResponseSeries
        excitation_series = mock_FSCVExcitationSeries(nwbfile=self.nwbfile)
        response_series = mock_FSCVResponseSeries(
            excitation_series=excitation_series,
            nwbfile=self.nwbfile,
        )
        bkg_series = mock_FSCVBackgroundSubtractedSeries(
            response_series=response_series,
            nwbfile=self.nwbfile,
        )

        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(response_series, read_nwbfile.acquisition[response_series.name])
            self.assertContainerEqual(bkg_series, read_nwbfile.acquisition[bkg_series.name])
