## analizar args
import re
from Utils.Utils import printComent,printError,printConsole


## export this
def analizarline(line:str)-> (str,dict):
    ## COMENTARIOS
   
    if re.match(r'^\s*#', line):
        print("")
        printComent(line)
        return None, None
    
    result = re.split(r'\s+-', line)
    command, args = "",""
    command = result[0].strip()
    try: args = result[1:]
    except Exception as e:print("no hay suficientes argumentos", e)

    if command.isspace(): command = ""
    dicArgs = analizarargs(command,args)
    return command, dicArgs



def analizarargs(command:str,args:dict):
    argum = {}
    key ,value= None,None
    printConsole(f"\tCURRENT COMMAND ''{command.upper()}''")
    
    for arg in args:
        arg = arg.strip() ## eliminar espacios al final de args
        try:
            temp = arg.split("=",1)
            key = temp[0].strip()
            value = temp[1].strip()
            if value =="" or key == "":
                printError(f" **Argumento '{arg}' no posee el formato adecuado")
                continue
            argum.setdefault(key,value.strip('"'))
        except:printError(f" **Argumento '{key.upper()}' incompleto;")
    
    #print(argum)
    return argum


if __name__ == "__main__":

    analizarline('mddi -dfaf=dsdfsa -dsana="fd.dfasadfadfsjn  -dsana="fdsjn"')
    analizarline("adfs")
    analizarline("   adfsdfs -fdsaadfs -adfs=     ")
    analizarline("#comentario            ")
    analizarline("#comentario            ")
    analizarline("pause -=dfsa   -dfsa=  -dfs   =   dasf-     ")
    