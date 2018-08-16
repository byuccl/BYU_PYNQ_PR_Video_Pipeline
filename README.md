# BYU Pynq PR Video Pipeline
**This is a BYU fork of the PYNQ project (https://github.com/Xilinx/PYNQ)**

As presented at FCCM 2018

![alt tag](./logo.png)


PYNQ is an open-source project from Xilinx that makes it easy to design embedded systems with Zynq All Programmable Systems on Chips (APSoCs). Using the Python language and libraries, designers can exploit the benefits of programmable logic and microprocessors in Zynq to build more capable and exciting embedded systems.
PYNQ users can now create high performance embedded applications with
-	parallel hardware execution
-	high frame-rate video processing
-	hardware accelerated algorithms
-	real-time signal processing
-	high bandwidth IO
-	low latency control

See the <a href="http://www.pynq.io/" target="_blank">PYNQ webpage</a> for an overview of the project, and find <a href="http://pynq.readthedocs.io" target="_blank">documentation on ReadTheDocs</a> to get started. 

## Overview
This demo utilizes 11 different partial reconfigurable regions that are connected to an AXI-Stream switch.
This Video Pipeline connects both to the raw HDMI ports as well the VDMA.
This allows for configurable combinations of different hardware video filters with very little latency (<600 clock cycles) at 1080p 60fps.
The Filters are:

- ASCII text overlay
- Dilate
- Emboss
- Erode
- Grayscale
- Green Screen
- Image Overlay
- Invert
- Japanese Hiragana text overlay
- Custom 3x3 Kernel
- Line overlay
- Mirror
- RGB filter
- Sobel
- Threshold

Source code will be available  in coming months with the potential to use High-Level Synthesis to design custom filters.
Go from a C file to a Partial Bit file in 20 to 30 mins.

## Quick Start

In order to install it your PYNQ, connect to the board, open a terminal and type:

```shell
# (on PYNQ v2.1)
sudo pip3.6 install git+https://github.com/byuccl/BYU_PYNQ_PR_Video_Pipeline.git
```

Just run the the Demos in the notebooks.  The best video source is the HDMI output on a laptop. If the kernel crashes, try again.

