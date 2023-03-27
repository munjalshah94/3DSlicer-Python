# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 11:24:50 2023

@author: munjalpu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 12:47:48 2022

@author: munjalpu
"""
import slicer 
import time
import vtk
import glob
import os

# Define interpolation for resampling 
INTERPOLATIONTYPE = 'bspline'  # Options:'nearestNeighbor' 'linear'

############### Execute the code using the below line in the Python slicer module. ###############
# exec(open(r"path_to_code\Resample_crop_Two_modalities_segmentations.py").read())

def BatchRegister2():
    base_path=r'path_to_code\output/'
    folder_names = glob.glob(r'path_to_code\original\*')
    
    out_vol_name= base_path +'DL_vol_files_modality1'
    isExist = os.path.exists(out_vol_name)
    if not isExist:
        os.makedirs(out_vol_name)
        
    out_vol_name2= base_path +'DL_vol_files_modality2'
    isExist = os.path.exists(out_vol_name2)
    if not isExist:
        os.makedirs(out_vol_name2)
        
    out_seg_name=base_path+ 'DL_seg_files'     
    isExist = os.path.exists( out_seg_name)
    if not isExist:
        os.makedirs( out_seg_name)   
        
    for folder_name in folder_names:
        Fixedfilename  = folder_name + '/modality1.nii.gz'
        Movingfilename = folder_name + '/modality2.nrrd'
        segmodelname   = folder_name + '/Segmentation.nii'
        fname = os.path.basename(folder_name)
        temp=fname+ '_modality1.nii.gz'
        OutVolumefilename = os.path.join(out_vol_name,temp)
        temp=fname+ '_modality2.nrrd'
        OutVolumefilename2=os.path.join(out_vol_name2,temp)
        temp=fname+ '_seg.nii.gz'
        OutVolumesegname = os.path.join(out_seg_name,temp)  
        
        Register(Fixedfilename, Movingfilename,segmodelname,OutVolumefilename,OutVolumefilename2,OutVolumesegname)
        slicer.mrmlScene.Clear()   

            
def Register(Fixedfilename, Movingfilename,segmodelname,OutVolumefilename,OutVolumefilename2,OutVolumesegname): 

        #Load and get information of modality1 (larger extent, coarser volume)
        orig=slicer.util.loadVolume(Fixedfilename)
        VOXEL_SPACING = orig.GetSpacing()
        
        print('Resampleing the modality2 for voxel sapcing - ',VOXEL_SPACING )
        
        #Resample volume of modality2
        orig2=slicer.util.loadVolume(Movingfilename)
        params={}
        params["InputVolume"]=orig2
        outputVolume_resample2 = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(outputVolume_resample2)
        params["OutputVolume"]=outputVolume_resample2
        params["outputPixelSpacing"]=VOXEL_SPACING
        params["interpolationType"]=INTERPOLATIONTYPE
        output_resample2 = slicer.cli.runSync(slicer.modules.resamplescalarvolume, None, params)
        
        print('Creating ROI based on volume extent of modality2 (smaller volume extent)....')
              
        # create ROI  based on volume extent of modality2
        roiNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")
        cropVolumeParameters = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLCropVolumeParametersNode")
        cropVolumeParameters.SetInputVolumeNodeID(outputVolume_resample2.GetID())
        cropVolumeParameters.SetROINodeID(roiNode.GetID())
        slicer.modules.cropvolume.logic().SnapROIToVoxelGrid(cropVolumeParameters)  # optional (rotates the ROI to match the volume axis directions)
        slicer.modules.cropvolume.logic().FitROIToInputVolume(cropVolumeParameters)
        slicer.mrmlScene.RemoveNode(cropVolumeParameters)
        
        print('Cropping modality1 (larger volume) image based on ROI of modality2...')
        
        # Crop volume of modality1 on ROI of modality2
        croppedvolume = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(croppedvolume)
        cropVolumeLogic = slicer.modules.cropvolume.logic()
        cropVolumeNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropVolumeNode.SetInputVolumeNodeID(orig.GetID())
        cropVolumeNode.SetOutputVolumeNodeID(croppedvolume.GetID())
        cropVolumeNode.SetROINodeID(roiNode.GetID())
        cropVolumeLogic.FitROIToInputVolume(cropVolumeNode)
        cropVolumeLogic.Apply(cropVolumeNode)
        
        
        print('Now svaing both image modalities...')
        # Save modality1
        slicer.util.saveNode(croppedvolume,OutVolumefilename)
        
        # Save modality2
        slicer.util.saveNode(outputVolume_resample2,OutVolumefilename2)
        
        # Crop segmentation on ROI of modality2 created before
        print('Now cropping segmentation...')
        orig3=slicer.util.loadVolume(segmodelname)
        croppedvolume3 = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(croppedvolume3)
        cropVolumeLogic3 = slicer.modules.cropvolume.logic()
        cropVolumeNode3 = slicer.vtkMRMLCropVolumeParametersNode()
        cropVolumeNode3.SetInputVolumeNodeID(orig3.GetID())
        cropVolumeNode3.SetOutputVolumeNodeID(croppedvolume3.GetID())
        cropVolumeNode3.SetROINodeID(roiNode.GetID())
        cropVolumeLogic3.CropInterpolated(roiNode, orig3, croppedvolume3,False,1,1,0)
        
        print('Saving segmentation...')
        slicer.util.saveNode(croppedvolume3,OutVolumesegname)

BatchRegister2()   


