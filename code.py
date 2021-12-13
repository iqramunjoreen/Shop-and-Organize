#a4.py#

"""================================VARIABLES================================"""

commands = ["load", "tell", "infer_all", "complete"]    # TO CHECK VALID COMMAND
data = []   # holds everything from the txt file (head, [body])
lines = []  # holds single lines
KB = []  # holds atoms from tells
inferred = []  # knowledge inferred till now


"""================================INTERPRETER================================"""

# this function checks if command is valid or not
def isValid(command_to_check):
    
    for check in commands: ## load, tell, infer_all
        
        if check in command_to_check:
            return check
        
    return None


# Interpreter Function
def interpreter():

    print("")
    command = input("organize> ")
    if command == "quit":
        exit()
    
    valid = isValid(command)
    
    if valid is not None:
        
        if valid == "load":
            load(command)
            return
        
        elif valid == "tell":
            tell(command)
            return
        
        elif valid == "infer_all":
            global inferred
            inferTemp = infer_all()
            
            for atom in inferTemp:
                KB.append(atom)

            keepGoing = True
            while keepGoing == True:
                
                temp = infer_all()
                
                if len(temp) == 0:
                    keepGoing = False
                else:
                    for atom_ in temp:
                        inferTemp.append(atom_)
                        KB.append(atom_)
            inferred = inferTemp
            printValues()
            return
        
        elif valid == "complete":
            if data[0][0] in inferred:
                print("Your monthly shopping is complete!")
            else:
                print("Your monthly shopping is not complete yet!")
            return
        
    elif valid is None:
        print(f'Error: Unknown Command {command}')
        print("")
        print("Commands: load <filename> --- load the shopping needs of your household")
        print("          tell <atom> --- add item to your home")
        print("          infer_all --- update list to find out how many things you have bought from your list!")
        print("          complete --- find out if your monthly shopping is complete")
        print("")
        return
    

def printInferred():
    print("\t", end="   ")
    for i in range(len(inferred)):
        if i == len(inferred) - 1:
            print(f'{inferred[i]}')
        else:
            print(f'{inferred[i]}', end=", ")
    return


def printKB():
    print("\t", end="   ")
    for i in range(len(KB)):
        if KB[i] not in inferred:
            if i == 0:
                print(f'{KB[i]}', end="")
            else:
                print(f', {KB[i]}', end="")
    print("")
    return


# this function prints values in infer_all() in interpreter function
def printValues():
    print(f'\tNewly added items to your home:')
    if len(inferred) == 0:
        print("\t   <none>")
    else:
        printInferred()

    print(f'\tItems you bought:')
    if len(KB) == 0:
        print("\t   <none>")
    else:
        printKB()



"""==================================LOAD=================================="""

# this function executes the load command
def load(command):
    
    global lines
    fileName = ""
    for i in range(5, len(command)):
        fileName += command[i]

    while True:
        try:
            f = open(fileName, "r")
            lines = f.readlines()
        except FileNotFoundError:
            if fileName == "":
                print("usage: load <filename>")
            else:
                print("ERROR! File " + fileName + " not found!")
            return
        else:
            break

    # remove "\n" from list of lines
    while '\n' in lines:
        lines.remove('\n')

    # remove "\n" from end of each line
    for i in range(len(lines)):
        
        updatedLine = ""
        line = lines[i]
        for j in range(len(line)):
            if line[j] != '\n':
                updatedLine += line[j]

        lines[i] = updatedLine

    if AddAtom():
        
        for line in lines:
            print("\t" + line)
        print(f'\n\t{len(lines)} new rule(s) added')
    else:
        
        print(f'Error! {fileName} is not a valid knowledge base')
        

"""================================ADD ATOM================================"""

# This function checks if the knowledge base is in the correct format
# then it splits all the atom and adds them to the list of data
def AddAtom():
    
    for line in lines:
        
        splitLine = line.split(' <-- ')
        if len(splitLine) != 2:
            return False

        head = splitLine[0]
        splitAtoms = splitLine[1]
        splitAtoms = splitAtoms.split(' & ')

        for atom in splitAtoms:
            if is_atom(atom) is False:
                print("atom is not atom in line :")
                print(line)
                return False

        newData = [head, splitAtoms]  # Create a list of atoms on the line
        data.append(newData)  # Append that list to the existing database

    return True


"""================================VALIDATE ATOM================================"""


# returns True if string s is a valid variable name
def is_atom(s):
    
    if not isinstance(s, str):
        return False
    elif s == "":
        return False
    
    return all(is_letter(x) or x.isdigit() for x in s[1:]) and is_letter(s[0])


def is_letter(x):
    return len(x) == 1 and x.lower() in "_abcdefghijklmnopqrstuvwxyz"


"""==================================TELL=================================="""


def tell(command):  
    atomCommand = ""

    for i in range(5, len(command)):
        atomCommand += command[i]

    if atomCommand == "" or atomCommand == " ":
        print("usage: tell <atom>")
        print("       tell <atom> & <atom> & ...")

    newAtoms = atomCommand.split()  

    if checkTellFormat(newAtoms) == False:
        return
    
    newKB = []  # unckecked atoms
    checked = []  # checked atoms (avoid repetition of print statements)

    for rule in data:
        
        for atom in newAtoms:
            
            if atom in rule[0] or atom in rule[1]: 
                
                if atom in KB:
                    if atom not in newKB and atom not in checked:
                        print(f'\tyou already bought item "{atom}"! ')
                        checked.append(atom)
                else:
                    KB.append(atom)
                    newKB.append(atom)
                    print(f'\t"{atom}" added to KB')
    infer_all() ##added this dec 12, 2021
    if data[0][0] in inferred:
        print("Your monthly shopping is complete!")
            

    return


def checkTellFormat(atoms):

    for atom in atoms:
        if not is_atom(atom):
            print(f'Error! "{atom}" is not a valid item')
            return False

    return True


"""================================INFER_ALL================================"""


def infer_all():
    global inferred
    inferred = []
    for rule in data:
        temp = []
        for atom in rule[1]:
            if rule[0] not in KB and rule[0] not in inferred:
                if atom in KB:
                    temp.append(atom)
        if temp == rule[1]:
            inferred.append(rule[0])

    return inferred



"""================================LET'S PLAY================================"""


# Infinitely running interpreter
def run():
    stop = False
    while stop is False:
        interpreter()


if __name__ == '__main__':
    print("Welcome to your monthly shopping list organizer!")
    print("")
    print("Commands: load <filename> --- load the shopping needs of your household")
    print("          tell <atom> --- add item to your home")
    print("          infer_all --- update list to find out how many things you have bought from your list!")
    print("          complete --- find out if your monthly shopping is complete")
    print("")
    print("Type quit to exit organizer. Enjoy!")
    print("")

    run()


    
