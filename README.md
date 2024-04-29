# tinySA-Ultra-Phase-Noise
tinySA Ultra Phase Noise Measurement App
# Introduction
blah, blah
# tinySA Ultra Implementation
blah, blah
# Instalation
blah, blah 
# Usage
   Your measured signal level should be < 0 dBm and > -30 dBm. 
   
   Power on tinySA Ultra. 
   
   Use the menu item 'Preset' -> 'Load Startup' to preset the tinySA Ultra. 
   
   Connect your signal to be measured to the tinySA Ultra. 
   
   Set the center frequency to the signal you wish to measure. 
   
   Set the span to 2 kHz. 
   
   Wait a few sweeps until the AGC settles and the attenuator is set correctly. 
   
   Set the 'App Control Settings' on the Phase Noise GUI as desired for the run. 
   When ready, press the 'Run' button on the GUI. 
   
   Program will pop a Matplotlib Plot when the measurement is complete. 
   Close the Matplotlib plot window before starting another run. 
  
 Notes:
   We are measuring noise, so for the best plot quality AVERAGE = 'aver16' is suggested. 
   If your center frequency drifts a 'small' amount then set RECENTER = True, 
   to recenter the center frequency after each offset band is measured. 
   A CSV file of the measured data will automatically be put in the directory where you ran 
   this program. The CSV file will be named the Plot Title with the current date and time added. 
   This way, every time you make a run a new CSV file will be created with a unique name. 
  
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
blah, blah
# References
HP App Notes
