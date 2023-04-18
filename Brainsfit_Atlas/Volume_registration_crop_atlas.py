import slicer 
import time
import vtk
import glob 
import sys
import os

# Infomation on flags can be found at: https://readthedocs.org/projects/slicer/downloads/pdf/latest/


# Subsampling percentage for the registration
SAMPLINGPERCENTAGE=0.05

#voxel sacping for resampling
VOXEL_SPACING=[0.223,0.223,0.223]

#Initialize Transform Mode

# Rigid (6 DOF) (useRigid): Perform a rigid registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.
# Rigid+Scale(7 DOF) (useScaleVersor3D): Perform a ScaleVersor3D registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.
# Rigid+Scale+Skew(10 DOF) (useScaleSkewVersor3D): Perform a ScaleSkewVersor3D registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.
# Affine(12 DOF) (useAffine): Perform an Affine registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.
# BSpline (>27 DOF) (useBSpline): Perform a BSpline registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.
# SyN (useSyN): Perform a SyN registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.
# Composite (many DOF) (useComposite): Perform a Composite registration as part of the sequential registration steps. This family of options overrides the use of transformType if any of them are set.

# Options: useRigid,useScaleVersor3D,useScaleSkewVersor3D,useAffine,useBSpline,useSyN,useComposite3D
AFFINE = "useAffine"

# Initialize Transform Mode (initializeTransformMode): Determine how to initialize the transform center. 'useMomentsAlign' assumes that the center of mass of the images represent similar structures. 'useCenterOfHeadAlign' attempts to use the top of head and shape of neck to drive a center of mass estimate. 'useGeometryAlign' on assumes that the center of the voxel lattice of the images represent similar structures. 'Off' assumes that the physical space of the images are close. This flag is mutually exclusive with the Initialization transform.

ALIGN_METHOD= 'useCenterOfHeadAlign' # Options: 'useGeometryAlign' 'useMomentsAlign' 'Off'

# Sampling algorithm

INTERPOLATIONTYPE = 'bspline'  # Options:'nearestNeighbor' 'linear'
INTERPOLATIONTYPE_SEG = 'nearestNeighbor'  # Options:'nearestNeighbor' 'linear'

############### Execute the code using the below line in the Python slicer module. ###############

# exec(open(r"D:\Github_Data\test/Volume_registration_crop_atlas.py").read())


 ##### Modify the below fucntion to read files per your folder structure #####

 
def BatchRegister2():
    folder_names = glob.glob(r'path_to_code\original\*')
    current_folder= r'D:\Github_Data/test'
    Fixedfilename=current_folder + "/Reference/Atlas.nrrd"
    roi_name=current_folder + "/Reference/ROI.mrk.json"
    
    output_folder= current_folder+'/output'
    isExist = os.path.exists(output_folder)
    if not isExist:
        os.makedirs(output_folder)
        
    out_vol_name=output_folder+ "/DL_vol_files"
    isExist = os.path.exists(out_vol_name)
    if not isExist:
        os.makedirs(out_vol_name)
        
    out_seg_name=output_folder+ "/DL_seg_files"   
    isExist = os.path.exists(out_seg_name)
    if not isExist:
        os.makedirs(out_seg_name)
        
    for folder_name in folder_names:
        file_names = glob.glob(folder_name+ '/*.nii.gz')
        for file_name in file_names:
            Movingfilename = file_name
            e = os.path.basename(Movingfilename)
            fname,ext = os.path.splitext(e)
            fname=fname[:-4:]
            temp=fname+ '_ROI.nii.gz'
            OutVolumefilename = os.path.join(out_vol_name,temp)
            temp=fname+ '.seg.nrrd'
            segmodelname = os.path.join(folder_name,temp)
            temp=fname+ '_ROI_seg.nii.gz'
            OutVolumesegname = os.path.join(out_seg_name,temp)       
            Register(Fixedfilename, Movingfilename,roi_name,segmodelname,OutVolumefilename,OutVolumesegname)
            slicer.mrmlScene.Clear()   
            
