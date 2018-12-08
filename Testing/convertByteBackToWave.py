import wave

rate = 44100

def output_wave(path, frames,nframes):
    output = wave.open(path,'w')
    output.setparams((1,2,rate,nframes,'NONE','not compressed'))
    output.writeframes(frames)
    output.close()

data = open('in.wav','rb').read()

packedData = data

output_wave('out.wav', packedData,315392)
print("Audio File Saved.")

