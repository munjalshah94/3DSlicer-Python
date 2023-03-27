# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:58:05 2023

@author: munjalpu
"""


import slicer 
import time
import vtk
import glob
import os


# https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html

# https://www.insight-journal.org/browse/publication/640


# BSpline grid resolution (initialMeshResolution): Resolution of the initial bspline grid defined as a sequence of three numbers. The actual resolution will be defined by adding the bspline order (default is 3) to the resolution in each dimension specified here. For example, 1,1,1 will result in a 4x4x4 grid of control points. This parameter may need to be adjusted based on your input image. In the multi-resolution N4 framework, the resolution of the bspline grid at subsequent iterations will be doubled. The number of resolutions is implicitly defined by Number of iterations parameter (the size of this list is the number of resolutions)

initialMeshResolution=(1,1,1)
# Spline distance (splineDistance): An alternative means to define the spline grid, by setting the distance between the control points. This parameter is used only if the grid resolution is not specified.
splineDistance=0.00
# Bias field Full Width at Half Maximum (bfFWHM): Bias field Full Width at Half Maximum. Zero implies use of the default value.
bfFWHM=0.00
# Number of iterations (numberOfIterations): Maximum number of iterations at each level of resolution. Larger values will increase execution time, but may lead to better results.
numberOfIterations=(50,40,30)
# Convergence threshold (convergenceThreshold): Stopping criterion for the iterative bias estimation. Larger values will lead to smaller execution time.
convergenceThreshold=0.0001
# BSpline order (bsplineOrder): Order of B-spline used in the approximation. Larger values will lead to longer execution times, may result in overfitting and poor result.
bsplineOrder=3
# Shrink factor (shrinkFactor): Defines how much the image should be upsampled before estimating the inhomogeneity field. Increase if you want to reduce the execution time. 1 corresponds to the original resolution. Larger values will significantly reduce the computation time.
shrinkFactor=4
# Weight Image (weightImageName): Weight Image

# Wiener filter noise (wienerFilterNoise): Wiener filter noise. Zero implies use of the default value.
wienerFilterNoise=0.00
# Number of histogram bins (nHistogramBins): Number of histogram bins. Zero implies use of the default value.
nHistogramBins=0


# exec(open(r"D:\Github_Data\test/N4ITKbias.py").read())     

def BatchRegister2():
    folder_names = glob.glob(r'D:\Github_Data\test\MRA\*')
    current_folder= r'D:\Github_Data/test'
    
    output_folder= current_folder+'/output'
    isExist = os.path.exists(output_folder)
    if not isExist:
        os.makedirs(output_folder)
        
        
    for folder_name in folder_names:
        file_names = glob.glob(folder_name+ '/*.nii.gz')
        for filename in file_names:
            temp=os.path.join(output_folder, os.path.basename(folder_name))
            temp=temp+ '_Bias_Corrected.nii.gz'
            OutVolumefilename = temp
            print(OutVolumefilename)
            Register(filename,OutVolumefilename)
            slicer.mrmlScene.Clear()   

def Register(filename,OutVolumefilename): 
        
        orig=slicer.util.loadVolume(filename)
        outputVolume = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(outputVolume)
        parameters={}
        parameters['initialMeshResolution']=initialMeshResolution
        parameters['splineDistance']=splineDistance
        parameters['bfFWHM']=bfFWHM
        parameters['numberOfIterations']=numberOfIterations
        parameters['convergenceThreshold']=convergenceThreshold
        parameters['bsplineOrder']=bsplineOrder
        parameters['shrinkFactor']=shrinkFactor
        parameters['weightImageName']='None'
        parameters['wienerFilterNoise']=wienerFilterNoise
        parameters['nHistogramBins']=nHistogramBins
        parameters['inputImageName']=orig.GetID()
        parameters['maskImageName']='None'
        parameters['outputImageName']=outputVolume.GetID()
        parameters['outputBiasFieldName']='None'
        
        slicer.cli.runSync(slicer.modules.n4itkbiasfieldcorrection,node=None,parameters=parameters)
        
        slicer.util.saveNode(outputVolume,OutVolumefilename)
        
        
        
        
   
BatchRegister2()   
