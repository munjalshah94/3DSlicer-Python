# 3DSlicer-Python
Python automated 3D slicer pipeline to convert different image modalities to DL ready image data


## Table of contents
* [Scripts](#scripts)
* [Inputs](#inputs)
* [Running-code](#run-code)
* [Outputs](#outputs)
* [Dependencies](#dependencies)
* [Useful-links](#links)

## Scripts
The repository includes below mentioned python scripts for various image operations. 
  - Crop Volume with a reference-ROI or volume-fit-ROI
  - General Registration (BRAINS)
  - Resample Scalar Volume
  - N4ITK MRI Bias Correction 

 ### Example scripts
  ```📜 Volume_registration_crop_atlas.py ```
  
        Registration of volume using BRAINS algorithm. The reference atlas used in the code can be found [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7274757/) Firstly, a transformation matrix is calculated to map image onto Atlas. The inverse of transformation matrix is used to map ROI onto the image. The image is then resampled from voxel spacing of n1xn2xn3 to m1xm2xm3 and exported.  Options for BRAINSfit algorithm and resampling can be found in config.py
  ![Image1](Documentation/Brainsfit_crop_resample.png)
  ```📜 Fit_to_Volume_resample.py ```
      
  ``` 📜 MRI_Bias_correction.py ```
      




## Inputs
The python code is tested on given formats: ```.nrrd, .nii, .nii.gz, .seg.nrrd ```. However, It should work on any volume node that can be imported via [```slicer.util.loadVolume```](https://slicer.readthedocs.io/en/v4.11/developer_guide/slicer.html?highlight=util.loadVolume#slicer.util.loadVolume). More information on python scripting commands can be found at [3D slicer Docs](https://slicer.readthedocs.io/en/v4.11/index.html). 

📦**Parent Directory**          &emsp; &emsp;  
  ┣ 📂**Reference**  
&ensp; &ensp;    ┣ 📜*Atlas.nrrd*  
&ensp; &ensp;    ┗ 📜*ROI_atlas.mrk.json*  
  ┣ 📂**Original**  
  &ensp; &ensp;    ┣ 📂case1                     
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜ImageModality1.nii.gz  
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜ImageModality2.nrrd  
  &ensp; &ensp; ┃ &nbsp;    ┗ 📜mask.seg.nrrd  
  &ensp; &ensp;    ┣ 📂case2                     
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜ImageModality1.nii.gz  
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜ImageModality2.nrrd  
  &ensp; &ensp; ┃ &nbsp;    ┗ 📜mask.seg.nrrd  
  &ensp; &ensp; ┗ ...                             
  
## Running-code
- Locate the python icon in your slicer GUI.
- It should open up a python consol at the bottom of the screen.
- Execute the python script using command : ``` exec(open(r"D:\folder1/folder2/slicer_python_processing_code.py").read()) ```
![Image1](Documentation/step1.png)

## Outputs
- The code will output the image or mask with any extension supported by 3D slicer under [```slicer.util.saveNode```](https://slicer.readthedocs.io/en/latest/developer_guide/slicer.html#slicer.util.saveNode)
- The outputs will be sorted based on image modalities provided by user in the config file. Output folders will be created based on image modalities inputs given by user.
 
📦**Output Directory**          &emsp; &emsp;  
  ┣ 📂**ImageModality1_out**  
  &ensp; &ensp;    ┣ 📜Case1.nii.gz  
  &ensp; &ensp;    ┣ 📜Case2.nii.gz   
  &ensp; &ensp;    ┣ 📜Case3.nii.gz  
  &ensp; &ensp;    ┗ ...  
  ┣ 📂**ImageModality2_out**  
  &ensp; &ensp;    ┣ 📜Case1.nrrd  
  &ensp; &ensp;    ┣ 📜Case2.nrrd   
  &ensp; &ensp;    ┣ 📜Case3.nrrd  
  &ensp; &ensp;    ┗ ...    
  ┗ 📂**Mask_out**  
  &ensp; &ensp;    ┣ 📜Case1.nii.gz  
  &ensp; &ensp;    ┣ 📜Case2.nii.gz   
  &ensp; &ensp;    ┣ 📜Case3.nii.gz  
  &ensp; &ensp;    ┗ ... 


## Dependencies
The python codes were tested and implemented on ```3D slicer 5.0.3 (r30893/7ea0f43)```. You can access older versions of 3D slicer [here](https://slicer-packages.kitware.com/#collection/5f4474d0e1d8c75dfc70547e/folder/5f4474d0e1d8c75dfc705482).

## Useful-links
- [Forum](https://discourse.slicer.org/) and  [Python](https://discourse.slicer.org/tag/python) related posts
- [API](https://slicer.readthedocs.io/en/latest/developer_guide/slicer.html) ```slicer.util and slicer.logic``` are most frequently used for volume operations. 
- [Script-repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)

## Keywords
3D Slicer, Python scripting, Region Of Interest (ROI), Volume cropping, Resample image, MRI Bias correction