# tinySA Ultra - Phase Noise Measurement App in Python
 
# Introduction
The tinySA Ultra actually works enough like a regular spectrum analyzer that I decided to write a Phase Noise Measurement Application for it in Python. This implementation is based on some excellent old Hewlett-Packard Application Notes especially AN270-2 [1].
![Figure 1](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure1.PNG?raw=true)   
Figure 1 - The tinySA Ultra phase noise measurement app main GUI.  

![Figure 4](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure4.PNG?raw=true)
Figure 2 - A tpical phase noise measurement made with the phase noise app. This is a plot of the tinySA Ultras built in 30 MHz signal generator.   
# tinySA Ultra Implementation
To implement this solution, I measured the 200, 1000 and 3000 Hz resolution bandwidth filters to determine their Equivalent Noise Bandwidth (ENBW). These measurements were then used to convert the measurement in dB to a measurement of noise in dB/Hz. Since these filters are implemented in the tinySA Ultra as digital filters, the results should be repeatable between devices.
# Installation
The 'src' directory here contains all the Python files to run the application. Simply copy all the files in 'src' directory and place them on your PC somewhere. The application can be run by launching the Python main file: "tinysa_ultra_phase_noise_app.py". Note: assumes that python 3.12 is on your system path somewhere.

If you are allergic to 'Pythons' you can use the compiled [2] windows EXE of the App. This can be used by copying the EXE file from the directory 'windows-binary' to your PC and then running the file: "tinysa_ultra_phase_noise_app.exe". Note that this file can take up to 30 seconds to fully launch. Please be patient.
# Usage
   Your measured signal level should be < 0 dBm and > -30 dBm. 
   
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
   We are measuring noise, so for the best plot quality AVERAGE = 'aver16' is suggested. 
   If your center frequency drifts a 'small' amount then set RECENTER = True, 
   to recenter the center frequency after each offset band is measured. 
   
   A CSV file of the measured data will automatically be put in the directory where you ran 
   this program. The CSV file will be named the "Plot Title" with the current date and time added. 
   This way, every time you make a run a new CSV file will be created with a unique name. Note: Do not use any characters in the "PLot Title" that are not legal file names or the creation of the CSV file will fail. Illegal characters for filenames on windows include: *, ", /, \, <, >, :, |, ?
  
 Test time notes:
   Less than 800 MHz center frequency,  
    AVERAGE = 'off', Test time = 1 minute  
    AVERAGE = 'aver4', Test time = 3 minutes  
    AVERAGE = 'aver16', Test time = 11 minutes  
    
   More than 800 MHz center frequency,  
    AVERAGE = 'off', Test time = 2 minutes  
    AVERAGE = 'aver4', Test time = 6 minutes  
    AVERAGE = 'aver16', Test time = 23 minutes  
# Limitations 
The oscillator being measured can't drift too much during the test, likewise large amounts FM or AM on the oscillator under test will result in poor measurement repeatability. PLL locked or crystal based sources measure with much better repeatability. In this implementation, you cannot measure phase noise lower than the tinySA Ultra's intrinsic LO source phase noise, this is true for most is not all spectrum analyzer based phase noise applications [x].
![figure 2](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure2.PNG?raw=true)  
Figure 3 - Measurement of a high performance YIG based Signal Generator at 30 MHz. 

![figure 3](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure3.PNG?raw=true)
Figure 4 - Measurement of a high performance YIG based Signal Generator at 500 MHz.   
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
* Guido for inventing Python.
* Hewlett-Packard Company (Pre 1999) for teaching me all things RF.
* PySimpleGUI for making the best 'Quick GUI' application in Python.
