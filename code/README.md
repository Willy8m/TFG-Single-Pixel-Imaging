# TFG Single Pixel imaging

As part of my Physics degree final thesis, a single-pixel camera prototype was developed, using an IDS camera and an Icodis projector. This repository will serve as a guide on how to replicate the steps taken to construct the camera and a public showcase of my work.

## Navigating the repository

#### Directories:
- **IDS_camera_interface**: Dedicated readme inside.
- **hadamard**: Storage of hadamard matrices in .npy archives, plus the .py scripts to generate them.
- **reconstructions**: Images reconstructed, both in matricial (.npy) and graphics (.jpg) format. The directories "wifi" and "cable" refer to the data accquired with each technique.
- **src**: Camera control scripts. Credit: Marcos Aviñoá.

#### Python archives:
- **01_PiCamera_test**: Script to test the IDS camera, also provides fps metrics.
- **02_Image_capture**: Main program, connects to the projector through HDMI and to the IDS camera. It displays the set of hadamard matrices through the projector and captures the overall light with the IDS camera. Then produces a reconstruction based on the math explained in the final report.
- **03_ShowWH_matrices**: A script to test the projector and the walsh-hadamard matrices.
- **04_show_npy_reconstruction**: Visualize .npy matrices as images.
- **05_convert npy to jpg**: Converts all .npy files to .jpeg in a given directory.
- **06_Filtering**: FFT filter used to enhance the reconstruction's imaged objects.
- **whdynamic**: Generator of WH matrices, it outputs one matrix at a time, and iterates for an entire set of walsh-hadamard matrices. It was based on code from Credit: Libe López Arandia.





