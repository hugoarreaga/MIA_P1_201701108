import struct
import traceback

import sys

import datetime
import random
import os


from Objectos.MBR import Mbr
from Objectos.Partition import Partition

from Utils.Utils import Fwrite_displacement,Fread_displacement,remove_disk

from Utils.Utils import printError,printConsole2,printSuccess

from Utils.Utils import encode_str
#sys.path.append("../Utils")

#sys.path.append("../Objectos")
#from Objectos.MBR import Mbr
#from Objectos.Partition import Partition
from Utils.Utils import conInt0,createFile,defineSizeUnitFile,conIntNone



class test:
    def __init__(self) -> None:
        self.id = 0
        self.edad = 0

    def update(self):
        self.id = 23
        self.edad = 19

    def info(self):
        print(f" id: {self.id}")
        print(f" edad: {self.edad}")

##############################################################################################################
########################################## crear particion ###################################################
##############################################################################################################
##############################################################################################################
def create_partition_logic():

    pass




### falta validar si es particion logica
def create_partition(size:int,fpath:str,name:str,unit:chr,ttype:chr,fit:chr):# PATH,NAME,UNIT,  TYPE,FIT
    printConsole2(f"size {size}, path {fpath}, name {name}, unit {unit}, type {ttype}, fit {fit}")
    
    
    try:

        tempmbr = Mbr() # objeto MBR
        tempfile = open(fpath,"r+b") 
        Fread_displacement(tempfile,0,tempmbr) ## guardar los datos a tempmbr
        
        if ttype == "l": 
            if tempmbr.existExtended(): create_partition_logic()
            
        if ttype == "e":    
            if tempmbr.existExtended():
                printError(f"El archivo ya posee una particion extendida")
                return
        # nombre repetido
        if tempmbr.existsName(name):
            printError(f"Ya existe una particion con el nombre {name}")
            return
        

        start = len(Mbr().serialize())### tamaño del mbr
        temp_part = Partition()          ### crear particion temporal
        temp_part.setInfo("0",ttype,fit,start,size,name)

        print("          DATOS RECUPERADOS","*"*25)
        tempmbr.printInfo()
        #tempfile.close()

        tempmbr.createPartition(temp_part) ### agregar tempPart a MBR
        print("          DATOS EDITADOS","*"*25)
        tempmbr.printInfo()

        Fwrite_displacement(tempfile,0,tempmbr) ## sobreEscribir
        tempfile.close()


        print(f"         DATOS 'GUARDADOS' EN EL ARCHIVO","*"*25)
        tempfile1 = open(fpath,"r+b") 
        tempmbr1 = Mbr() # objeto MBR
        Fread_displacement(tempfile1,0,tempmbr1) ## guardar los datos a tempmbr
        tempmbr1.printInfo()





        


        
    except FileNotFoundError: printError(f"El disco '{fpath}' no existe")
    except Exception as e: traceback.print_exc()

    print("fin fdisk")


def delete_partition(*args):
    print("delete partition")

def add_partition(*args):
    print("add partition size")

