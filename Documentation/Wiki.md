How to add custom ROI based on a reference volume?
- If the ROI is to be extracted based on a reference image and varies for each case, it can be changed in each looop using this snippet. 

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
        slicer.util.saveNode(croppedvolume,OutVolumefilename)		```