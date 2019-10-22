import json

class ResultSaver:

    def SaveTemplate(self, address, tweets, images):
        resultFileName = 'output/' + address + '.html'
        with open("template/template.html", "r") as file:
            template = file.read()
            visDataset = ""
            for tweet in tweets:
                visDataset += ("{start: new Date(")
                visDataset += (str(tweet['time']*1000))
                visDataset += ("), content: '")
                visDataset += (tweet['text'].replace('\'', '').replace('\n', ''))
                visDataset += ("'},")
            
            for image in images:
                visDataset += ("{start: new Date(")
                visDataset += (str(image['time']*1000))
                visDataset += ("), content: '")
                visDataset += ('<img src="' + image['imageUrl'] + '" width="50px">')
                visDataset += ("'},")

                
            template = template.replace('$$dataset$$', visDataset)
            template = template.replace('$$address$$', address)
            with open(resultFileName, "w+") as result:
                result.write(template)