How to add custom ROI based on a reference volume?
- If the ROI is to be extracted based on a reference image and varies for each case, it can be changed in each loop using this snippet. 

```     referenceVolume=slicer.util.loadVolume(filename)  #put path of reference filename here .nrrd, .nii, or .nii.gz
	inputVolume=slicer.util.loadVolume(inputfilename) #put path of input filename here .nrrd, .nii, or .nii.gz
	OutVolumefilename= 'path/outfile.nii' #Define the path to output node/volume
		
	roiNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")
        cropVolumeParameters = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLCropVolumeParametersNode")
        cropVolumeParameters.SetInputVolumeNodeID(referenceVolume.GetID())
        cropVolumeParameters.SetROINodeID(roiNode.GetID())
        slicer.modules.cropvolume.logic().SnapROIToVoxelGrid(cropVolumeParameters)  # optional (rotates the ROI to match the volume axis directions)
        slicer.modules.cropvolume.logic().FitROIToInputVolume(cropVolumeParameters)
        slicer.mrmlScene.RemoveNode(cropVolumeParameters)
		
		
	croppedvolume = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(croppedvolume)
        cropVolumeLogic = slicer.modules.cropvolume.logic()
        cropVolumeNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropVolumeNode.SetInputVolumeNodeID(inputVolume.GetID())
        cropVolumeNode.SetOutputVolumeNodeID(croppedvolume.GetID())
        cropVolumeNode.SetROINodeID(roiNode.GetID()) #Pass the ROI node created earlier
        cropVolumeLogic.Apply(cropVolumeNode)
        slicer.util.saveNode(croppedvolume,OutVolumefilename)
```
- How to crop segmentation without any information loss?
	There are mutiple ways to crop volume as can be found here in implementaion of [CropVolumeLogic](https://github.com/Slicer/Slicer/blob/main/Modules/Loadable/CropVolume/Logic/vtkSlicerCropVolumeLogic.h).

	To crop input volume using the specified ROI node. Default interpolation algorithm is 'linear'
  ```   
  cropVolumeNode.SetROINodeID(roiNode.GetID())   
  cropVolumeLogic3.Apply(croppedvolume) 
  ```
	
  	To perform non-interpolated (voxel-based) cropping.
  ```  
  cropVolumeLogic3.CropVoxelBased(roiNode, inputVolume, croppedvolume,'false',0.0)
  ```
  	Where, inputs are defined as;
  ```	
  CropVoxelBased(roi, inputVolume,outputNode,limitToInputExtent=true, fillValue=0.0) 
  ```
  
  	To crop with a interpolation algorithm
  ```   
  cropVolumeLogic3.CropInterpolated(roiNode, inputVolume, croppedvolume,False,1,1,0) 
  ```
  	Where, inputs are defined as;
  ```   
  CropInterpolated(roi,inputVolume,outputNode,isotropicResampling=False, spacingScale, interpolationMode,fillValue) 
  ```
	

