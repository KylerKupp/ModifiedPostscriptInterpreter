from colors import *
from psexpressions import StringValue, DictionaryValue, CodeArrayValue
# Name: Kyler Kupp
# Collaborators: None

class PSOperators:
    def __init__(self, scoperule):
        #stack variables
        self.scope = scoperule
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        if len(self.dictstack) > 0:
            x = self.dictstack[len(self.dictstack) - 1]
            self.dictstack.pop(len(self.dictstack) - 1)
            return x
        else:
            print("Error: dictPop - Dict stack is empty")

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        if self.dictstack:
            self.dictstack[-1][1].update(d)
        else:
            self.dictstack.append(tuple([0, d]))

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self,name, value):
        if not self.dictstack:
            self.dictstack.append(tuple([0, {}]))
        self.dictstack[-1][1][name] = value 

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        real = "/" + name
        if self.scope == "dynamic":
            for i in range(len(self.dictstack)-1, -1, -1):
                if real in self.dictstack[i][1]:
                    return self.dictstack[i][1][real]
            print("Error: lookup - definition not found")
            return None
        else: #scope = static
            cur = len(self.dictstack) - 1
            while not cur == -1: # will run forever if no return or break
                if real in self.dictstack[cur][1]:
                    return self.dictstack[cur][1][real]
                if self.dictstack[cur][0] == cur: #if staticlink points to itself then we are at index 0 and the variable/function has not been found
                    break
                cur = self.dictstack[cur][0]

    def get_static_link(self, name, index):
        real = "/" + name
        if real in self.dictstack[index][1]:
            return index
        if self.dictstack[index][0] == index: #staticlink points to current index (name not found)
            return -1
        return self.get_static_link(name, self.dictstack[index][0])

    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mod expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of the StringValue objects;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) and isinstance(op2,int))  or isinstance(op1,bool) and isinstance(op2,bool):
                self.opPush(op1 == op2)
            elif isinstance(op1,StringValue) and isinstance(op2,StringValue):
                self.opPush(op1.value == op2.value)
            elif isinstance(op1,DictionaryValue) and isinstance(op2,DictionaryValue):
                self.opPush(op1 == op2)
            else:
                print("Error: eq - operands are not comparable")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: eq expects 2 operands")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) and isinstance(op2,int))  or isinstance(op1,bool) and isinstance(op2,bool):
                self.opPush(op1 > op2)
            elif isinstance(op1,StringValue) and isinstance(op2,StringValue):
                self.opPush(op1.value > op2.value)
            elif isinstance(op1,DictionaryValue) and isinstance(op2,DictionaryValue):
                self.opPush(op1 > op2)
            else:
                print("Error: lt - operands are not comparable")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("lt: lt expects 2 operands")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) and isinstance(op2,int))  or isinstance(op1,bool) and isinstance(op2,bool):
                self.opPush(op1 < op2)
            elif isinstance(op1,StringValue) and isinstance(op2,StringValue):
                self.opPush(op1.value < op2.value)
            elif isinstance(op1,DictionaryValue) and isinstance(op2,DictionaryValue):
                self.opPush(op1 < op2)
            else:
                print("Error: gt - operands are not comparable")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("gt: gt expects 2 operands")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print("===**opstack**===")
        for item in reversed(self.opstack):
            print(item)
        print("===**dictstack**===")
        for i in range(len(self.dictstack)-1, -1, -1):
            print("{---- ", i, " ---- ", self.dictstack[i][0], "----}")
            print(self.dictstack[i][1])
        print("=================")

    """
       Copies the top element in opstack.
    """
    def dup(self):
        self.opPush(self.opstack[-1])

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        self.opstack.count(self)
        num = self.opPop()
        for i in range(len(self.opstack) - num, len(self.opstack)):
            self.opPush(self.opstack[i])

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        while self.opstack:
            self.opPop()
        return
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            self.opPush(op1)
            self.opPush(op2)             
        else:
            print("Error: exch expects 2 operands")

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        num = self.opPop()
        self.opPush(StringValue('(' + '\0'*num + ')'))
    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        self.opPop()
        self.opPush(DictionaryValue({}))

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictionaryValue and StringValue values.
    """
    def length(self):
        value = self.opPop()
        if isinstance(value,StringValue):
            self.opPush(value.length() - 2)
        elif isinstance(value,DictionaryValue):
            self.opPush(value.length())

    """ Pops either:
         -  "A (zero-based) index and an StringValue value" from opstack OR 
         -  "A `name` (i.e., a key) and DictionaryValue value" from opstack.  
        If the argument is a StringValue, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictionaryValue, gets the value for the given `name` from DictionaryValue's dictionary value and pushes it onto the opstack
    """
    def get(self):
        if len(self.opstack) >= 2:
            index = self.opPop()
            item = self.opPop()
            if isinstance(item,StringValue):
                self.opPush(ord(item.value[index+1]))
            elif isinstance(item,DictionaryValue):
                self.opPush(item.value[index])  
            else:
                print("Error: get expects StringValue or DictionaryValue")
        else:
            print("Error: get expects 2 operands")

    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StringValue value from  opstack", OR
    - "An `item`, a `name`, and a DictionaryValue value from  opstack". 
    If the argument is a StringValue, replaces the character at `index` of the StringValue's string with the character having the ASCII value of `item`.
    If the argument is an DictionaryValue, adds (or updates) "name:item" in DictionaryValue's dictionary `value`.
    """
    def put(self):
        if len(self.opstack) >= 3:
            value = self.opPop()
            index = self.opPop()
            item = self.opPop()
            if isinstance(item,StringValue):
                item.value = item.value[0:index + 1] + chr(value) + item.value[index+2:]
            elif isinstance(item,DictionaryValue):
                item.value[index] = value
            else:
                print("Error: put expects StringValue or DictionaryValue")
        else:
            print("Error: put expects 3 operands")

    """
    getinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a `count`, a (zero-based) `index`, and an StringValue value from  opstack, and 
    extracts a substring of length count from the `value` of StringValue starting from `index`,
    pushes the substring back to opstack as a StringValue value. 
    """ 
    def getinterval(self):
        if len(self.opstack) >= 3:
            count = self.opPop()
            index = self.opPop()
            item = self.opPop()
            if isinstance(item,StringValue) and isinstance(index,int) and isinstance(count,int):
                self.opPush(StringValue('(' + item.value[index+1:index+count+1] + ')'))
            else:
                print("Error: getinterval expects StringValue, int, int")
        else:
            print("Error: getinterval expects 3 operands")

    """
    putinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a StringValue value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StringValue's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        if len(self.opstack) >= 3:
            substring = self.opPop()
            index = self.opPop()
            item = self.opPop()
            if isinstance(item,StringValue) and isinstance(index,int) and isinstance(substring,StringValue):
                item.value = item.value[:index+1] + substring.value[1:-1] + item.value[index + len(substring.value) - 1:]
            else:
                print("Error: putinterval expects StringValue, int, StringValue")
        else:
            print("Error: putinterval expects 3 operands")

    """
    search is a string only operator, i.e., works only with StringValue values. 
    Pops two StringValue values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StringValue values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        if len(self.opstack) >= 2:
            delimiter = self.opPop()
            inputstr = self.opPop()
            found = False
            if isinstance(delimiter,StringValue) and isinstance(inputstr,StringValue):
                delraw = delimiter.value[1:-1] # delimiter in form of raw string with no parenthesis
                inraw = inputstr.value[1:-1]   # inputstr in form of raw string with no parenthesis
                for i in range(len(inraw) - len(delraw) + 1):
                    if delraw == inraw[i:i + len(delraw)]:
                        self.opPush(StringValue('(' + inraw[i+len(delraw):] + ')'))
                        self.opPush(delimiter)
                        self.opPush(StringValue('(' + inraw[:i] + ')'))
                        self.opPush(True)
                        found = True
                        break
                if found != True:
                    self.opPush(inputstr)
                    self.opPush(False)
            else:
                print("Error: search expects 2 StringValues")
        else:
            print("Error: search expects 2 operands")

    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictionaryValue value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        if self.opstack:
            item = self.opPop()
            if isinstance(item, DictionaryValue):
                self.dictstack.append(tuple([0, item.value]))
            else:
                print("Error: begin expects dictionary value")
        else:
            print("Error: Def expects 1 operand")

    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        if self.dictstack:
            self.dictPop()
        else:
            print("Error - dictstack is empty")
        
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        if len(self.opstack) >= 2:
            value = self.opPop()
            name = self.opPop()
            if isinstance(name,str):
                self.dictPush({name:value})
            else:
                print("Error: Def expects name to be StringValue")
        else:
            print("Error: Def expects 2 operands")

    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a CodeArrayValue object and a boolean value, if the value is True, executes (applies) the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        code_array = self.opPop()
        val = self.opPop()
        if val:
            code_array.apply(self, len(self.dictstack) - 1)

    """ ifelse operator
        Pops two CodeArrayValue objects and a boolean value, if the value is True, executes (applies) the bottom CodeArrayValue otherwise executes the top CodeArrayValue.
        Will be completed in part-2. 
    """
    def psIfelse(self):
        code_array1 = self.opPop()
        code_array2 = self.opPop()
        val = self.opPop()
        if val:
            code_array2.apply(self, len(self.dictstack) - 1)
        else:
            code_array1.apply(self, len(self.dictstack) - 1)


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a CodeArrayValue object, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the CodeArrayValue. 
       Will be completed in part-2. 
    """ 
    def psFor(self):
        code_array = self.opPop()
        end = self.opPop()
        inc = self.opPop()
        begin = self.opPop()

        top = len(self.dictstack) - 1
        for i in range(begin, end+inc, inc):
            self.opPush(i)
            code_array.apply(self, top)

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()