#assistance from chatGPT to make function more efficient using zip() and all()
def isTooSimilar(color, existing, threshold):
        return all(abs(c1 - c2) < threshold for c1, c2 in zip(color, existing))

def calculateMostFrequentHex(app):
    frequent = []
    hexFrequency = app.hexCodeToFrequency.copy()
    #app.mostFrequentHex can hold UP TO 10 values
    #assistance from 
    #https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    sortedColors = sorted(hexFrequency.items(), key=lambda item: item[1], 
                          reverse=True)
    frequent = []
    for color, frequency in sortedColors:
        #if there are already existing similar colors
        if all(not isTooSimilar(color, existing, 50) for existing in frequent):
            frequent.append(color)
            hexFrequency.pop(color)
        #if there are 10 or less
        if len(frequent) >= 10 or len(hexFrequency) == 0:
            break

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