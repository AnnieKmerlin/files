import gzip
import wget
import re
import requests
from lxml import etree
import sys

def cna_parse(input_file, output_text):
    base_url = 'https://api.github.com/repos/AnnieKmerlin/files/contents'
    r = requests.get(base_url)
    if r.status_code != 200:
        print('Failed to get the downloading list.')

    with open(output_text, 'w') as of:
        files = r.json()
        pattern = re.compile(input_file)
        for file in files:
            file_name = file['name']
            if pattern.match(file_name):
                #wget to download the files
                downloaded_file = wget.download(file['download_url'])    
                #gzip to decompress the files
                with gzip.open(downloaded_file, 'rb') as f:
                    file_content = f.read().decode('utf-8')
                    root = etree.XML(file_content)

                    items = root.xpath('//*[@type="story"]')
                    for item in items:
                        story = ''
                        paragraphs = item.xpath('.//TEXT//P')
                        print(paragraphs[0].text)
                        if paragraphs != None:
                            for paragraph in paragraphs:
                                if paragraph.text != None:
                                    story += paragraph.text + '\r\n'

                        of.write(story + '\r\n')        

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        file_path = args[1]
        output_file = args[2]
        
        if file_path != None and output_file != None:
            cna_parse(file_path, output_file)
            exit()
            
    print('Please input file name and output file')
