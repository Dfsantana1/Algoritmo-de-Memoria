from tabulate import tabulate
import numpy as np

class Process:
    def __init__(self, value):
        self.value=value
        self.ForwardPositions=-1
        self.youth=0

    def Set_Value(self, value):
        self.value=value

    def Set_Coin(self, coin):
        self.coin=coin

    def set_Youth(self, youth):
        self.youth=youth

    def get_Youth(self):
        return self.youth

    def set_ForwardPositions(self, ForwardPositions):
        self.ForwardPositions=ForwardPositions

    def get_ForwardPositions(self):
        return self.ForwardPositions

    def get_Value(self):
        return self.value


def displayMenu01():
    print("\t\t Options Menu \n\n")
    print("(1) Optimal algorithm")
    print("(2) FIFO algorithm")
    print("(3) LRU algorithm")
    print("\n\n")

if __name__ =="__main__":

    #program's while
    halt=False
    while not halt:
        #input section
        print("---------------------------------------------------------------------")
        print("\n\n\t\t WELCOME, HERE YOU CAN RUN ALL 3 PAGES-SWAP-ALGORITHMS \n\n")
        rawInput=input("Please write a string of integers separated by commas: ")
        splitedInput=rawInput.split(',')
        intInput = []
        for element in splitedInput:
            try:
                temp=int(element.strip())
                intInput.append(temp)
            except:
                print("error, the input must be integers only")
                halt=True
        if halt:
            break

        keyToken2=False
        framesLength=0
        while not keyToken2:
            try:
                framesLength=int(input("Enter frames length 'x' where [ 3 - 10 ]: "))
                if framesLength > 2 and framesLength <= 10:
                    keyToken2=True
            except:
                print("error, the input must be an integer")

        ExecutionLength=len(intInput)

        keyToken3=False
        swapOption=0
        domain01=[1,2,3]
        while not keyToken3:
            try:
                displayMenu01()
                swapOption=int(input("Enter your choice: "))
                print("\n\n")
                if swapOption in domain01:
                    keyToken3=True
                else:
                    print("error, input out of range, check menu")
            except:
                print("error, the input must be an integer")

        #body section

        #copy of intInput
        intInputCopy01=[]
        for e in intInput:
            intInputCopy01.append(e)

        #I prepare fault list
        faultList=[]
        temp=0
        while (temp < ExecutionLength):
            faultList.append("/")
            temp+=1
        f=0 #initial position (the first singleFrame is coming)

        #I prepare the first frame
        AlreadyStarted=False
        FramesTable=[]
        myCoin=0 #n-side coin

        while len(intInput) > 0:
            singleFrame=[]
            if not AlreadyStarted:
                temp=0
                while temp < framesLength:
                    singleFrame.append("P") #frame structure #pass
                    temp+=1
                AlreadyStarted=True
            else:
                for i in FramesTable[-1]:
                    singleFrame.append(i)

            It_is_present=False
            for element in singleFrame: #if the process is not in frames
                if isinstance(element, Process):
                    if element.get_Value()==intInput[0]:
                        It_is_present=True
                        break
            if not It_is_present:
                faultList[f]="F"
            f+=1


            isThereRoom=False
            pos=0
            for element in singleFrame:
                if element=='P':
                    isThereRoom=True
                    break
                pos+=1

            if isThereRoom and not It_is_present:

                 #spoiler alert
                if swapOption == 3:
                    for process in singleFrame:
                        if isinstance(process, Process):
                            #I increase the ages
                            process.set_Youth(process.get_Youth()+1)

                #here is where the process is born, when it enters to the frame
                singleFrame[pos]=Process(intInput[0])

            elif swapOption == 1 and not It_is_present: #Optimal
                ForwardedList=[]
                found=False
                for process in singleFrame:
                    value=process.get_Value()
                    for number in intInput:
                        if number==value:
                            break
                        process.set_ForwardPositions(process.get_ForwardPositions()+1)
                    if not found: #I punish that process
                        process.set_ForwardPositions(process.get_ForwardPositions()+1)
                    ForwardedList.append(process.get_ForwardPositions())
                for process in singleFrame:
                    process.set_ForwardPositions(-1)

                singleFrame[ForwardedList.index(max(ForwardedList))]=Process(intInput[0])

            elif swapOption == 2 and not It_is_present: #FIFO
                singleFrame[myCoin]=Process(intInput[0])
                if myCoin == framesLength-1:
                    myCoin=0
                else:
                    myCoin+=1

            elif swapOption == 3 and not It_is_present: #LRU
                for process in singleFrame: #I increased the ages
                    process.set_Youth(process.get_Youth()+1)

                ageList=[]
                for process in singleFrame: #I look for the oldest one to replace it
                    ageList.append(process.get_Youth())
                singleFrame[ageList.index(max(ageList))]=Process(intInput[0])

            else:
                #Action no specified (when a process is already in the singleFrame)
                #But, for LRU, we need to rejuvenate it
                #for process in singleFrame: #I increased the ages
                    #process.set_Youth(process.get_Youth()+1)
                if swapOption == 3:
                    for process in singleFrame: #I increased the ages
                        if isinstance(process, Process):
                            process.set_Youth(process.get_Youth()+1)

                    for process in singleFrame:
                        if isinstance(process, Process):
                            if process.get_Value()==intInput[0]:
                                process.set_Youth(0)
                print("", end="")

            FramesTable.append(singleFrame)
            intInput.pop(0)

        #Formatting table of frames THE PROBLEM IS HERE BRO!
        FramesTable_onlyValues = []
        for singleFrame in FramesTable:
            dataFrame = []
            for element in singleFrame:
                if isinstance(element, Process):
                    dataP=element.get_Value()
                    dataFrame.append(dataP)
                else:
                    dataFrame.append(element)
            FramesTable_onlyValues.append(dataFrame)

        transposedMatrix = np.asarray(FramesTable_onlyValues).T.tolist()

        if swapOption == 1:
            print("\n\n\t\t OPTIMAL ALGORITHM \n\n")
        elif swapOption == 2:
            print("\n\n\t\t FIFO ALGORITHM \n\n")
        else:
            print("\n\n\t\t LRU ALGORITHM \n\n")

        for e in intInputCopy01:
            print("  ", e, end="")
        print("")

        print(tabulate(transposedMatrix, tablefmt='fancy_grid'))

        for e in faultList:
            print("  ", e, end="")
        print("\n\n")

        #I check how many faults there are:
        totalFaults=0
        for e in faultList:
            if e == 'F':
                totalFaults+=1


        print("Quantity of Faults: ", totalFaults, "\n\n")
        print("---------------------------------------------------------------------")

        #program's end section
        keyToken=False
        option=""
        while not keyToken:
            option=input("Do you want to run this program again? (y:yes / n:no): ")
            optionL=option.lower()
            if optionL == 'n':
                keyToken=True
                halt=True
            elif optionL == 'y':
                keyToken=True
            else:
                print("no valid input")

    print("\n\n I HOPE THIS PROGRAM HAS BEEN HELPFUL FOR YOU. \n\n")
    print("\n END OF LINE \n\n")
