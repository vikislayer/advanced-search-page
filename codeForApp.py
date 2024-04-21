def removePunctuationAndToStringArray(stringWithCommaAndSpeechMarks):
    outputArray = []
    tempString =""
    switch = True
    for character in stringWithCommaAndSpeechMarks:
        if(character=="\""):
            switch = not switch
            if(switch==True):
                outputArray.append(tempString)
                tempString = ""
        elif(character=="," or character==" " or character=="[" or character=="]"):
            pass
        else:
            tempString += character
        
    return outputArray

print("\"Hello\", \"World\"")
print(removePunctuationAndToStringArray("\"Hello\", \"World\""))