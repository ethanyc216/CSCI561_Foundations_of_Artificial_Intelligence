#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 3       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
############################

import re
import copy


operations = set(['&', '|', '=>'])


class KnowledgeBase:

    def __init__(self):
        self.positives = {}
        self.negatives = {}
        self.predicates = set()
        self.sentences = []
        self.checkedSentences = {}

    def getNameAndVariables(self, predicate):
        p = re.search('\s*([~\w\d]+)\((.*)\)', predicate)
        name = p.group(1)
        variables = p.group(2).split(',')
        return name, variables

    def addPredicate(self, predicate, i):
        name, variables = self.getNameAndVariables(predicate)
        if name[0] == '~':
            if (name not in self.predicates):
                self.predicates.add(name)
                self.negatives[name] = []
            self.negatives[name].append(i)
        else:
            if (name not in self.predicates):
                self.predicates.add(name)
                self.positives[name] = []
            self.positives[name].append(i)

    def tell(self, sentences):
        for i, sentence in enumerate(sentences):
            if sentence.find(' => ') > -1:
                premise, conclusion = sentence.split(' => ')
                sentencePart = premise.split()

                newSentence = ''
                for part in sentencePart:
                    if part in operations:
                        newSentence += ' | '
                        continue
                    part = self.neg(part)
                    self.addPredicate(part, i)
                    newSentence += self.standardiseVariables(part, i)
                self.addPredicate(conclusion, i)
                newSentence += ' | '
                newSentence += self.standardiseVariables(conclusion, i)
                self.sentences.append(newSentence)
            
            else:
                self.addPredicate(sentence, i)
                self.sentences.append(self.standardiseVariables(sentence, i))

    def standardiseVariables(self, predicate, index):
        name, variables = self.getNameAndVariables(predicate)
        for i, variable in enumerate(variables):
            if (variable.islower()):
                variables[i] = variable + '_' + str(index)
        return '%s(%s)' % (name, ','.join(variables))

    def neg(self, predicate):
        if predicate[0] == '~':
            return predicate[1:]
        else:
            return '~' + predicate

    def ask(self, query):
        query = self.neg(query)
        self.sentences.append(query)
        self.addPredicate(query, len(self.sentences) - 1)
        if self.resolution(query, self.checkedSentences, 0):
            return 'TRUE'
        else:
            return 'FALSE'

    def findCandidate(self, predicates, resolvedNameNeg):
        candidates = []
        for i, predicate in enumerate(predicates):
            name, variables = self.getNameAndVariables(predicate)
            if name == resolvedNameNeg:
                candidates.append(i)
        return candidates

    def unify(self, predicate1, predicate2):
        unifyDict = {}
        noConst = True
        name1, variables1 = self.getNameAndVariables(predicate1)
        name2, variables2 = self.getNameAndVariables(predicate2)
        if len(variables1) != len(variables2):
            return unifyDict, noConst

        for i, variable1 in enumerate(variables1):
            variable2 = variables2[i]

            if variable1.islower() and (not variable2.islower()):
                if variable1 not in unifyDict:
                    unifyDict[variable1] = variable2
                    noConst = False
                elif unifyDict[variable1] != variable2:
                    return {}, noConst
            elif variable1.islower() and variable2.islower():
                if (variable1 not in unifyDict) and (variable2 not in unifyDict):
                    unifyDict[variable1] = variable2
            elif (not variable1.islower()) and variable2.islower():
                if variable2 not in unifyDict:
                    unifyDict[variable2] = variable1
                    noConst = False
                elif unifyDict[variable2] != variable1:
                    return {}, noConst
            else:
                if variable1 != variable2:
                    return {}, noConst
                else:
                    unifyDict[variable1] = variable2
                    noConst = False
        return unifyDict, noConst

    def noVariables(self, sentenceNum):
        predicates = self.sentences[sentenceNum].split(' | ')
        for predicate in predicates:
            name, variables = self.getNameAndVariables(predicate)
            for variable in variables:
                if (variable.islower()):
                    return False
        return True

    def resolve(self, sentence1, sentence2, resolvedName):
        resolvedNameNeg = self.neg(resolvedName)
        predicates1 = sentence1.split(' | ')
        predicates2 = sentence2.split(' | ')
        candidates1 = self.findCandidate(predicates1, resolvedNameNeg)
        candidates2 = self.findCandidate(predicates2, resolvedName)
        
        #TODO
        findUnify = False
        for i, candidate1 in enumerate(candidates1):
            for j, candidate2 in enumerate(candidates2):
                unifyDict, unifyConst = self.unify(predicates1[candidate1], predicates2[candidate2])
                if unifyDict:
                    findUnify = True
                    done_i = i
                    done_j = j
                    break
            #if findUnify:
            #    break
        if not findUnify:
            return 'RESOLVE FAIL', True

        #TODO
        newSentence = ''
        predicates1.pop(candidates1[done_i])
        predicates2.pop(candidates2[done_j])

        for i, predicate in enumerate(predicates1):
            name, variables = self.getNameAndVariables(predicate)
            for j, variable in enumerate(variables):
                if variable in unifyDict:
                    variables[j] = unifyDict[variable]
            newSentence += '%s(%s) | ' % (name, ','.join(variables))

        for i, predicate in enumerate(predicates2):
            name, variables = self.getNameAndVariables(predicate)
            for j, variable in enumerate(variables):
                if variable in unifyDict:
                    variables[j] = unifyDict[variable]
            newSentence += '%s(%s) | ' % (name, ','.join(variables))

        if newSentence == '':
            return 'FALSE', True
        else:
            predicates = set(newSentence[:-3].split(' | '))
            #predicates = sorted(list(set(newSentence[:-3].split(' | '))))
            predicatesRes = []
            for predicate in predicates:
                if self.neg(predicate) not in predicates:
                    predicatesRes.append(predicate)
            if not predicatesRes:
                return 'RESOLVE FAIL', True
            else:
                predicates = sorted(predicatesRes)
                return ' | '.join(predicates), unifyConst
    
    def resolution(self, query, checkedSentences, depth):
        if depth > 120:
            return False
        #print 'Query is %s' % query
        #localCheckedSentences = copy.deepcopy(checkedSentences)

        # check Unify 
        unifyDict = {}
        predicates = query.split(' | ')
        for predicate in predicates:
            name, variables = self.getNameAndVariables(predicate)
            nameNeg = self.neg(name)
            if name[0] == '~' and nameNeg in self.positives:
                unifyDict[name] = self.positives[nameNeg]
            elif name[0] != '~' and nameNeg in self.negatives:
                unifyDict[name] = self.negatives[nameNeg]
        
        if unifyDict:
            for name in unifyDict:
                for sentenceNum in unifyDict[name]:
                    #print depth, self.sentences[sentenceNum], query
                    newSentence, noConst = self.resolve(self.sentences[sentenceNum], query, name)
                    #print newSentence
                    if (newSentence in self.checkedSentences):
                        if self.checkedSentences[newSentence] >= 15:
                            continue
                    if (newSentence == 'RESOLVE FAIL'):
                        continue
                    if (newSentence == 'FALSE'):
                        return True
                    #if (not noConst):
                    #    if (not self.noVariables(sentenceNum)):
                    #        self.checkedSentences.add(newSentence)
        
                    result = self.resolution(newSentence, self.checkedSentences, depth+1)
                    if (result):
                        #print newSentence, sentenceNum, query
                        return True
                    if newSentence not in self.checkedSentences:
                        self.checkedSentences[newSentence] = 0
                    self.checkedSentences[newSentence] += 1
                    #if (not noConst):
                    #    if (not self.noVariables(sentenceNum)):
                    #        localCheckedSentences.remove(newSentence)
        return False            
        