# WriteToFile
# Created by Matt Shenton
# 12/5/17
# purpose: define function to write specified emotion to text file


# arguments (the i/o variable, the line number that will be written, the most likely emotion)
def writeEmotions(emotionFile, lineNum, emotion):
	
	output = str(lineNum) + " " + emotion + "\n"

	emotionFile.write(output)