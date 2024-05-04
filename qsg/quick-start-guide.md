# tinySA Ultra Phase Noise App - Quick Start Guide
This guide will show you the steps to make a Phase Noise Measurement of the internal 30 MHz Calibration Signal.  
**Steps:**  
* Disconnect all signals from the tinySA Ultra.
* Turn on the tinySA Ultra.  
* From the screen menu select: *Preset -> Load Startup* The screen should look like the figure below. 0-800 Mhz sweep and the marker randomly moving around finding the peaks in the noise floor.
    
![screen0](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/0.bmp)  

  
* Using a SMA-SMA cable, connect the CAL connector on the tinySA Ultra to the RF connector.  
* From the screen menu select *Mode -> Calibration Output -> 30 MHz*.
* From the screen menu select *Spectrum Analyzer*. The screen should look like the figure below. The marker must be on the 30 MHz peak automatically. If the marker is not on the 30 MHz peak, then reset the markers to the default setting (this should have happened when the *Preset -> Load Startup* step was done.

![screen1](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/1.bmp)  

* From the screen menu select *Frequency -> Center* and type in *30 M* for 30 MHz. The screen should look like the figure below, again with the marker on the 30 MHz peak.

![screen2](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/2.bmp)  
  
  
* From the screen menu select *Frequency -> Span" and type in *2 k* for 2 kHz span. The screen should look like the figure below, again with the marker on the 30 MHz peak.

![screen3](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/3.bmp)  

   
* Wait for the tinySA Ultra to make a few sweeps so that the autoscale attenuator finds a solid setting.
* You can now run the tinySA Ultra Phase Noise App (or as we say in the lab: *Let 'er rip!* ;-)
* When the app is finished you should see a plot as shown below,
![final](https://github.com/Hagtronics/tinySA-Ultra-Phase-Noise/blob/main/docs/pn_figure4.PNG)

    
* Note: In general, it should be noted, when you have spanned in to 2 kHz (as per the step above), and you see that your signal under test is *moving around* either in Frequncy or Ampplitude you will not be able to make a very good phase noise measurement. Phase Noise Measurements require that the Signal Under Test be stable.
