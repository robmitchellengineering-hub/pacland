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