### COMANDO INICIAL
def command_fdisk(args):
    SIZE = 0    #OBLIGATORIO
    PATH = ""   #OBLIGATORIO
    NAME = ""   #OBLIGATORIO
    UNIT = "k"  # OPC
    TYPE = "p"  # OPC
    FIT = "w"   # OPC
    DELETE = "full"
    ADD = 0
    ## asignar opcion de fdisk encontrada
    add_delete = False
    add_size = False
    add_moresize = False
    ## validar solamente la primera
    add_option = False
    try: 
        for key,value in args.items():

            ### validar si se selecciona la opcion de crear particion
            if   key.lower() == "size": 
                SIZE = value
                if add_option is False:
                    add_option = True
                    add_size = True

            elif key.lower() == "path": PATH = value
            elif key.lower() == "name": NAME = value
            elif key.lower() == "unit": UNIT = value.lower()

            elif key.lower() == "type": TYPE = value.lower()
            elif key.lower() == "fit": FIT = value[0].lower()


            elif key.lower() == "delete": 
                DELETE = value.lower()
                if add_option is False:
                    add_option = True
                    add_delete = True
            elif key.lower() == "add": 
                ADD = value.lower()
                if add_option is False:
                    add_option = True
                    add_moresize = True
            else: printError(f"**Argumento erroneo '{key}'")

        ## VALIDAR DATOS RECUPERADOS/ALTERADOS
        RSIZE , RDELETE,RADD= 0,"full",0
        if conInt0(SIZE) and add_size < 1: printError(f"WRONG SIZE {SIZE}")
            ##RSIZE = False
        elif PATH == "" or not PATH.endswith(".dsk"):printError(f"WRONG PATH {PATH} ")
        elif NAME == "": printError(f"EMPTY NAME {NAME}")    
        elif UNIT not in ["k","m","b"]: printError(f"WRONG UNIT {UNIT}")
        elif TYPE not in ["p","e","l"]: printError(f"WRONG TYPE {TYPE}")
        elif FIT not in ["f","b","w"]: printError(f"WRONG FIT {FIT}")


        elif DELETE != "full": printError(f"WRONG DELETE VALUE {DELETE}")    ## name y path
        elif conIntNone(ADD) is None: printError(f"WRONG ADD VALUE {ADD}")       ## name y path


        else: 
            if add_size: create_partition(conInt0(SIZE), PATH,NAME,UNIT,  TYPE,FIT)
            if add_delete: delete_partition(PATH,NAME,DELETE)
            if add_moresize: add_partition(PATH,NAME,conIntNone(ADD))
            #print("else")
    except: traceback.print_exc()




##############################################################################################################
#################################### crear archivo binario ###################################################
##############################################################################################################
##############################################################################################################

### crear archivo binario
def create_disk(size:int,unit:chr,fpath:str,fit:chr):
    print("*"*15,"CREANDO DISCO","*"*20)
    if createFile(fpath): return
    cfile = open(fpath,"rb+")
    defineSizeUnitFile(cfile,size,unit)


    currDate = str(datetime.datetime.now())
    sign  = random.randrange(100000)
    cMbr = Mbr()
    cMbr.setInfo(size,currDate,sign,fit)
    cMbr.serialize()
    
    Fwrite_displacement(cfile,0,cMbr)
    cfile.close()


def command_mkdisk(args:dict):
    SIZE, UNIT, PATH,FIT = 0, "k", "","f"
    try: 
        for key,value in args.items():
            if   key.lower() == "size": SIZE = value
            elif key.lower() == "unit": UNIT = value.lower()
            elif key.lower() == "fit": FIT = value.lower()
            elif key.lower() == "path": PATH = value
            else: print(f"**Argumento erroneo '{key}'")
        ## validar datos
        if conInt0(SIZE) < 1: print(f"WRONG SIZE {SIZE}")
        elif PATH == "": print(f"EMPTY PATH {PATH}")
        elif not PATH.endswith(".dsk") : print(f"WRONG FILE TYPE {PATH} '.dsk' expected")
        elif UNIT not in ["k","m","b"]: print(f"WRONG UNIT {UNIT}")
        elif FIT not in ["f","b","w"]: print(f"WRONG FIT {FIT}")
        else: create_disk(conInt0(SIZE),UNIT,PATH,FIT)
    except: print(traceback.print_exc())


##############################################################################################################
#################################### eliminar archivo binario ###################################################
##############################################################################################################
##############################################################################################################


def command_rmdisk(args: dict):
    PATH = ""
    try:
        for key,value in args.items(): 
            if key.lower() == "path": PATH = value
    except Exception as e: printError(e)
    if PATH != "": remove_disk(PATH)

    

if __name__ == "__main__":
    dic = {'path   ': 'dasf-.dsk'}