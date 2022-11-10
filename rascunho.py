import soundfile as sf
import sounddevice as sd
import numpy as np

# Imports
from scipy.io import wavfile
import scipy.signal as sps

# Your new sampling rate
new_rate = 32000

# Read file
sampling_rate, data = wavfile.read("Sample_0007.wav")
data1=data[:,0]
data2=data[:,1]
dataMono=(np.array(data1)+np.array(data2))/2

# Resample data
number_of_samples = round(len(dataMono) * float(new_rate) / sampling_rate)
newData = sps.resample(dataMono, number_of_samples)

wavfile.write('New_sample.wav',new_rate,newData)