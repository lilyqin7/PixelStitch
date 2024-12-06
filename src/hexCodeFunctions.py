def calculateMostFrequentHex(app):
    frequent = []
    hexFrequency = app.hexCodeToFrequency.copy()
    #app.mostFrequentHex can hold UP TO 10 values
    #if there aren't 10 vastly unique colors, loop will still terminate
    while len(frequent) < 10 and len(hexFrequency) > 0:
        num = 0
        code = None
        #searches through app.hexCodeToFrequency for most frequent hex code
        for val in hexFrequency:
            if hexFrequency[val] > num:
                num = hexFrequency[val]
                code = val
        #adds new value frequent, removes from old dictionary
        frequent.append(code)
        hexFrequency.pop(code)
        #search through app.mostFrequentHex and pop too similar colors
        j = 0
        while j < len(frequent):
            rgbVal = frequent[j]
            r = rgbVal[0]
            g = rgbVal[1]
            b = rgbVal[2]
            k = j + 1
            while k < len(frequent):
                nextVal = frequent[k]
        #if all rgb differences are less than threshold, colors are too similar
                threshold = 50
                if (abs(nextVal[0] - r) < threshold and abs(nextVal[1] - g) < 
                    threshold and abs(nextVal[2] - b) < threshold):
                    frequent.pop()
                k += 1
            j += 1
    return frequent
   
#goes through all x and y computer pixels and calculates frequncy of each color
#returns dictionary
def calculateHexCodes(app, pilImage):
    d = {}
    for x in range(pilImage.width):
        for y in range(pilImage.height):
            rgb = pilImage.getpixel((x, y))
            d[rgb] = d.get(rgb, 0) + 1
    return d