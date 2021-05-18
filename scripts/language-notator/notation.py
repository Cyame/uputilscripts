from logging import fatal
import pypinyin
from yaml.loader import FullLoader
import xlwt
import yaml
import os
import sys
import string
import re


def checkWord(Chinese,Pinyin):
    py = pypinyin.pinyin(Chinese,heteronym=True,style=pypinyin.Style.TONE3,neutral_tone_with_five=True)
    if Pinyin in py[0]:
        return True
    else:
        return False

def getLine(wordLine, dictionary):
    pyLine = pypinyin.lazy_pinyin(wordLine,style=pypinyin.Style.TONE3,strict=False,neutral_tone_with_five=True,errors=lambda x: {'unCN': x})
    thisKanaLine = []
    for word in pyLine:
        if type(word) == dict: # Dealing trans-words
            thisKana = word['unCN']
        elif word.isalnum() and not word.isdigit(): # Pinyin
            thisTune = int(word[-1])
            thisPron = word[:-1]
            # 1-5<tune> --> 0-4<list>
            thisKana = dictionary[thisPron][thisTune-1]
        else: # Excpetions: Num & EN
            thisKana = word
        thisKanaLine.append(thisKana)
    return thisKanaLine

def readYaml(filePath):
    config = []
    with open(filePath,'r',encoding='utf8') as ymlfile:
        cfg = yaml.load_all(ymlfile, Loader= yaml.FullLoader)
        for conf in cfg:
            config.append(conf)
    print('You are going to generate a result as: ', config[0]['output-type'])
    return config[0]['output-type'],config[1]

def outputXls(originLines,resLines):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Notation')
    for index in range(len(originLines)):
        for wordIndex in range(len(resLines[index])):
            sheet.write(index*2+1,wordIndex+1,resLines[index][wordIndex])
        for wordIndex in range(len(originLines[index])):
            sheet.write(index*2,wordIndex+1,originLines[index][wordIndex])
    wbk.save("noted.xls")


def outputQuote(originLines,resLines):
    with open("notedQuote.txt","w",encoding="utf8") as quoText:
        for lineIndex in range(len(resLines)):
            for wordIndex in range(len(resLines[lineIndex])):
                quoText.write(f'{originLines[lineIndex][wordIndex]}({resLines[lineIndex][wordIndex]})')
    pass

def outputLine(originLines,resLines):
    with open("notedLine.txt","w",encoding="utf8") as ouText:
        for index in range(len(resLines)):
            ouText.write("".join(resLines[index]))
            ouText.write("".join(originLines[index]))
    pass

def outputTypeDealer(mode, originLines, resLines):
    if mode == 'xls':
        outputXls(originLines, resLines)
        pass
    elif mode == 'quote':
        outputQuote(originLines, resLines)
        pass
    elif mode == 'line':
        outputLine(originLines, resLines)
        pass
    else:
        raise IOError("Invalid Output Type")
    pass

if __name__ == "__main__":
    # Initialization
    currentPath = os.getcwd()
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(scriptPath,'rules.yml')
    try:
        targetFilePath = sys.argv[1]
    except:
        raise IOError("Another parameter needed. Did you run with your txt file path?")
    # Read Config
    outputType, dictionary = readYaml(yamlPath)
    # Read File
    resLines = []
    originLines = []
    with open(targetFilePath,'r',encoding='utf8') as content:
        for line in content.readlines():
            # Exec
            thisResLine = getLine(line,dictionary)
            buffer = []
            thisOriginLine = []
            chnReStr = ".*?([\u4E00-\u9FA5]+).*?"
            for word in line:
                if re.search(chnReStr,word) == None:
                    buffer.append(word)
                else:
                    if buffer != list():
                        thisOriginLine.append("".join(buffer))
                    buffer = []
                    thisOriginLine.append(word)
            if buffer != list():
                thisOriginLine.append("".join(buffer))
            # if thisOriginLine != list():
            #     originLines.append(thisOriginLine)
            originLines.append(thisOriginLine)
            resLines.append(thisResLine)
        pass
    # print(originLines)
    # print(resLines)
    # Output
    outputTypeDealer(outputType,originLines,resLines)