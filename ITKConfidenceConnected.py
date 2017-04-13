# Install ITK
import pip
pip.main(['install', '--upgrade', 'pip'])
pip.main(['install', 'itk', '-f', 'https://github.com/InsightSoftwareConsortium/ITKPythonPackage/releases/tag/latest'])

import itk


# Get a brain MRI dataset
pip.main(['install', 'requests'])
import requests

url = 'https://data.kitware.com/api/v1/file/588271308d777f4f3f3072e2/download'
filename = 'brainweb165a10f17.mha'

request = requests.get(url)
with open('brainweb165a10f17.mha', 'wb') as fp:
    fp.write(request.content)

# Read in the image
reader = itk.ImageFileReader.New(FileName=filename)
reader.Update()
input_image = reader.GetOutput()
print(input_image)


# The image type we will use to process the image
PixelType = itk.ctype('float')
Dimension = 3

ImageType = itk.Image[PixelType, Dimension]


InputImageType = type(input_image)
caster = itk.CastImageFilter[InputImageType, ImageType].New(input_image)


# Smooth the image
smoother = itk.CurvatureFlowImageFilter.New(caster.GetOutput())
smoother.SetNumberOfIterations(6)
smoother.SetTimeStep(0.05)


confidence_connected = itk.ConfidenceConnectedImageFilter[ImageType, InputImageType].New()
confidence_connected.SetInput(smoother.GetOutput())
confidence_connected.SetMultiplier(2.5)
confidence_connected.SetNumberOfIterations(5)
confidence_connected.SetInitialNeighborhoodRadius(2)
confidence_connected.SetReplaceValue(255)

SeedType = itk.Index[Dimension]
seed1 = SeedType()
seed1[0] = 118
seed1[1] = 133
seed1[2] = 92
confidence_connected.AddSeed(seed1)

seed2 = SeedType()
seed2[0] = 63
seed2[1] = 135
seed2[2] = 94
confidence_connected.AddSeed(seed2)

seed3 = SeedType()
seed3[0] = 63
seed3[1] = 157
seed3[2] = 90
confidence_connected.AddSeed(seed3)

seed4 = SeedType()
seed4[0] = 111
seed4[1] = 150
seed4[2] = 90
confidence_connected.AddSeed(seed4)

seed5 = SeedType()
seed5[0] = 111
seed5[1] = 50
seed5[2] = 88
confidence_connected.AddSeed(seed5)


writer = itk.ImageFileWriter.New(confidence_connected.GetOutput())
writer.SetFileName('WhiteMatterSegmentation.mha')


# Runs the processing pipeline
writer.Update()
