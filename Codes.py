from re import split as reSplit
from random import choice as randomChoice
from string import ascii_lowercase as WORDS
ENCRYPTION_KEY_LEN=14
POPULATION_NUM=100
NUM_CROSS_INDEX=3

# Phase 0 #
inpText=open('encoded_text.txt',encoding='utf-8-sig').read()
globalText=open('global_text.txt').read()

inpOrderedWords=reSplit('[^a-zA-Z]+',inpText)
textLen=len(inpOrderedWords)
WordsLenInText=dict()
for i in inpOrderedWords:
    tempLen=len(i)
    if(tempLen not in WordsLenInText.keys()):
        WordsLenInText[len(i)]=1
    else:WordsLenInText[len(i)]+=1

textWordsLen=[WordsLenInText.keys()]


wordsList=reSplit('[^a-zA-Z]+',globalText)
globalDict=dict()
for i in wordsList:
    tempLen=len(i)
    if(tempLen>0):
        if(tempLen not in globalDict.keys()):
            globalDict[len(i)]={i.lower()}
        
        else:globalDict[len(i)].add(i.lower())    
dictKeys=set(globalDict.keys())
            
                
class Decoder():
    
    def __init__(self,globalText,encodedText,ENCRYPTION_KEY_LEN=14) -> None:
        self.globalText=globalText
        self.inpText=encodedText
        self.ENCRYPTION_KEY_LEN=ENCRYPTION_KEY_LEN
        self.initPopulation=self.init_population()
        self.generationLen=0
    # Phase 1 #
    #gene:an alphabet between [a-z]
    #chromosome:permutation from genes with length ENCRYPTION_KEY

    def makeChromosome(self):
        chromo=''.join(randomChoice(WORDS) for i in range(ENCRYPTION_KEY_LEN))
        return chromo

    # Pahse 3 #
    def decryption(self,word:str,tempKey:str,currInd:int):
        ans=str()
        for i in word.lower():
            ans+= WORDS[WORDS.index(i) - WORDS.index(tempKey[currInd])]
            currInd+=1
            currInd %= ENCRYPTION_KEY_LEN
        
        return ans
    
    def calcFitness(self,tempChromo:str):
        numFitWords=0
        currInd=0
        ansInds=set()
        for _word in inpOrderedWords:
            currLen=len(_word)
            decryptionWord=self.decryption(_word,tempChromo,currInd)
            if(decryptionWord in globalDict[currLen]):
                for i in range(currInd,currInd+currLen):ansInds.add(i)
                numFitWords+=1
                
            currInd += currLen
            currInd %= ENCRYPTION_KEY_LEN
        return numFitWords

    # Phase 2 #

    def init_population(self):
        initPopulation=list()
        for i in range(POPULATION_NUM):
            tempChromo=self.makeChromosome()
            initPopulation.append([self.calcFitness(tempChromo),tempChromo])
        return initPopulation
    
    
    # Phase 4#
    def crossOver(self,chromo1:str,chromo2:str,fit1:int,fit2:int):
        indexes=set()
        crossed=NUM_CROSS_INDEX
        tempChromo1,tempFit1=chromo1,fit1
        tempChromo2,tempFit2=chromo2,fit2
        while crossed>0:
            tempIndex=randomChoice(range(0,ENCRYPTION_KEY_LEN))
            if(tempIndex not in indexes):
                tempChromo1=chromo1[:tempIndex]+chromo2[tempIndex]+chromo1[tempIndex+1:]
                tempChromo2=chromo2[:tempIndex]+chromo1[tempIndex]+chromo2[tempIndex+1:]
                crossed-=1
                indexes.add(tempIndex)
        
        tempFit1=self.calcFitness(tempChromo1)    
        tempFit2=self.calcFitness(tempChromo2)    

        return [[tempFit1,tempChromo1],[tempFit2,tempChromo2]]

    def mutate(self,chromo:str,fit:int):
        tempIndex=randomChoice(range(0,ENCRYPTION_KEY_LEN))
        ansFit=fit
        ansChromo=chromo
        for i in WORDS:
            tempChromo=chromo[:tempIndex]+i+chromo[tempIndex+1:]
            tempFit=self.calcFitness(tempChromo)
            if(tempFit>ansFit):
                ansChromo=tempChromo
                ansFit=tempFit
        return [ansFit,ansChromo]
                
    # Phase 5 #
    def decode(self):
        goalNotFound=True
        lastPopulation=self.initPopulation
        while goalNotFound:
            self.generationLen+=1
            lastPopulation=sorted(lastPopulation,reverse=True)
            # print("tempFirstKey:",lastPopulation[0])
            if(lastPopulation[0][0]==textLen):
                key=lastPopulation[0][1]
                print("Key:",key)
                print("generation Length:",self.generationLen)
                ansText=''
                currInd=-1
                for i in self.inpText:
                    if(i.isalpha()):
                        currInd+=1
                        currInd %= ENCRYPTION_KEY_LEN
                        tempChar= WORDS[WORDS.index(i.lower())  - WORDS.index(key[currInd])]
                        if(i.islower()):ansText+=tempChar
                        else:ansText+=tempChar.upper()
                    else:ansText+=i                    
                print(ansText)
                goalNotFound=False
                break
            tempInd=0
            tempPopulation=list()
            while tempInd<POPULATION_NUM:
                if(tempInd<POPULATION_NUM//5):
                    tempPopulation=lastPopulation[:POPULATION_NUM//5]
                    tempInd+=POPULATION_NUM//5
                else:
                    tempIndex1=randomChoice(range(0,POPULATION_NUM))
                    tempIndex2=randomChoice(range(0,POPULATION_NUM))
                    chromo1=lastPopulation[tempIndex1]
                    chromo2=lastPopulation[tempIndex2]
                    ans=self.crossOver(chromo1[1],chromo2[1],chromo1[0],chromo2[0])
                    tempPopulation.append(ans[0])
                    tempPopulation.append(ans[1])
                    tempInd+=2
                if(tempInd>=POPULATION_NUM):
                    for j in range(POPULATION_NUM//10):
                        #2nd way: tempIndex1=j
                        tempIndex1=randomChoice(range(0,POPULATION_NUM))
                        chromo1=lastPopulation[tempIndex1]
                        ans=self.mutate(chromo1[1],chromo1[0])
                        tempPopulation[tempIndex1]=ans
            
            lastPopulation=tempPopulation.copy()
            

                            
                    
d=Decoder(globalText,inpText,ENCRYPTION_KEY_LEN)
d.decode()