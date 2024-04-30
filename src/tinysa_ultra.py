"""
=====[ tinySA Ultra Serial Driver]=============================================

Heavily modified 'standard' tinySA driver.

Since this is a heavily modified code from the 'internet'
you are absolutely free to do whatever you want with it in line with the original
authors copyright.

Original Source:
https://github.com/mrhgit/Miscellaneous/blob/master/tinySA_Ultra_Movie_Capture/makin_movies.py

Original Copyright:
None listed.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Version:
0.1a - 30Apr24 - Initial 'Alpha' Debug Release
"""
VERSION = str(0.1)


import math
import time
import serial
from serial.tools import list_ports
import numpy as np
import PySimpleGUI as ps

# tinySA Ultra USB Identifiers
VID = 0x0483  # 1155
PID = 0x5740  # 22336

SERIAL_PORT_TIMEOUT = 30    # All in Seconds
SWEEP_WAIT_TIMEOUT = 30
INTER_CMD_DELAY = 0.1
WAIT_DELAY = 0.5
FREQUENCY_CHANGE_DELAY = 0.5
FETCH_DATA_TIMEOUT = 10


# Get tinysa device automatically
def getport() -> str:
    device_list = list_ports.comports()
    for device in device_list:
        if device.vid == VID and device.pid == PID:
            return device.device
    ps.popup_error('Could not find the tinySA Ultra.\nConnect the tinySA Ultra and try again.')
    raise OSError("tinySA Ultra device not found.")


