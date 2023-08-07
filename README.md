# PyNanoporeAnalyzer

_Individual Project for M.Sc. in Embedded Systems Engineering at University of Leeds._

Python application for analysis of nanopore data.

### Features
- Supports Axon Binary Format (.abf)
- Signal filtering using Butterworth and Bessel Low Pass Filters
- Signal Baseline detection by data mean and moving window average method
- Event spike detection using amplitude threshold based method (Automatic threshold calculation based on raw data gaussian pdf sigma).
- The following features of each event in the data are being extracted:
    - Event Maxima Amplitude (from baseline)
    - Event Duration (Baseline to baseline)
    - Event Dwell Time (Full width at half maxima)
    - Area under event curve
    - Event Rise Time (Baseline to maxima)
    - Event Fall Time (Maxima back to baseline)
- The application has the following visualisation options:
    - Time domain plot
    - Fourier domain plot
    - Scatterplots
    - Histogram (with gaussian pdf fitting)
    - Density Plot
    - Contour Plot

### Testing

The application has been tested with the following data sets:
- Confederat, Samuel (2022) Nanopore Fingerprinting of Supramolecular DNA Origami Nanostructures. University of Leeds. [Dataset] https://doi.org/10.5518/1198 (Data supporting Figures 1-5)
- Chau, Chalmers and Radford, Sheena and Hewitt, Eric and Actis, Paolo (2020) Dataset for Macromolecular crowding enhances the detection of DNA and proteins by a solid-state nanopore. University of Leeds. [Dataset] https://doi.org/10.5518/841