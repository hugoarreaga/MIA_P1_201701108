import sys
import traceback

from Analizador.Analizador import analizarline


from DiskManagment.DiskManagment import command_mkdisk, command_fdisk,command_rmdisk


from Utils.Utils import printConsole,printSuccess,printError

def selectCommnad(command:str,args:dict)-> None:
    """SELECCIONAR COMMANDO RECUPERADO"""

    ####    ADMINISTRACION DE DISCOS BINARIOS
    if command.lower() == "mkdisk":     command_mkdisk(args)
    elif command.lower() == "rmdisk":   command_rmdisk(args)
    elif command.lower() == "fdisk":    command_fdisk(args)
    elif command.lower() == "mount":    pass
    elif command.lower() == "unmount":  pass
    elif command.lower() == "mkfs":     pass
    #####   ADMINISTRACION DE GRUPOS Y USUARIOS
    elif command.lower() == "login":    pass
    elif command.lower() == "logout":   pass
    elif command.lower() == "mkgrp":    pass
    elif command.lower() == "rmgrp":    pass
    elif command.lower() == "mkusr":    pass  
    elif command.lower() == "rmusr":    pass
    ####    Administración de Carpetas Archivos y Permisos
    elif command.lower() == "mkfile":   pass  
    elif command.lower() == "cat":      pass  
    elif command.lower() == "remove":   pass  
    elif command.lower() == "edit":     pass  
    elif command.lower() == "remame":   pass  
    elif command.lower() == "mkdir":    pass  
    elif command.lower() == "copy":     pass  
    elif command.lower() == "move":     pass  
    elif command.lower() == "find":     pass  
    elif command.lower() == "chown":    pass  
    elif command.lower() == "chgrp":    pass  
    elif command.lower() == "chmod":    pass  
    elif command.lower() == "pause":    input("PRESIONE ENTER PARA CONTINUAR...")  
    ####    Pérdida y recuperación del sistema de archivos EXT3
    elif command.lower() == "recovery": pass  
    elif command.lower() == "loss":     pass  
    elif command.lower() == "chmod":    pass  
    else:printError(f"El comando: '{command}' no existe")

### LEER LINEA POR LINEA DEL SCRIPT
def read_script(fpath):
    """LEER LAS LINEAS DEL SCRIPT"""
    printConsole(f"\tLEYENDO COMANDOS DE: {fpath}")
    try:
        with open(fpath, "r") as file:
            for line in file:
                if not line.strip() : continue ## ignore white line
                comm, dargs = analizarline(line.rstrip('\n'))
                if comm is None: continue ### comentario
                selectCommnad(comm,dargs)
        printSuccess("SCRIPT FINALIZADO.....")
    except Exception as e: print(e.args)


if __name__ == "__main__":

    args = sys.argv # <> [] \
    if len(args) < 3 or len(args) > 3: exit()
    if args[1].lower() != "execute": exit()
    try:
        printSuccess("\tIniciando programa:")
        Param, Val = args[2].split("=",1)
        if Val.startswith('"') and Val.endswith('"'): Val = Val[1:-1]
        if Param == "-path": read_script(Val)
    except Exception as e:
        #print("main",e.args,e)
        printError("no se pudo iniciar el script")
        traceback.print_exc()