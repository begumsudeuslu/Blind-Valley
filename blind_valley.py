import sys

"""This function read input txt and return all txt as list in list. 
But input txt has different two types: int and str. So we creat two list for numbers and strings."""
def read_file(file_name):
    input_list=[]          #this is my mean list. Firstly, we put numebrs in it.
    table = []          #this is my str list.
    with open(file_name, 'r') as f:  
        for line in f:
            #First 4 line have int which show count H and B us.
            if len(input_list)<4:
                input_list.append([int(num) for num in line.strip().split(" ")])
            #Other lines tell as direction which have L, R, U, D.
            else:
                table.append([str(item) for item in line.strip().split(" ")])         
    input_list.append(table)        #Merge list.
    return input_list


#This function check the input values of row and column.
"""If inputs are in index, function return True or else return False and dont allow run."""
def is_valid(i,j, list):
    return 0 <= i < len(list) and 0 <= j < len(list[0])


"""This function check the whether the entered letter is the same on the right, left, below and above. If we find same letter, return False.
The function do that for just H and B cause of the rule. If letter is L, return True. """
def control(row, col, plug, current_list):
    if plug == 'H' or plug=='B':        # This function Check H and B not other letter.
        
        for pos_i, pos_j in [(-1, 0), (1, 0), (0, 1), (0,-1)]:       #Check the right, left, below and above.
            contact_number_i = row +  pos_i
            contact_number_j = col +  pos_j
                
            if is_valid(contact_number_i, contact_number_j, current_list):      #If possible index is in the list, keep on.
                if current_list[contact_number_i][contact_number_j]==plug:     #If there is same letter, return False.
                    return False

    return True     


#This function compute how many plugs are in the entered row.
def row_count(row,plug,table):
    count = 0 
    for j in range(0,len(table[0])):
        if table[row][j] == plug:
            count += 1  
    return count        #And return count of how many there are.


#This function compute how many plugs are in the entered column.
def col_count(col,plug,table):  
    count = 0
    for j in range(0,len(table)):
        if table[j][col] == plug:
            count += 1      
    return count      #And return count of how many there are.


"""This function is function and do backtracking.
First of all the function checks to see if we have reached the end of the list.
If we have reached the end, it checks whether the conditions are ture or not.
But if we are not in end of the list (actually we start left most and up most cell (0,0)), we plug H, B and N.
Table is our empty list, file show count H and B us, template tell as direction which have L, R, U, D and also check_solution check if there is no solution. """
def solve(row, col, table,file,template,output_file,check_solution):   
    #Check the number of row. 
    if row == len(table):
        #If all rows and columns are filled, check conditions and write file if necessary.
        flag = True
        
        #Check whether the total H numbers in all rows are equal to the given number.
        for i in range(len(file[0])):
            if file[0][i] != -1 and file[0][i] != row_count(i, 'H', table):     #If condition is -1, dont check the counts.
                flag = False   #If not equal  
                break       
        
        #Check whether the total B numbers in all rows are equal to the given number.    
        for i in range(len(file[1])):
            if file[1][i] != -1 and file[1][i] != row_count(i, 'B', table):     #If condition is -1, dont check the counts.
                flag = False   #If not equal
                break
        
        #Check whether the total H numbers in all cols are equal to the given number.    
        for i in range(len(file[2])):
            if file[2][i] != -1 and file[2][i] != col_count(i, 'H', table):      #If condition is -1, dont check the counts.
                flag = False    #If not equal
                break
            
        #Check whether the total B numbers in all cols are equal to the given number.
        for i in range(len(file[3])):
            if file[3][i] != -1 and file[3][i] != col_count(i, 'B', table):       #If condition is -1, dont check the counts.
                flag = False    #If not equal
                break
        
        #If flag True, write created file.
        if flag:
            #If check_solution changed, we will learn this file is written 
            check_solution[0]+=1
            #Creat file and write.
            with open(output_file,'w') as f:
                for i,line in enumerate(table):
                    f.write(' '.join(line) )
                    if i<len(table)-1:
                        f.write('\n')                
        return
    
    #If it reaches the end of the line, we cotinue from the beginning  of the next line.
    if col == len(table[row]):
        solve(row + 1, 0, table,file,template,output_file,check_solution)
        return

    #If cell is R and D, go to next cell.
    if template[row][col] in ['R', 'D']:
        solve(row, col + 1, table,file,template,output_file,check_solution)
    
    else:
        if template[row][col] == 'L':   
            if control(row, col, 'H', table) and control(row, col + 1, 'B', table):   #Firstly, we try to plug H and B.
                table[row][col] = 'H'
                table[row][col + 1] = 'B'
                solve(row, col + 2, table,file,template, output_file,check_solution)   #And move forward two. 
                table[row][col] = ''            #If there is backtracking, delete previous.
                table[row][col + 1] = ''
            if control(row, col, 'B', table) and control(row, col + 1, 'H', table):    #Secondly, we try to plug B and H.
                table[row][col] = 'B'            #If there is backtracking, delete previous.
                table[row][col + 1] = 'H'
                solve(row, col + 2, table,file,template, output_file,check_solution)   #And move forward two.
                table[row][col] = ''             #If there is backtracking, delete previous.
                table[row][col + 1] = ''
            table[row][col] = 'N'              #If HB and BH not suit, plug N and N.
            table[row][col + 1] = 'N'
            solve(row, col + 2, table,file,template,output_file,check_solution)    #And move forward two.
            table[row][col] = ''                 #If there is backtracking, delete previous.
            table[row][col + 1] = ''
        elif template[row][col] == 'U':
            if control(row, col, 'H', table) and control(row + 1, col, 'B', table):     #Firstly, we try to plug H and B.
                table[row][col] = 'H'
                table[row + 1][col] = 'B'
                solve(row, col + 1, table,file,template,output_file,check_solution)      #And move forward two. 
                table[row][col] = ''             #If there is backtracking, delete previous.
                table[row + 1][col] = ''
            if control(row, col, 'B', table) and control(row + 1, col, 'H', table):     #Secondly, we try to plug B and H.
                table[row][col] = 'B'
                table[row + 1][col] = 'H'
                solve(row, col + 1, table,file,template,output_file,check_solution)     #And move forward two.
                table[row][col] = ''             #If there is backtracking, delete previous.
                table[row + 1][col] = ''
            table[row][col] = 'N'           #If HB and BH not suit, plug N and N.
            table[row + 1][col] = 'N'
            solve(row, col + 1, table,file,template,output_file,check_solution)
            table[row][col] = ''             #If there is backtracking, delete previous.
            table[row + 1][col] = ''

#The main function run all function.
def main():
    input_file=(sys.argv[1])             #Take input from user.
    all_file=read_file(input_file)            #Take input file as list.
    output_file=(sys.argv[2])         #File to write.
    file=all_file[:-1]           #First 4 rows in txt which show count H and B us.
    template=all_file[-1]            #Take other rows in txt which  tell as direction which have L, R, U, D.
    table = [['' for _ in range(0,len(template[0]))] for _ in range(0,len(template))]        #This is empty list which is filled. 
    none_solution=[0]           #This is parameter of check solution.
    solve(0,0,table,file,template,output_file,none_solution)
    if none_solution[0]==0:          #If none_solution doesnt change or file cannot write for any possiblety, write another txt. 
        with open(output_file, 'w') as f:
            f.write("No solution!")   
    
if __name__=='__main__':
    main()