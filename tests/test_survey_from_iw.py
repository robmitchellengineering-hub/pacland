"""The AP parser: real `iw` output shapes, and the occupancy arithmetic."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import rf_survey_from_iw as S

SURVEY = """Survey data from wlan0
\tfrequency:\t\t5180 MHz [in use]
\tnoise:\t\t-92 dBm
\tchannel active time:\t\t10000 ms
\tchannel busy time:\t\t2500 ms
Survey data from wlan0
\tfrequency:\t\t5500 MHz
\tnoise:\t\t-96 dBm
\tchannel active time:\t\t10000 ms
\tchannel busy time:\t\t800 ms
"""

STATIONS = """Station aa:bb:cc:dd:ee:ff (on wlan0)
\tsignal:  \t-52 [-56, -58] dBm
\tsignal avg:\t-53 dBm
\ttx bitrate:\t1201.0 MBit/s
\trx bitrate:\t1201.0 MBit/s
"""


def test_occupancy_is_busy_over_active():
    out = S.summarise(S.parse_survey(SURVEY), S.parse_stations(STATIONS))
    assert abs(out["quietest"]["occupancy"] - 0.08) < 1e-9, out
    assert abs(out["busiest"]["occupancy"] - 0.25) < 1e-9, out
    assert out["quietest"]["noise_dbm"] == -96


def test_station_signal_parsed():
    st = S.parse_stations(STATIONS)
    assert len(st) == 1 and st[0]["mac"] == "aa:bb:cc:dd:ee:ff"
    assert "-52" in st[0]["signal"]


if __name__ == "__main__":
    test_occupancy_is_busy_over_active()
    test_station_signal_parsed()
    print("survey-from-iw: 2 checks pass")


def test_nss_from_mcs_covers_all_four_streams():
    assert S.nss_from_mcs(0) == 1 and S.nss_from_mcs(7) == 1
    assert S.nss_from_mcs(8) == 2 and S.nss_from_mcs(15) == 2
    assert S.nss_from_mcs(16) == 3 and S.nss_from_mcs(24) == 4


def test_parse_link_reads_the_real_node_output():
    # verbatim from pacland-rog, 2026-10-31
    text = """Connected to 14:59:c0:65:57:2d (on wlp2s0)
\tSSID: Telstra3696
\tfreq: 2462.0
\tsignal: -37 dBm
\trx bitrate: 144.4 MBit/s MCS 15 short GI
\ttx bitrate: 144.4 MBit/s MCS 15 short GI
"""
    link = S.parse_link(text)
    assert link["ssid"] == "Telstra3696"
    assert link["freq_mhz"] == 2462.0
    assert link["band"] == "2.4 GHz"
    assert link["signal_dbm"] == -37.0
    assert link["nss"] == 2, link


def test_the_committed_capture_still_parses_to_two_streams():
    """The measurement record cites this file; if the parser drifts, the record is wrong."""
    import pathlib
    text = (pathlib.Path(__file__).resolve().parents[1] / "docs" / "data" / "iw-link-2026-10-31.txt").read_text()
    link = S.parse_link(text)
    assert link["ssid"] == "Telstra3696"
    assert link["band"] == "2.4 GHz"
    assert link["freq_mhz"] == 2462.0
    assert link["nss"] == 2
    assert link["mcs"] == 15
