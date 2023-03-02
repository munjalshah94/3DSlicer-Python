# 3DSlicer-Python
Python automated 3D slicer pipeline to convert different image modalities to DL ready image data


## Table of contents

* [Inputs](#inputs)
* [Running-code](#run-code)
* [Outputs](#outputs)
* [Dependencies](#dependencies)
* [Useful-links](#links)

## Inputs
The python code is tested on given formats: ```.nrrd, .nii, .nii.gz, .seg.nrrd ```. However, It should work on any volume node that can be imported via [```slicer.util.loadVolume```](https://slicer.readthedocs.io/en/v4.11/developer_guide/slicer.html?highlight=util.loadVolume#slicer.util.loadVolume). More information on python scripting commands can be found at [3D slicer Docs](https://slicer.readthedocs.io/en/v4.11/index.html). 

📦**Parent Directory**          &emsp; &emsp;  
  ┣ 📂**Reference**  
&ensp; &ensp;    ┣ 📜*Atlas.nrrd*  
&ensp; &ensp;    ┗ 📜*ROI_atlas.mrk.json*  
  ┣ 📂**Original**  
  &ensp; &ensp;    ┣ 📂case1                     
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜Modality1.nii.gz  
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜Modality2.nrrd  
  &ensp; &ensp; ┃ &nbsp;    ┗ 📜mask.seg.nrrd  
  &ensp; &ensp;    ┣ 📂case2                     
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜Modality1.nii.gz  
  &ensp; &ensp; ┃ &nbsp;    ┣ 📜Modality2.nrrd  
  &ensp; &ensp; ┃ &nbsp;    ┗ 📜mask.seg.nrrd  
  &ensp; &ensp; ┗ ...                             
  ┣ 📂**ImageModality2_out**  
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
## Running-code
- Locate the python icon in your slicer GUI.
- It should open up a python consol at the bottom of the screen.
- Execute the python script using command : ``` exec(open(r"D:\folder1/folder2/slicer_python_processing_code.py").read()) ```
![Image1](Documentation/step1.png)

## Outputs
- The code will output the image or mask with any extension supported by 3D slicer under [```slicer.util.saveNode```](https://slicer.readthedocs.io/en/latest/developer_guide/slicer.html#slicer.util.saveNode)



## Dependencies
The python codes were tested and implemented on ```3D slicer 5.0.3 (r30893/7ea0f43)```. You can access older versions of 3D slicer [here](https://slicer-packages.kitware.com/#collection/5f4474d0e1d8c75dfc70547e/folder/5f4474d0e1d8c75dfc705482).

## Useful-links
-[forum](https://discourse.slicer.org/)
-[Python related posts](https://discourse.slicer.org/tag/python)
-[API](https://slicer.readthedocs.io/en/latest/developer_guide/slicer.html) ```slicer.util and slicer.logic``` are most frequently used for volume operations. 
-[Script-repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)