class tinySA:
    """ TinySA Ultra Driver for Python.
    """
    def __init__(self, dev=None):
        self.dev = dev or getport()
        self.serial = None

    def __version__(self):
        return VERSION

    def open(self) -> None:
        if self.serial is None:
            self.serial = serial.Serial(self.dev, timeout=SERIAL_PORT_TIMEOUT)

    def close(self) -> None:
        if self.serial:
            self.serial.close()
        self.serial = None

    # *===== Low Level Commands ===============================================
    def _send_command(self, cmd) -> None:
        self.serial.write(cmd.encode())
        time.sleep(INTER_CMD_DELAY)
        _ = self.serial.readline()  # discard empty line
        time.sleep(INTER_CMD_DELAY)

    def _fetch_data(self) -> str:
        result = ""
        line = ""
        time_start = time.time()
        while True:
            c = self.serial.read().decode("utf-8")
            if c == chr(13):
                continue  # ignore CR
            line += c
            if c == chr(10):
                result += line
                line = ""
                continue
            if line.endswith("ch>"):
                # stop on prompt
                break
            delta_time = time.time() - time_start
            if delta_time > FETCH_DATA_TIMEOUT:
                # print("@@@@@ tinySA DEBUG: Fetch Data Timeout")
                break
        time.sleep(INTER_CMD_DELAY)
        return result

    def _data(self, array=2) -> list[float]:
        self._send_command("data %d\r" % array)
        data = self._fetch_data()
        x = []
        for line in data.split("\n"):
            if line:
                line.strip().split(" ")
                try:
                    x.append(float(line))
                except ValueError:
                    # print("@@@@@ TinySA DEBUG: _data() read exception!")
                    x.append(float("nan"))
        return x

    def _fetch_frequencies(self) -> list[float]:
        self._send_command("frequencies\r")
        data = self._fetch_data()
        x = []
        for line in data.split("\n"):
            if line:
                x.append(float(line))
        return x

    # * ===== My High Level Commands Here Down ====================================

    def calc(self, cmd: str) -> None:
        """Sets the tinySA Calc mode

        Args:
            cmd (str): Valid commands: |off|minh|maxh|maxd|aver4|aver16|quasip|
        """
        self._send_command('calc ' + cmd + '\r')
        return

    def get_temperature(self) -> float:
        """Get Device Temperature

        Returns:
                float: temperature in Deg C
        """
        self._send_command("k\r")
        data = self._fetch_data()
        for line in data.split("\n"):
            if line:
                return float(line)
        return float('nan')

    def get_battery_voltage(self) -> float:
        """Get Battery Voltage

        Returns:
                float: Battery voltage in mV
        """
        self._send_command("vbat\r")
        data = self._fetch_data()
        for line in data.split("\n"):
            if line:
                rval = line.replace("m", "")
                rval = rval.replace("V", "")
                return float(rval)
        return float('nan')

    def set_rbw(self, rbw: int = 0) -> None:
        """Sets the tinySA Res BW in Hz
                Valid values in Hz:
                        0, 200, 1000, 3000, 10000, 30000, 100000, 600000, 850000
                if RBW = zero then 'AUTO' mode is selected
        Args:
                rbw (float): RBW in Hz
        """
        if rbw == 0:
            self._send_command("rbw auto\r")
            return
        if rbw == 200:
            self._send_command("rbw 0.2\r")
            return
        if rbw >= 1:
            self._send_command("rbw %d\r" % int(rbw / 1000))

    def resume(self) -> None:
        """Resumes the tinySA Sweep"""
        self._send_command("resume\r")

    def pause(self) -> None:
        """Pauses the tinySA sweep"""
        self._send_command("pause\r")

    def trigger(self, mode: str) -> None:
        """Triggers the tinySA

        Args:
                mode (str): Modes are: 'auto', 'normal', 'single'
        """
        if "auto" in mode:
            self._send_command("trigger auto\r")
            return
        if "normal" in mode:
            self._send_command("trigger normal\r")
            return
        if "single" in mode:
            self._send_command("trigger single\r")
            return

    def wait(self) -> None:
        """Triggers and waits for sweep to finish.
        Puts tinySA Ultra into 'pause' mode as a side effect.
        """
        self.serial.write('wait\r'.encode())
        _ = self.serial.readline()  # discard cmd echo
        time.sleep(INTER_CMD_DELAY)

        time_start = time.time()
        while True:
            # Wait until the 'ch>' prompt
            rval = self.serial.read().decode("utf-8")
            if '>' in str(rval):
                break

            delta_time = time.time() - time_start
            if delta_time > SWEEP_WAIT_TIMEOUT:
                break

        # Trace updating takes some extra time too
        time.sleep(WAIT_DELAY)

    def get_freq_data(self) -> list[float]:
        """Gets the current sweep frequency array from the tinySA

        Returns:
                list[float]: Frequency points in Hz
        """
        return self._fetch_frequencies()

    def get_amp_data(self) -> list[float]:
        """Gets the current amplitude array from the tinySA

        Notes:  Data array '0' - Seems like the last measured array without any math.
                Data array '1' - Don't know what this is.
                Data array '2' - Seems like it is the display array which
                                includes trace averaging or other math.

        Returns:
                list[float]: Amplitude points in dBm
        """
        return self._data(2)

    def get_marker_value(self, mk_num: int = 1) -> tuple[float, float]:
        """Gets the marker amplitude value specified.

        Args:
                mk_num (int, optional): The Marker to read. Defaults to 1.

        Returns:
                tuple: [MarkerAmpl, MarkerFreq]
        """
        tries = 0
        while True:
            self._send_command("marker %d\r" % mk_num)
            data = self._fetch_data()
            line = data.split("\n")[0]
            if line:
                dl = line.strip().split(" ")
                if len(dl) >= 4:
                    d = line.strip().split(" ")
                    r_tuple = tuple[float, float]
                    try:
                        r_tuple = (float(d[3]), float(d[2]))
                    except ValueError:
                        tries += 1
                        if tries > 10:
                            # print("@@@@@ TinySA DEBUG: get_marker_value() - Too many retries!")
                            return (float("nan"), float("nan"))
                        continue
                    return r_tuple

    def get_marker_peak(self) -> tuple[float, float]:
        """Reads the current amplitude and frequency array then returns a tuple
                of the (amplitude, frequency) of the maximum amplitude value in the array.

        Returns:
                tuple[float, float]: (amplitude dBm, frequency Hz) of maximum amplitude
        """
        max_amp = 0.0
        freq_at_max = 0.0
        tries = 0
        while True:
            freq = np.array(self.get_freq_data())
            amp = np.array(self.get_amp_data())

            if tries > 10:
                # print("@@@@@ tinySA DEBUG: get_marker_peak() - Too many retries!")
                return (float("nan"), float("nan"))
            try:
                i = amp.argmax()
            except ValueError:
                tries += 1
                continue

            max_amp = amp[i]
            freq_at_max = freq[i]

            if math.isnan(max_amp) or math.isnan(freq_at_max):
                tries += 1
                continue
            else:
                return (max_amp, freq_at_max)

    def set_start_stop(self, start: float, stop: float) -> None:
        """Sets the sweep Start and Stop frequencies in Hz

        Args:
                start (float): Start Frequency Hz
                stop (float): Stop Frequency Hz
        """
        self._send_command("sweep start %d\r" % start)
        self._send_command("sweep stop %d\r" % stop)
        time.sleep(FREQUENCY_CHANGE_DELAY)

    def set_center_span(self, center: float, span: float) -> None:
        """Sets the sweep Center and Span frequencies in Hz

        Args:
                center (float): Center Frequency in Hz
                span (float): Span Frequency in Hz
        """
        self._send_command("sweep center %d\r" % center)
        self._send_command("sweep span %d\r" % span)
        time.sleep(FREQUENCY_CHANGE_DELAY)

    def get_sweep(self) -> tuple[float, float, int]:
        """Gets current sweep frequencies an number of points.

        Returns:
                tuple[float, float, int]: (Start Frequency Hz, Stop Frequency Hz, Number of Points)
        """
        self._send_command("sweep\r")
        time.sleep(INTER_CMD_DELAY)
        data = self._fetch_data()
        for line in data.split("\n"):
            if line:
                vals = line.split(" ")
                return (float(vals[0]), float(vals[1]), int(vals[2]))
        return (0, 0, 0)

    def set_lna(self, lna_on=1) -> None:
        """Sets the LNA state

        Args:
                lna_on (int): 1 = LNA ON, 0 = LNA OFF
        """
        if lna_on == 1:
            self._send_command("lna on\r")
        else:
            self._send_command("lna off\r")

    def set_attenuator(self, value: str) -> None:
        """Sets the input Attenuator

        Args:
            value (str):  Valid Values: |0..31|auto|
        """

    def set_cal_output_Frequency(self, value: str) -> None:
        """Sets the calibrator output frequency

        Args:
            value (str): Valid values:  |off|30|15|10|4|3|2|1|
        """

    def get_info(self) -> str:
        """Returns tinySA device information.

        Returns:
            str: device info string.
        """
        self._send_command("info\r")
        time.sleep(INTER_CMD_DELAY)
        return self._fetch_data()

    def get_version(self) -> str:
        """Returns the tinySA version FW information.

        Returns:
            str: FW ID String
        """
        self._send_command("version\r")
        time.sleep(INTER_CMD_DELAY)
        return self._fetch_data()

# ----- Fini -----
