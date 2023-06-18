# Python module and CLI Tool for NORDIC

This repository contains a python function and ~~command-line interface (CLI) tool written in Python~~ for executing functions of the NIFTI_NORDIC powered by MATLAB compiler SDK. The addition of python wrapper are made under the terms of the original license, and the software is intended for educational and research purposes only.

The original Matlab code, and the DEMO files can be found in the MATLAB subfolder. The CLI tool is compiled with MATLAB 2023a, and thus requires the Matlab runtime version 9.14. It is compatible with Python versions 3.8, 3.9, and 3.10.

In order to run the CLI tool, you need to properly set up the MATLAB runtime in your environment. Instructions for installing the MATLAB runtime can be found [here](https://www.mathworks.com/help/compiler/install-the-matlab-runtime.html), and instructions for configuring the MATLAB runtime are available [here](https://www.mathworks.com/help/compiler/mcr-path-settings-for-run-time-deployment.html).

Please note that all products compiled with the MATLAB compiler are copyright MathWorks, Inc. Please abide by their licensing terms when using this software.

# Licensing

This repository provides an additional interface to the NORDIC and NIFTI_NORDIC software, enabling Python and CLI execution. The core code, copyrighted by the Regents of the University of Minnesota, is governed by licensing terms detailed below. These terms delineate the rights and restrictions concerning the use, distribution, and modification of the software. By downloading or executing any part of this software, you implicitly agree to adhere to these terms. The repository does not alter these rights or terms in any way but serves to extend the software's accessibility. Please read and understand the licensing information provided below before using this repository.

# Usage
```python
import nordic

# magnitude only
nordic.run('./sample.nii.gz', 
           'output.nii.gz',
           modality="fMRI",
           kernel_size_gfactor=[10, 10, 1],
           kernel_size_pca=[5, 5, 5])

# with phase image
nordic.run('./sample.nii.gz',
           'output.nii.gz',
           phase_path = "./phase.nii.gz',
           modality="fMRI",
           kernel_size_gfactor=[10, 10, 1])
```

---

# Original Software: NORDIC_Raw
Matlab code for performing image reconstruction in MRI and performing the NORDIC denoising.
Needs matlab version 2017b or newer

# Overview
The two files NORDIC and NIFTI_NORDIC perform similar concepts, locally low-rank denoising.
Both approaches, uses a g-factor map to flatten the noise, and a noise-scan for estimating the homoegenous noise.
For NORDIC, the noise-scan and the g-factor are explicit constructions provided as the last elements in a 4D array.
For NIFTI_NORDIC, these are estimated based on the data. The construction for estimating the g-factor noise and the thermal noise level
uses the MPPCA method of Veraart et al. 2016
NIFTI_NORDIC has additional paramters that can be adjusted, for learning or understanding the influence of the different algortimic choices.
For NIFTI_NORDIC, there are two different options, depending on whether dMRI or fMRI is used. 
This difference appears related to the hwo the phase is retained in the DICOM of the vendor software. A corresponding distinction is not neccesary for the NORDIC processing.

This version of NIFTI_NORDIC has been made possible through the testing and evaulation of many people, including


Logan Dowdle,
Luca Vizioli,
Cheryl Olman,
Essa Yacoub,
Henry Braun,
Remi Patriat,
Mehmet Akcakaya,
Federico De Martino,
Lonike Faes,
Torben Ellegaard Lund,
Lasse Knudsen,
Stamatios Sotiropoulos,
Karen Mullinger,
Daniel Marsh,
Susan Francis,
Jose Manzano Patron


Any questions, comments or suggestions can be directed to

Steen Moeller
moell018@umn.edu

# Copyright and License information

© 2021 Regents of the University of Minnesota

NORDIC and NIFTI_NORDIC is copyrighted by Regents of the University of Minnesota and covered by US 10,768,260. Regents of the University of Minnesota will license the use of NORDIC and NIFTI_NORDIC solely for educational and research purposes by non-profit institutions and US government agencies only. For other proposed uses, contact umotc@umn.edu. The software may not be sold or redistributed without prior approval. One may make copies of the software for their use provided that the copies, are not sold or distributed, are used under the same terms and conditions. As unestablished research software, this code is provided on an "as is'' basis without warranty of any kind, either expressed or implied. The downloading, or executing any part of this software constitutes an implicit agreement to these terms. These terms and conditions are subject to change at any time without prior notice.

# System Requirements
# Hardware Requirements
Package only requires a standard computer with enough RAM to support the in-memory operations and loading the data
# Software Requirements
 This package is tested on Matlab version 2017b. All neccesary dependencies are part of the default matlab installation
# Installation Guide
 Ensure that NORDIC.m is in a path that is visible to matlab
# Demo for the installation
   Using the NORDIC.m function and the simulation in DEMO, the following will demonstrate hwo to use NORDIC

    script_for_creating_simulation_data
    NORDIC('demo_data_for_NORDIC.mat')
    
    QQ=load('KSP_demo_data_for_NORDICkernel8')
    Q=load('demo_data_for_NORDIC') 
    figure; clf
    subplot(2,2,1); imagesc(squeeze(real(Q.KSP(:,:,32,12))),[0 1]); title('Data + noise')
    subplot(2,2,2); imagesc(squeeze(real(Q.IMG(:,:,32,12))),[0 1]); title('Data w/o noise')
    subplot(2,2,3); imagesc(squeeze(real(QQ.KSP_update(:,:,32,12))),[0 1]); title('NORDIC processed')
    subplot(2,2,4); plot(squeeze(real(Q.KSP(20,25,32,1:end-2)  -   Q.IMG(20,25,32,1:end-1)))), hold on
                    plot(squeeze(real(QQ.KSP_update(20,25,32,1:end)  -   Q.IMG(20,25,32,1:end-1))))
                    legend('difference before NORDIC','difference after NORDIC')

 



