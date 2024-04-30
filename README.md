# tinySA Ultra - Phase Noise Measurement App in Python
 
# Introduction
The tinySA Ultra ( https://www.tinysa.org/wiki/ ) actually works enough like a regular spectrum analyzer that I decided to write a SSB Phase Noise Measurement Application for it in Python. This implementation is based on some excellent old Hewlett-Packard Application Notes especially AN270-2 [1].
![Figure 1](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure1.PNG?raw=true)   
**Figure 1 - The tinySA Ultra phase noise measurement app main GUI.**  

![Figure 4](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure4.PNG?raw=true)
**Figure 2 - A typical phase noise measurement made with the phase noise app. This is a plot of the tinySA Ultras built in 30 MHz signal generator. The 'Orange' trace above is a curve fit 'Smoothed' representation of the average phase noise measured.**  
# tinySA Ultra Implementation
To implement this solution, I measured the 200, 1000 and 3000 Hz resolution bandwidth filters (RBW) to determine their actual Equivalent Noise Bandwidth (EQNBW). These measurements were then used to convert the measurement in dB to a measurement of noise in dB/Hz. Since these filters are implemented in the tinySA Ultra as digital filters, the results should be repeatable between devices. The application measures the following band sweeps and then merges all the data into one continuous 1 kHz to 1 MHz data plot for display and saving to a CSV file.    
   
Sweep ranges and RBW's used for the sweeps,  
*1k - 3k       = 200Hz RBW  
3k - 10k      = 200Hz RBW  
10k - 30k     = 200 Hz RBW  
30k - 100k    = 200 Hz RBW  
100k - 300k   = 1000 Hz RBW  
300k - 1M     = 3000 Hz RBW*  
  
Noise Measurement Correction factor notes:  
Actual (measured) RBW filter EQNBW factors  
*3kHz correction = 35.3 dB  
1kHz correction = 30.6 dB  
200Hz correction = 26.6 dB*  
# Installation
The 'src' directory here contains all the Python files to run the application. Simply copy all the files in 'src' directory and place them on your PC somewhere. The application can be run by launching the Python main file: "tinysa_ultra_phase_noise_app.py". Note: assumes that python 3.12 is on your system path somewhere.

If you are allergic to 'Pythons' you can use the compiled [2] windows EXE of the App. This can be used by copying the EXE file from the directory 'windows-binary' to your PC and then running the file: "tinysa_ultra_phase_noise_app.exe". Note that this file can take up to 30 seconds to fully launch. Please be patient.
# Usage
   Your measured signal level should be < 0 dBm and > -30 dBm for the best dynamic range. 
   
   Power on tinySA Ultra and connect it to your PC.
   
   Use the menu item 'Preset' -> 'Load Startup' to preset the tinySA Ultra. Note: The marker must be in the mode where it 'follows' the peak displayed signal.
   
   Connect your signal to be measured to the tinySA Ultra. 
   
   Set the center frequency to the signal you wish to measure. 
   
   Set the span to 2 kHz. 
   
   Wait a few sweeps until the AGC settles and the attenuator is set correctly. 
   
   Start the Phase Noise App.
   
   Set the app settings on the Phase Noise GUI as desired for the run. 
   When ready, press the 'Run' button on the GUI. 
   
   Program will pop a Matplotlib plot when the measurement is complete, with a size as set in the GUI. You can move around, zoom and save the resulting plot from the controls on the plot.
   Close the Matplotlib plot window before starting another run. 
  
 Notes:
   We are measuring noise, so for the best plot quality set the "Trace Averaging" to 'aver16' (Averaging by 16 traces).  
   If your center frequency drifts a 'small' amount then check the "Recenter after each Sweep" button. 
   This will re-measure the signals center frequency after each offset band is measured. 
   
   A CSV file of the measured data will automatically be put in the directory where you ran 
   this program. The CSV file will be named the "Test Name" with the current date and time added. 
   This way, every time you make a run, a new CSV file will be created with a unique name. Note: Do not use any characters in the "Test Name" that are not legal file names or the creation of the CSV file will fail. Illegal characters for filenames on windows include: *, ", /, \, <, >, :, |, ?
  
 Test time notes:
   Less than 799 MHz center frequency,  
    *AVERAGE = 'off', Test time = 1 minute  
    AVERAGE = 'aver4', Test time = 3 minutes  
    AVERAGE = 'aver16', Test time = 11 minutes*  
    
   More than 800 MHz center frequency,  
    *AVERAGE = 'off', Test time = 2 minutes  
    AVERAGE = 'aver4', Test time = 6 minutes  
    AVERAGE = 'aver16', Test time = 23 minutes*  

# Problems / Solutions
Like all master / slave devices, this app can get out of sync with the tinySA Ultra and the application can hang. The remedy for this is to power cycle the tinySA Ultra and try again.
# Limitations 
The implementation has a dead band between 799 MHz and 800 Mhz where measurements cannot be made. This is due to the tinySA Ultras internal measurment algorithm changing at 800 MHz.  
The oscillator being measured can't drift too much during the test, likewise large amounts FM or AM on the oscillator under test will result in poor measurement repeatability and results. PLL locked or crystal based sources measure with much better repeatability. In this implementation, you cannot measure phase noise lower than the tinySA Ultra's intrinsic internal local oscillators (LO) phase noise, this is true for most is not all spectrum analyzer based phase noise applications. There are ways of extending the phase noise measurement range on the highest quality Spectrum Analyzers, but this is a waste of time for economy analyzers like the tinySA Ultra [3].
# Example Measurements
![figure 1a](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure1a.PNG?raw=true)
**Figure 3 - When running, the Phase Noise App provides a status bar that shows what it is doing. Status messages are also written to the console window as shown above.**  
![figure 2](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure2.PNG?raw=true)  
**Figure 4 - Measurement of a high performance YIG based Signal Generator at 30 MHz. This signal Generator has a phase noise below -110 dBc/Hz at 1 kHz and dropping to -140 dBc/Hz at 1 MHz offset, so this is essentially a plot of the tinySA Ultras LO Phase Noise.** 

![figure 3](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure3.PNG?raw=true)
**Figure 5 - Measurement of a high performance YIG based Signal Generator at 500 MHz. This signal Generator has a phase noise below -110 dBc/Hz at 1 kHz and dropping to -140 dBc/Hz at 1 MHz offset, so this is essentially a plot of the tinySA Ultras LO Phase Noise.**   
# Requirements
Application written in Python 3.12.1  
Libraries used,  
  * pyserial==3.5
  * PySimpleGUI==4.60.5
  * numpy==1.26.2
  * matplotlib==3.8.2
# References
[1] https://www.hpmemoryproject.org/technics/bench/3048/bench_pn_docs.htm  
[2] Python code compiled with: pyinstaller  
[3] https://www.edn.com/measuring-small-signals-accurately-a-practical-guide   
# Special Thanks To
* Eric for designing the tinySA Ultra  
* Guido for inventing Python.  
* Hewlett-Packard Company (Pre 1999) for teaching me all things RF.  
* PySimpleGUI for making the best 'Quick GUI' application in Python.  
