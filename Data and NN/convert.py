# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 09:42:40 2018

@author: msolonko
"""
class Converter:
    def convert_test(self, scores):        
        result = []
        for score in scores:
            if score<=36:
                result.append(score)
            else:
                if score>1600:
                    file_name = "old"
                else:
                    file_name = "new"
                conv_list = self.get_conversion_test(file_name)
                for tup in conv_list:
                    if score >= tup[1]:
                        result.append(tup[0])
                        break
                    elif tup[0] == 9:
                        result.append(0)
        return list(map(int, result))
        
    def get_conversion_test(self, f):
        conv_list=[]
        with open(f + "_conversion.txt","r") as inputFile:
            conv_list = [tuple(map(int, line.split(' '))) for line in inputFile.read().splitlines()]
        return sorted(conv_list, key=lambda tup: tup[0], reverse=True)



'''import random
fake_list = []
for i in range(10000):
    fake_list.append(int(random.random() * 600+1000))
print(convert_test(fake_list))'''