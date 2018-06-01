#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import numpy

def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.

    Main algorithm used is dynamic programming.

    Attributes:
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d

def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.

    Attributes:
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0:
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]:
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y-1]+1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]

def alignedPrint(list, r, h, result, tag):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.

    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
        tag    -> indicate printing style for CER or WER.
    '''
    print "REF:",
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print " "*(len(h[index])),
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                print r[index1] + " " * (len(h[index2])-len(r[index1])),
            else:
                print r[index1],
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print r[index],
    if tag == "wer":
        print
    print "HYP:",
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print " " * (len(r[index])),
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print h[index2] + " " * (len(r[index1])-len(h[index2])),
            else:
                print h[index2],
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print h[index],
    if tag == "wer":
        print
    print "EVA:",
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print "D" + " " * (len(r[index])-1),
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print "I" + " " * (len(h[index])-1),
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print "S" + " " * (len(r[index1])-1),
            else:
                print "S" + " " * (len(h[index2])-1),
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print " " * (len(r[index])),
    print
    if tag == "cer":
        print "CER: " + result
    else:
        print "WER: " + result
    print

def singleErrorRate(r, h, tag):
    """
    This is a function that calculate the WER or CER for a single sentence input.
    """
    # build the matrix

    d= editDistance(r, h)

    # find out the manipulation steps
    list = getStepList(r, h, d)

    # print the result in aligned way
    errors = d[len(r)][len(h)]
    raw_result = float(errors) / len(r)
    float_result = raw_result * 100
    result = str("%.2f" % float_result) + "%"
    alignedPrint(list, r, h, result, tag)
    return float_result, errors

def totalErrorRate(r, h, tag):
    """
    This is a function that calculate the WER or CER in ASR.
    You can use it like this: wer("what is it".split(), "what is".split())
    """
    errors = 0
    tokenCount = 0
    for i in range(len(r)):
        if tag == "wer":
            ref = r[i].split()
            hyp = h[i].split()
            _, numErrs = singleErrorRate(ref, hyp, tag)
        elif tag == "cer":
            ref = r[i].replace(" ","")
            hyp = h[i].replace(" ","")
            _, numErrs = singleErrorRate(ref, hyp, tag)

        errors = errors + numErrs
        tokenCount = tokenCount + len(ref)

    float_result = float(errors)/tokenCount * 100
    return float_result, errors, tokenCount

if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    hyp = []
    ref = []
    with open(filename1, 'r') as h:
        for line in h:
            hyp.append(line)
    with open(filename2, 'r') as r:
        for line in r:
            ref.append(line)

    print "########## Compute CER ##########"
    cer, err_cer, count_cer = totalErrorRate(ref, hyp, "cer")
    print "########## Compute WER ##########"
    wer, err_wer, count_wer = totalErrorRate(ref, hyp, "wer")
    print "########## Scoring is completed ##########"
    result = str("%.2f" % cer) + "%"
    print "CERs: %s (%d/%d)" % (result, err_cer, count_cer)
    result = str("%.2f" % wer) + "%"
    print "WERs: %s (%d/%d)" % (result, err_wer, count_wer)