def Register(Fixedfilename,Movingfilename,roi_name,segmodelname,OutVolumefilename,OutVolumesegname):
    
        atlas=slicer.util.loadVolume(Fixedfilename)
        orig=slicer.util.loadVolume(Movingfilename)
        roi_atlas=slicer.util.loadMarkups(roi_name)
        seg_model=slicer.util.loadVolume(segmodelname)
        
        print('Starting BRAINSFIT for:', os.path.basename(Movingfilename))
        
        #BRAINSfit using Affine
        parameters = {}
        parameters["fixedVolume"] = atlas
        parameters["movingVolume"] = orig
        parameters["outputVolume"] = orig
        outputTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(outputTransform)
        outputTransform.SetName("Transform_New")
        parameters["linearTransform"] = outputTransform
        parameters[AFFINE] = True            
        parameters["initializeTransformMode"] = ALIGN_METHOD
        parameters["samplingPercentage"] = SAMPLINGPERCENTAGE
        output_Reg = slicer.cli.runSync(slicer.modules.brainsfit, None, parameters)
        
        print('BRAINSFIT Completed!! Now inverting and hardening Transformation matrix')
        #Invert the transform matrix
        matrix=vtk.vtkMatrix4x4()
        outputTransform.GetMatrixTransformToWorld(matrix)
        matrix.Invert()
        transformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', 'Transformation')
        transformNode.SetMatrixTransformToParent(matrix)
    
        #Transform and harden the ROI
        roi_atlas.SetAndObserveTransformNodeID(transformNode.GetID())
        logic2 = slicer.vtkSlicerTransformLogic()
        logic2.hardenTransform(roi_atlas)
        
        print('Resampling the image for voxel spacing - ',VOXEL_SPACING )
        
        #Resample image
        orig2=slicer.util.loadVolume(Movingfilename)
        params={}
        params["InputVolume"]=orig2
        outputVolume_resample = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(outputVolume_resample)
        params["OutputVolume"]=outputVolume_resample
        params["outputPixelSpacing"]=VOXEL_SPACING
        params["interpolationType"]= INTERPOLATIONTYPE
        output_resample = slicer.cli.runSync(slicer.modules.resamplescalarvolume, None, params)
        print('Cropping....')
        
        #Crop image to ROI
        croppedvolume = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(croppedvolume)
        cropVolumeLogic = slicer.modules.cropvolume.logic()
        cropVolumeNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropVolumeNode.SetInputVolumeNodeID(outputVolume_resample.GetID())
        cropVolumeNode.SetOutputVolumeNodeID(croppedvolume.GetID())
        cropVolumeNode.SetROINodeID(roi_atlas.GetID())
        cropVolumeLogic.Apply(cropVolumeNode)
        slicer.util.saveNode(croppedvolume,OutVolumefilename)
        
        print('Volume resampled and cropped')
        
        # # only use this code to resample segmntation to ROI
        
        print('Now doing segmentation...')

        #Resample segmentation
        orig3=slicer.util.loadVolume(segmodelname)
        params={}
        params["InputVolume"]=orig3
        outputVolume_resample2 = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(outputVolume_resample2)
        params["OutputVolume"]=outputVolume_resample2
        params["outputPixelSpacing"]=VOXEL_SPACING
        params["interpolationType"]=INTERPOLATIONTYPE_SEG
        output_resample2 = slicer.cli.runSync(slicer.modules.resamplescalarvolume, None, params)
                
        # Crop segmentation to ROI
        croppedvolume2 = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(croppedvolume2)
        cropVolumeLogic2 = slicer.modules.cropvolume.logic()
        cropVolumeNode2 = slicer.vtkMRMLCropVolumeParametersNode()
        cropVolumeNode2.SetInputVolumeNodeID(outputVolume_resample2.GetID())
        cropVolumeNode2.SetOutputVolumeNodeID(croppedvolume2.GetID())
        cropVolumeNode2.SetROINodeID(roi_atlas.GetID())
        cropVolumeLogic2.Apply(cropVolumeNode2)
        slicer.util.saveNode(croppedvolume2,OutVolumesegname)
        
        print('Segmentation cropped')
        
BatchRegister2()


