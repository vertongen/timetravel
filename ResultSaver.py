import json

class ResultSaver:

    def SaveTemplate(self, address, tweets, images, satelliteImages):
        resultFileName = 'output/' + address + '.html'
        with open("template/template.html", "r") as file:
            template = file.read()
            visDataset = ""
            for tweet in tweets:
                visDataset += ("{start: new Date(")
                visDataset += (str(tweet['time']*1000))
                visDataset += ("), content: '")
                visDataset += ('<a target="_blank" href="' + tweet['url'].replace("'", "\\'") + '" >' + tweet['text'].replace('\'', '').replace('\n', '') + '</a>')
                visDataset += ("'},")
            
            for image in images:
                visDataset += ("{start: new Date(")
                visDataset += (str(image['time']*1000))
                visDataset += ("), content: '")
                visDataset += ('<a target="_blank" href="' + image['url'].replace("'", "\\'") + '" >')
                visDataset += ('<img src="' + image['imageUrl'] + '" width="50px"></a>')
                visDataset += ("'},\n")
            

            for image in satelliteImages:
                visDataset += ("{start: new Date(")
                visDataset += (str(image['time']*1000))
                visDataset += ("), content: '")
                visDataset += ('<a target="_blank" href="' + image['url'].replace("'", "\\'") + '" >' + image['name'].replace('\'', '').replace('\n', '') + '</a>')
                visDataset += ("'},\n")

                
            template = template.replace('$$dataset$$', visDataset)
            template = template.replace('$$address$$', address)
            with open(resultFileName, "w+") as result:
                result.write(template)