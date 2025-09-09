"""
=====[ tinySA Ultra / Phase Noise App w/GUI ]==================================

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
import csv
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
import FreeSimpleGUI as sg
import savitzky_golay_filter as sgf
import phase_noise


# * ----- Version Tag ---------------------------------------------------------
VERSION = str(0.1)


# * ----- Local Routines ------------------------------------------------------
def update_status(window, message: str) -> None:
    window['-TEXTSTATUS-'].update(message)


def plot(x_data: list[float], y_data: list[float], title: str, centerf: float, width: int, height: int) -> None:
    # Plot Smooth - window size 601, polynomial order 3
    y_data_smooth = sgf.savitzky_golay(np.array(y_data), 601, 3)

    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    plt.subplots(figsize=(width*px, height*px))
    plt.plot(x_data, y_data)
    plt.plot(x_data, y_data_smooth)
    plt.semilogx()
    plt.grid(which='both')
    plt.xlabel('Frequency Offset [Hz]')
    plt.ylabel('Phase Noise [dBc/Hz]')
    plt.suptitle(title)
    dt = time.strftime("%Y-%m-%d %H:%M")
    title_str = f'Center Frequency = {centerf} Hz.  {dt}'
    plt.title(title_str)
    plt.xlim(1e3, 1e6)  # Hardcoded, not ideal
    plt.show(block=False)

    # window.write_event_value('-PLOTCLOSED-', 'plot is finished')


def save_to_csv(x_data: list[float], y_data: list[float], title: str) -> None:
    print('Writing Results to CSV File.')
    dt = time.strftime("%Y-%m-%d %H%M")
    output_file_name = title + ' (' + dt + ').csv'

    try:
        with open(output_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            wr = csv.writer(csvfile)
            # for i in range(len(phase_noise_freq)):
            #     wr.writerow([phase_noise_freq[i], phase_noise_amp[i]])
            for f, a in zip(x_data, y_data):
                wr.writerow([f, a])
    except Exception as e:
        sg.popup_error('Could not create or write to CSV file.\nReason,\n' + str(e))


# * ----- GUI -----------------------------------------------------------------

def app_gui():

    step1_text = """A - Do a full reset on the tinySA Ultra.
B - Set the tinySA Ultra 'Center Frequency' on the signal to be measured.
C - Set the 'Span' to 2 kHz.
D - Wait several sweeps until the tinySA Ultra autoscales the amplitude."""

    block_step1 = [[sg.Text(step1_text)]
                   ]

    step2_text = """Set the following parameters for the phase noise test,"""
    block_step2 = [[sg.Text(step2_text)],
                   [sg.Text('Test Name:'), sg.Input(default_text='Phase Noise Test', key='-TESTNAME-')],
                   [sg.Text('Trace Averaging:'), sg.Combo(['off', 'aver4', 'aver16'], default_value='aver16', key='-AVERAGING-')],
                   [sg.Text('Plot Width x Height:'), sg.Input('800', size=(10, 20), key='-PLOTW-'), sg.Input('600', size=(10, 20), key='-PLOTH-'), sg.Text('pixels')],
                   [sg.Checkbox('Recenter Center Frequency after each sweep?', default=False, key='-RECENTER-')],
                   [sg.Checkbox('Write result to CSV file?', default=True, key='-WRITECSV-')]
                   ]

    step3_text = """'Run' the phase noise test.\nPress 'Exit' to close the app."""
    block_step3 = [[sg.Text(step3_text)],
                   [sg.Button('Run'), sg.Button('Exit')]
                   ]

    layout = [
        [sg.Frame('Step 1', block_step1, size=(600, 115))],
        [sg.Frame('Step 2', block_step2, size=(600, 215))],
        [sg.Frame('Step 3', block_step3, size=(600, 115))],
        [sg.Text('Status: Idle', relief=sg.RELIEF_GROOVE, border_width=1, size=(65, 1), key='-TEXTSTATUS-')]
        ]

    sg.set_options(dpi_awareness=True)
    window = sg.Window(f'tinySA Ultra - Phase Noise Application - V{VERSION}', layout, size=(600, 520), finalize=True)

    timeout = None
    thread = None
    update_status(window, "Idle.")

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read(timeout=timeout)

        # print(event, values)

        # Exit button
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        # Run button
        if event in 'Run' and not thread:
            # disable this button
            window['Run'].update(disabled=True)

            # Set PN App Values
            phase_noise.PN_TEST_NAME = values['-TESTNAME-']
            phase_noise.PN_RECENTER = bool(values['-RECENTER-'])
            phase_noise.PN_AVERAGE = values['-AVERAGING-']  # Valid values: 'off', 'aver4', 'aver16'

            # Start PN App thread
            timeout = 100
            thread = threading.Thread(target=phase_noise.run_phase_noise, args=(window,), daemon=True)
            thread.start()
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', transparent_color='white', time_between_frames=100)

        if thread is not None:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', transparent_color='white', time_between_frames=100)

        # Thread message
        if event in '-THREADMESSAGE-':
            update_status(window, str(values['-THREADMESSAGE-']))

        # Thread completed
        if event in '-THREADCOMPLETED-':         # Thread has completed
            thread.join(timeout=0)
            print('Thread finished')
            sg.popup_animated(None)     # stop animation in case one is running
            thread = None
            timeout = None

            # Get the data / parameters
            x_data = phase_noise.PN_FREQ_DATA
            y_data = phase_noise.PN_AMP_DATA
            title = values['-TESTNAME-']
            center_f = phase_noise.PN_CENTER_FREQUENCY
            plot_width = int(values['-PLOTW-'])
            plot_height = int(values['-PLOTH-'])

            # Save to csv
            if values['-WRITECSV-'] is True:
                save_to_csv(x_data, y_data, title)

            plot(x_data, y_data, title, center_f, plot_width, plot_height)

            # Enable run button
            window['Run'].update(disabled=False)

    window.close()


if __name__ == '__main__':
    app_gui()
    print('Exiting Program Normally.')
