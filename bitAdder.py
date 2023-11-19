#Author: Vasile-Alexandru Ciulea
#Python minimum version 3.x

def AND(a,b):
    return a & b

def OR(a,b):
    return a | b

def XOR(a,b):
    return a ^ b

#Converts a number to a string representation in binary
def binary(x):
    #Applies a bit mask to extract the first 8 bits of the number
    x = x & 255

    #Removes the '0b' prefix
    s = bin(x)[2:]

    #Fill empty spaces with '0' to get correct string representation (8 characters)
    s = s.zfill(8) 
    
    return s

    
#Converts a 8-bit binary string to a python integer (24 bits) taking into account if it's signed or unsigned
def integer(s, signed):
    #Remove any white space
    s= s.replace(" ", "")
    
    if(len(s) != 8):
        raise Exception("Invalid format! Expected exactly 8 bits, got %d" % len(s))

    x = int(s,2)

    #If the sequence is signed and negative the fianl value becomes negative too 
    if(s[0] == "1" and signed):
        x = ((~0)<<8) | x 

    return x

#Reads and validates number. Accepts only 8-bit numbers
def readInput(prompt, signed):
    while True:
        inp = input(prompt)
        x = 0

        try:
            #Handles numbers entered as a binary string
            if(inp[0] == 'b'):
                x = integer(inp[1:len(inp)], signed)
                
            #Handles regular numbers (base 10, string of digits)
            else:
                x = int(inp)
        except Exception as e:
            print("\nInvalid input!")
            print(e)    #Prints the error that occured
            print("\n")
            continue    #Skips the rest of the code and resets the loop
        
        if(signed and (x >= -128 and x <= 127)):
            return x
        elif(not signed and (x >= 0 and x <= 255)):
            return x
        else:
            print("%d\tis not a valid number.(Number is out of %s range)" % (x, "[-128,127]" if signed else "[0,255]"))


#This is concerned with only 1 bit
#Ax - bit value from 1st number
#Bx - bit value from 2nd number
def bitAdder(Ax,Bx, carryIn):
    xor1 = XOR(Ax, Bx)
    and1 = AND(Ax, Bx)
    and2 = AND(xor1, carryIn)

    bitSum = XOR(xor1, carryIn)
    carryOut = OR(and1,and2)

    return (bitSum, carryOut)

#A - the first number
#B - the second number
def signedAddition(A,B):
    S = 0
    carry = 0
    bit = 0
    c6 = 0
    
    for i in range(0,8):
        bit, carry = bitAdder((A>>i)&1, (B>>i)&1, carry)
        bit = bit << i
        S = (S | bit)

        #Carry out from 6th bit
        if(i == 6):
            c6 = carry

    #Enforcing the correct sign across all python integer's 24 bits
    S = S | ((~0^255) * ((S>>7)&1) )

    #'carry' is the carry out from 7th bit
    overflow = XOR(carry,c6)

    #Check for overflow
    if(overflow):
        #x = (((~0)*(1-(S>>7)&1))<<7) | (S&127)

        print("")
        print("Overflow!")
        print("Carry bit 7: %d  Carry bit 6: %d" %(carry,c6))

    return S

#A - the first number
#B - the second number
def unsignedAddition(A,B):
    S = 0
    carry = 0
    bit = 0

    for i in range(0,8):
        bit, carry = bitAdder((A>>i)&1, (B>>i)&1, carry)
        bit = bit << i
        S = (S | bit)

    #Check for overflow
    if(carry):
        print("Overflow")

    return S

#op1 - first number of the addition (operator 1)
#op2 - second number of the addition (operator 2)
#res - the result (sum)
def printResult(op1,op2,res):
    print(" ")
    
    #Output results
    print("%s+\t(%d)" % (binary(op1), op1 ))
    print("%s \t(%d)" % (binary(op2), op2 ))
    print("--------")
    print("%s \t(%d)" % (binary(res), res ))

    print(" ")    

#Displays an options list numbered from 1 to list size
#response is returned in range 0 to list size
def optionListPrompt(msg,arrOptions):

    listSize = len(arrOptions)
    
    while True:
        #Display list header
        print(msg)
        
        #Display numbered option list
        for i in range(0,listSize):
            print("(%d)%s" % (i+1, arrOptions[i]))

        response = 0
        try:
            response = int(input())
        except:
            print("You must enter the number that corresponds to the option you wish to select.")
            response = 0

        if(response >0 and response <= listSize):
            return (response-1)

#Displays a question to which the user must respond with (Y)es or (N)o
def yesNoPrompt(msg):
    while True:
        #Display message
        print("%s(Y/N)" % msg)

        #Read input
        response = str(input()) #not supported in python above 2.7

        #Case does not matter every letter will be converted to uppercase for uniformity
        response = response.upper()

        #Check if response is a valid one
        if(response == "Y"):
            return True
        elif(response == "N"):
            return False
        else:
            print("Response invalid! Type 'Y' for YES or 'N' for NO.")


#Main function
def main():
    A = 0
    B = 0
    isSigned = False
    
    stop = False

    while not stop:

        additionType = optionListPrompt("Select one of the options below", [ "Add 2 signed numbers   (positive and negative numbers)","Add 2 unsigned numbers (positive numbers only)"])
        if(additionType):
            isSigned = False
        else:
            isSigned = True
        
        print("") #For aesthethics, leave an empty line

        #Reading input
        print("If you wish to enter a number in binary, add the prefix 'b' to it. Example 'b0000 0101' (5)")
        A = readInput("A = ",isSigned)
        B = readInput("B = ",isSigned)
        
        if(isSigned):
            S = signedAddition(A,B)
        else:
            S = unsignedAddition(A,B)
         
        #Printing results
        printResult(A,B,S)

        stop = not yesNoPrompt("Do you wish to continue?")
        
        S = 0

#This part of the code triggers the main function when this file is run            
if __name__ == '__main__':
    main() 
