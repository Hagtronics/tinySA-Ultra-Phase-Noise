"""
=====[ tinySA Ultra / Phase Noise Test App ]=====================================

MIT License
Copyright (c) 2024 Steven C. Hageman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Version:
0.1 - 30Apr24 - Initial Release

"""

import time
import tinysa_ultra as tsa

VERSION = str(0.1)

# * ===== Usage ================================================================
#   Your measured signal level should be < 0 dBm and > -30 dBm.
#   Power reset the tinySA Ultra.
#   Use the menu item 'Preset' -> 'Load Startup' to preset the tinySA Ultra.
#   Connect your signal to be measured to the tinySA Ultra.
#   Set the center frequency to the signal you wish to measure.
#   Set the span to 2 kHz.
#   Wait a few sweeps until the AGC settles and the attenuator is set correctly.
#   Set the 'App Control Settings' on the GUI as desired for the run.
#   When ready, press the 'Run' button on the GUI.
#   Program will pop a Matplotlib Plot when the measurement is complete.
#   Close the Matplotlib plot window before starting another run.
#
# Notes:
#   We are measuring noise, so for the best plot quality AVERAGE = 'aver16' is suggested.
#   If your center frequency drifts a 'small' amount then set RECENTER = True,
#   to recenter the center frequency after each offset band is measured.
#   A CSV file of the measured data will automatically be put in the directory where you ran
#   this program. The CSV file will be named the Plot Title with the current date and time added.
#   This way, every time you make a run a new CSV file will be created with a unique name.
#
# Test time notes:
# < 800 MHz center frequency,
#   AVERAGE = 'off', Test time = 1 minute
#   AVERAGE = 'aver4', Test time = 3 minutes
#   AVERAGE = 'aver16', Test time = 11 minutes
#
# > 800 MHz center frequency,
#   AVERAGE = 'off', Test time = 2 minutes
#   AVERAGE = 'aver4', Test time = 6 minutes
#   AVERAGE = 'aver16', Test time = 23 minutes


# * ===== App Control Settings =================================================
PN_TEST_NAME = 'Phase Noise Test'
PN_RECENTER = False
PN_AVERAGE = 'aver16'  # Valid values: 'off', 'aver4', 'aver16'


# * ===== Resultant Trace Data =================================================
PN_AMP_DATA: list[float] = []
PN_FREQ_DATA: list[float] = []
PN_CENTER_FREQUENCY: float = 0.0

# Noise Measurement Correction factor notes:
# Actual (measured) RBW filter EQNBW factors
# 3kHz correction = 35.3 dB
# 1kHz correction = 30.6 dB
# 200Hz correction = 26.6 dB

# RBW's used for offsets,
# 1k - 3k       = 200Hz RBW
# 3k - 10k      = 200Hz RBW
# 10k - 30k     = 200 Hz RBW
# 30k - 100k    = 200 Hz RBW
# 100k - 300k   = 1000 Hz RBW
# 300k - 1M     = 3000 Hz RBW

# This list tuple = [(start_freq, stop_freq, noise correction factor), ...]
FREQUENCY_OFFSET_LIST = [(1e3, 3e3, 26.6), (3e3, 10e3, 26.6), (10e3, 30e3, 26.6),
                         (30e3, 100e3, 26.6), (100e3, 300e3, 30.6), (300e3, 1e6, 35.3)
                         ]


# * ===== Instantiate Device(s) ==================================================
sa = tsa.tinySA()


# * ===== Local Functions ======================================================

def _print_message(window, msg) -> None:
    print(msg)
    window.write_event_value('-THREADMESSAGE-', msg)

def _take_sweep(aver: str) -> None:

    sweeps = 1
    if 'aver16' in aver:
        sweeps = 16

    if 'aver4' in aver:
        sweeps = 4

    for _ in range(sweeps):
        sa.wait()
        print('.', end='', flush=True)

    print('')


def _find_carrier_center() -> tuple[float, float]:
    sa.wait()
    center_amplitude, center_frequency = sa.get_marker_value()
    return (center_amplitude, center_frequency)


def _make_amp_correction(amp_list: list[float], rbw_correction: float, center_amp: float) -> list[float]:
    corrected_list: list[float] = []

    for amp in amp_list:
        corrected_list.append((amp - rbw_correction) - center_amp)

    return corrected_list


def _make_freq_correction(freq_array: list[float], center_frequency: float) -> list[float]:
    corrected_list: list[float] = []

    for freq in freq_array:
        corrected_list.append(freq - center_frequency)

    return corrected_list


# * ===== Main P Measure Code =================================================
def run_phase_noise(window) -> None:
    global PN_AMP_DATA, PN_FREQ_DATA, PN_CENTER_FREQUENCY
    PN_AMP_DATA = []
    PN_FREQ_DATA = []
    center_drift = []

    time_start = time.time()

    # *----- Setup tinySA -----
    sa.open()
    sa.set_rbw(0)
    sa.calc('off')
    sa.pause()

    # *----- Get carrier info -----
    _print_message(window, 'Measuring Center Frequency and Amplitude.')

    center_amplitude, center_frequency = _find_carrier_center()
    PN_CENTER_FREQUENCY = center_frequency
    print(f'Center Frequency = {center_frequency} Hz    Amplitude = {center_amplitude} dBm')

    sa.calc(PN_AVERAGE)

    # *----- Loop through offsets -----
    for (start, stop, rbw_correction) in FREQUENCY_OFFSET_LIST:

        _print_message(window, f'Measuring offset = {start/1e3} kHz.')
        sa.set_start_stop(center_frequency + start, center_frequency + stop)

        _take_sweep(PN_AVERAGE)

        amp_array = sa.get_amp_data()
        amplitude_corrected = _make_amp_correction(amp_array, rbw_correction, center_amplitude)

        PN_AMP_DATA.extend(amplitude_corrected)

        freq_array = sa.get_freq_data()
        freq_corrected = _make_freq_correction(freq_array, center_frequency)
        PN_FREQ_DATA.extend(freq_corrected)

        if PN_RECENTER is True:
            _print_message(window, 'Re-Measuring Center Frequency.')
            old = center_frequency
            sa.calc('off')
            sa.set_center_span(center_frequency, 2000)
            center_amplitude, center_frequency = _find_carrier_center()
            sa.calc(PN_AVERAGE)
            center_delta = old - center_frequency
            center_drift.append(center_delta)

    if PN_RECENTER is True:
        print(f'Center Frequency Drift was = {center_drift} Hz')

    _print_message(window, f'Finished. Elapsed time = {(time.time() - time_start)/60.0:.1f} Minutes')



    # *----- Clean up tinySA -----
    sa.calc('off')
    sa.set_center_span(center_frequency, 2e3)
    sa.resume()

    # *----- Exit -----
    sa.close()

    window.write_event_value('-THREADCOMPLETED-', 'PN App code is finished')

# ----- Fini -----
