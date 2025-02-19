import json

with open("data.json", 'r') as file:
    data=json.load(file)

# Function to report error
def report_error(line_number, line, expected, received):
    (f"Error in line {line_number}: {line}")
    (f"Expected {expected} tokens, got {received}")

# Function to report invalid register
def report_invalid_register(line_number, line):
    print(f"Error in line {line_number}: {line}")
    print("Invalid register name")
    
# Function to report invalid immediate value
def report_invalid_immediate(line_number, line):
    print(f"Error in line {line_number}: {line}")
    print("Invalid immediate value. Expected integer")

# Function to report invalid range of immediate value
def report_invalid_range(line_number, line, min_val, max_val):
    print(f"Error in line {line_number}: {line}")
    print(f"Invalid value. Expected between {min_val} and {max_val}")
    
# Fundtion to report an undefined label
def report_undefined_label(line_number, line):
    print(f"Error in line {line_number}: {line}")
    print("Undefined label")

def tokenization(line, data, line_number):
    tokens=line.replace(","," ").split()
    opcode=tokens[0]
    instruction_type=data["INSTRUCTION_FORMATS"]
    if opcode in instruction_type["S"]:
        token=[]
        tokens[2]=tokens[2].replace("("," ").replace(")"," ").split()
        for t in tokens:
            if isinstance(t,list):
                for t1 in t:
                    token.append(t1)
            else:
                token.append(t)
        if len(token)!=4:
            print(f"Error in line {line_number}: {line}")
            print(f"Expected 4 tokens, got {len(tokens)} tokens")
            return None
        elif len(token)==4:
            rs2=token[1]
            immediate=token[2]
            rs1=token[3]
            if rs2 not in data["REGISTER_MAP"] or rs1 not in data["REGISTER_MAP"]:
                print(f"Error in line {line_number}: {line}")
                print("Invalid register name")
                return None
            try:
                immediate=int(immediate)
            except ValueError:
                print(f"Error in line {line_number}: {line}")
                print(f"Invalid immediate value. Expected integer")
                return None
            if isinstance(immediate,int):
                if immediate>=-2048 and immediate<=2047:
                    immediate=format(immediate & 0xFFF, "012b")
                    return (immediate[0:7]+data["REGISTER_MAP"][rs2]+data["REGISTER_MAP"][rs1]+data["FUNCT3"][opcode]+immediate[7:12]+data["OPCODES"][opcode])
                else:
                    print(f"Error in line {line_number}: {line}")
                    print(f"Invalid immediate value. Expected value between -2048 and 2047")

    elif opcode in instruction_type["J"]:
        if len(tokens)!=3:
            print(f"Error in line {line_number}: {line}")
            print(f"Expected 3 tokens, got {len(tokens)} tokens")
            return None
        elif len(tokens)==3:
            rd=tokens[1]
            immediate=tokens[2]
            if rd not in data["REGISTER_MAP"]:
                print(f"Error in line {line_number}: {line}")
                print("Invalid register name")
                return None
            try:
                immediate=int(immediate)
            except ValueError:
                print(f"Error in line {line_number}: {line}")
                print(f"Invalid immediate value. Expected integer")
                return None
            if isinstance(immediate,int):
                if immediate>=-1048576 and immediate<=1048575:
                    imm=format(immediate & 0xFFFFFFFF,"032b")
                    return (imm[11]+imm[21:31]+imm[20]+imm[12:20]+data["REGISTER_MAP"][rd]+data["OPCODES"][opcode])
                else:
                    print(f"Error in line {line_number}: {line}")
                    print(f"Invalid immediate value. Expected value between -1048576 and 1048575")
    elif opcode in instruction_type["I"]:
        # Checking if the opcode is load type or not
        if opcode in data["LOAD_OPCODES"]:
            # If tokens != 3 : Report Error
            if len(tokens)!=3:
                report_error(line,line_number,3,len(tokens))
                return None
            # Assing destination register and (immediate) their corresponding values
            rd,offset=tokens[1],tokens[2]
            # Extracting the immediate value and rs1 from the parenthesis
            if "(" in offset and ")" in offset:
                offset,rs1=offset.split("(")
                rs1=rs1.strip(")")
            else:
                # Print Error if no parenthesis 
                print(f"error in line {line_number}: {line.strip()}")
                print(f"Invalid load instruction format. Expected offset(rs1)")
                return None
            # Print Error if any register is invalid
            if rd not in data["REGISTER_MAP"] or rs1 not in data["REGISTER_MAP"]:
                report_invalid_register(line_number, line)
                return None
            try:
                # Checking if the immediate is integer or not
                offset = int(offset)
            # Print Error : if immediate is not integer 
            except ValueError:
                print(f"Error in line {line_number}: {line}")
                print(f"Invalid offset instruction. Expected integer")
                return None
            min=-2048
            max=2047
            # Print Error : if immediate is not within acceptable range
            if not(-2048<=offset<=2047):
                report_invalid_range(line_number,line,min,max)
                return None
            # 2's complement of offset/immediate
            off=format(offset & 0xFFF,"012b")
            return(
                # Returning the 32-bit binary instruction
                off+data["REGISTER_MAP"][rs1]+data["FUNCT3"][opcode]+data["REGISTER_MAP"][rd]+data["LOAD_OPCODES"][opcode]
            )
    
            

instr=input("Enter : ")
print(tokenization(instr,data,4))