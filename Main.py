from Config import Config
#------------------------ Start Function Scope ------------------------#

def executeFeature(c): 
    if(c == 1): # Update Database
        print(c)
        

#------------------------ End Function Scope ------------------------#

menu = """
Press 1 To Update Database,
Press 2 To Send Message To User,
Press 3 To Send Group Message,
Press 0 To Exit Application,
Enter Menu Item: """

c = int(input(menu))
while(c != 0):
    executeFeature(c)
    c = int(input(menu))


