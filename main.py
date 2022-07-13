import os
from collections import OrderedDict

import easyocr
import cv2
# from matplotlib import pyplot as plt
import numpy as np
import xlwt
from xlwt import Workbook
from xlutils.copy import copy
import xlrd
import spacy
from spacy import displacy
import zope.interface
from pyexcel_ods import save_data
from pyexcel_ods import get_data
import json
import os.path
import sys


def getAuthor(result):
    NER = spacy.load("en_core_web_sm")
    author = "No Author Detected  "
    temp = ""
    for elem in result:
        raw_text = elem[1]
        text = NER(raw_text)
        flag = False
        for word in text.ents:
            if word.label_ == "PERSON":
                flag = True
        if flag and len(raw_text) < 30:
            temp += raw_text
            temp += ", "
            author = temp
    author = author[:-2]
    return author


def getTitle(result):
    maxVal = 0
    title = "No Title Detected"
    for elem in result:
        temp = abs(elem[0][0][0] - elem[0][1][0]) * abs(elem[0][1][1] - elem[0][2][1])
        if temp > maxVal and len(elem[1]) < 80:
            maxVal = temp
            title = elem[1]

    return title


def getISBN(result):
    isbn = "No ISBN Number Detected"
    for elem in result:
        if ((elem[1][0] == 'I' or elem[1][0] == 'i') and (elem[1][1] == 'S' or elem[1][1] == 's') and (
                elem[1][2] == 'B' or elem[1][2] == 'b') and (elem[1][3] == 'N' or elem[1][3] == 'n')):
            isbn = elem[1]
    return isbn


def getPublisher(result):
    publisher = "No Publisher Detected"
    maxVal = 0
    for elem in result:
        temp = abs(elem[0][0][0] - elem[0][1][0]) * abs(elem[0][1][1] - elem[0][2][1])
        if temp > maxVal:
            maxVal = temp

    NER = spacy.load("en_core_web_sm")
    for elem in result:
        temp = abs(elem[0][0][0] - elem[0][1][0]) * abs(elem[0][1][1] - elem[0][2][1])
        raw_text = elem[1]
        text = NER(raw_text)
        flag = True
        if temp == maxVal:
            continue
        for word in text.ents:
            if word.label_ == "PERSON":
                flag = False
        if flag and 40 > len(raw_text) > 5:
            publisher = raw_text
    return publisher


def processBookCover(path):
    IMAGE_PATH = path
    reader = easyocr.Reader(['en'])
    result = reader.readtext(IMAGE_PATH, paragraph="False")

    title = getTitle(result)
    author = getAuthor(result)
    publisher = getPublisher(result)
    isbn = getISBN(result)

    print("Title : " + title)
    print("Authors : " + author)
    print("Publisher : " + publisher)
    print("ISBN Number : " + isbn)

    file = open('config.json')
    fileData = json.load(file)
    fileName = fileData['output']

    if os.path.exists(fileName):
        excelData = get_data(fileName)
        excelArray = excelData['Sheet1']
        data = OrderedDict()

        excelArray.append([title, author, publisher, isbn])
        data.update({"Sheet1": excelArray})
        save_data(fileName, data)
        return [title, author, publisher, isbn]
    else:
        print("No such file. Make changes to the configuration file")
        return "No such file. Make changes to the configuration file"


class BookCoverInterface(zope.interface.Interface):
    def processBookCoverMain(self, pathToImage):
        pass


@zope.interface.implementer(BookCoverInterface)
class BookCoverClass:
    def processBookCoverMain(self, pathToImage):
        return processBookCover(pathToImage)


def start(val, path):
    if val != '0' and val != '1':
        print("Invalid Format Selected")
        return "Invalid Format Selected"
    else:
        val = int(val)

        if val == 0:
            if os.path.exists(path):
                obj = BookCoverClass()
                return obj.processBookCoverMain(path)
            else:
                print("Incorrect File Path Provided")
                return "Incorrect File Path Provided"
        else:
            if os.path.exists(path):
                directory = path
                ans = []
                for filename in os.listdir(directory):
                    f = os.path.join(directory, filename)
                    # checking if it is a file ( There might be folders inside folders )
                    if os.path.isfile(f):
                        obj = BookCoverClass()
                        ans.append(obj.processBookCoverMain(f))
                return ans
            else:
                print("Incorrect Directory Path Provided")
                return "Incorrect Directory Path Provided"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid Input Format. Read the README")
    else:
        start(sys.argv[1], sys.argv[2])
