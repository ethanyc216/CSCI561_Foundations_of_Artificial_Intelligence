#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 3       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
##     Nov. 18th 2019     ##
############################

# input: input.txt
# output: output.txt

import argparse 
import copy
import KnowledgeBase
#import time


def processInput(fileName): 
    # N = NUMBER OF QUERIES 
    # QUERY
    # K = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE
    # SENTENCE
    with open(fileName) as f: 
        lines = f.read().splitlines() 

    queryNum = int(lines[0])
    sentenceNum = int(lines[queryNum + 1])
    queries = lines[1:queryNum + 1]
    sentences = lines[queryNum + 2:queryNum + sentenceNum + 2]

    return queries, sentences


def compareAnswers(outputFile, answersFile):
    res = True
    with open(answersFile) as f:
        answers = f.read().splitlines()
    with open(outputFile) as f:
        outputs = f.read().splitlines()
    if len(answers) != len(outputs):
        res = False
    i = 0
    for answer, output in zip(answers, outputs):
        if not answer == output:
            print 'The answer vs output:\n {} {} {}'.format(i, answer, output)
            res = False
        i += 1
    print res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt',
                        help='input file name')

    parser.add_argument('--output', type=str, default='output.txt',
                        help='output file name')

    parser.add_argument('--answers', type=str, default='output.txt',
                        help='answers file name')
    args = parser.parse_args()

    queries, sentences = processInput(args.input)
    
    knowledgeBase = KnowledgeBase.KnowledgeBase()
    knowledgeBase.tell(sentences)
    #print knowledgeBase.positives
    #print knowledgeBase.negatives
    #print knowledgeBase.sentences
    #print knowledgeBase.predicates
    
    results = []
    for i, query in enumerate(queries):
        knowledgeBaseQ = copy.deepcopy(knowledgeBase)
        result = knowledgeBaseQ.ask(query)
        results.append(result)
        #print result, i

    with open(args.output, 'w') as f:
        f.write(str(results[0]))
        for i in range(1, len(queries)):
            f.write('\n' + results[i])
        f.close()
    
    # compare answers
    #compareAnswers(args.output, args.answers)
