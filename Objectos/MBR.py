import ctypes
from typing import Any
import struct

import traceback

from Objectos.Partition import Partition
from Utils.Utils import encode_str


def __init__():
    pass
class Mbr(ctypes.Structure):
    _fields_ = [
        ('mbr_tamano', ctypes.c_int),
        ('mbr_fecha_creacion', ctypes.c_char * 19),
        ('mbr_dsk_signature', ctypes.c_int),
        ('dsk_fit',ctypes.c_char),
    ]

    def __init__(self):
        self.mbr_tamano = 0
        self.mbr_fecha_creacion = b'\0'*19
        self.mbr_dsk_signature = 0
        self.dsk_fit = b'\0'
        self.part1 = Partition()
        self.part2 = Partition()
        self.part3 = Partition()
        self.part4 = Partition()

    def const(self) -> str:
        """RETURN: representacion de los datos para convertir a binario MBR"""
        return 'I 19s I 1s'
    
    def setInfo(self,tamano:int,fecha:str,firma:int,fit:str):
        self.mbr_tamano = tamano
        self.mbr_fecha_creacion = encode_str(fecha,19)
        self.mbr_dsk_signature = firma 
        self.dsk_fit = encode_str(fit,1)

    def printInfo(self):
        print(f"     DISCO DE ARCHIVO BINARIO")
        print(f"   DISK SIGN: {self.mbr_dsk_signature}")
        print(f"   DISK FECHA: {self.mbr_fecha_creacion.decode()}")
        for index,part in enumerate([self.part1, self.part2, self.part3, self.part4]):
            print(f"\tParticion: {(index+1)} {'-'*10}",end="")
            print(f"\t   Nombre: {part.part_name.decode()}")
            #print(f"\t   Tipo: {part.part_type.decode()}")
            #print(f"\t   Size: {part.part_s}")
            #part.showInfo()
            
    #######################
    #######################
    #######################


    def getSize(self):
        """Retorna en bites la cantidad total que utiliza la clase Mbr()"""
        return struct.calcsize(self.const()+self.part1.const()*4)


    ## 
    def existsName(self,name:str):
        """Retorna un valor boleano si el nombre ya existe en las particiones"""
        print(f"Exist la particion {name} ?")
        for part in [self.part1, self.part2, self.part3, self.part4]:
            if part.part_name.decode() == name:
                print(F" LA PARTICION {part.part_name} YA EXISTE")
                return True
        print(f"La particion {name} no existe.")
        return False
    
    ## regresa una particion vacia
    def getEmpty(self):
        """Regesa la primera particion vacia que encuentre"""
        for part in [self.part1, self.part2, self.part3, self.part4]:
            if part.part_s == -1:
                return part
        return None
    
    def getPartitionsInfo(self):
        """IMPRIME LA INFORMACION DE LAS PARTICIONES"""
        for part in [self.part1, self.part2, self.part3, self.part4]:
            part.showInfo()


    def getMaxSize(self,Pindex): # <> [] \
        """retorna el bit maximo que puede tener la particionN"""
        maxSize = -1
        for index,part in enumerate([self.part1, self.part2, self.part3, self.part4]):
            if index > Pindex: 
                if part.part_start == -1:
                    maxSize = part.part_start
                else:
                    return maxSize
        return maxSize
    
    def getMinSize(self,Pindex): # <> [] \
        parts =[self.part4, self.part3, self.part2, self.part1]
        if Pindex == 0:
            return len(self.serialize())

        maxSize = len(self.serialize())

        if Pindex == 1: ## part2
            if parts[0].part_s == -1:
                return maxSize
            pass


        for index,part in enumerate(parts):
            if index < Pindex: 
                if part.part_start == -1:
                    maxSize = part.part_start
                else:
                    return maxSize
        return maxSize

    def createPartition(self,tempPart:Partition):
        """CREAR UNA NUEVA PARTICION VERIFICAR SI ES POSIBLE"""
        #if self.part1.part_status ==



        start = len(self.serialize())
        num = 0
        try:
            for index,part in enumerate([self.part1, self.part2, self.part3, self.part4]):
                print(f" size: -{part.part_s}- == -{-1}-")
                if part.part_s == -1 : 
                    print("Se encontro particion vacia")
                    #part = tempPart
                    part.part_status =  tempPart.part_status   
                    part.part_type =    tempPart.part_type   
                    part.part_fit =     tempPart.part_fit     
                    part.part_start =   tempPart.part_start
                    part.part_s =       tempPart.part_s
                    part.part_name =    tempPart.part_name 
                    return
        except Exception as e:
            traceback.print_exc()


    def existExtended(self):
        print("extended exist")
        for part in [self.part1, self.part2, self.part3, self.part4]:
            print(f" type: -{part.part_type.decode()}- == e")
            if part.part_type.decode() == "e":return True
        return False
    
    def existName(self,newname):
        print("exist name")
        for part in [self.part1, self.part2, self.part3, self.part4]:
            print(f" name: {part.part_name.decode()} == {newname}")
            if part.part_name.decode() == newname:return True
        return False

    
    #####################
    def serialize(self) -> bytes:
        """convertir a data"""
        base = struct.pack(
            self.const(),
            self.mbr_tamano,
            self.mbr_fecha_creacion,
            self.mbr_dsk_signature,
            self.dsk_fit 
        )
        for part in [self.part1, self.part2, self.part3, self.part4]:
            base += part.serialize()
        return base 
    

    def deserialize(self,data:bytes):
        """deserializar datos {se pueden imprimimr}"""
        sizeMbr  = struct.calcsize(self.const()) ## size mbr sin particiones
        sizePart = struct.calcsize(self.part1.const()) ## size part1
        
        dataMbr  = data[:sizeMbr]  ### binarios de la parte del mbr sin part
        (self.mbr_tamano,
         self.mbr_fecha_creacion,
         self.mbr_dsk_signature,
         self.dsk_fit) = struct.unpack(self.const(), dataMbr) # desp datos mbr

        ## deserializar los datos de la particion
        particiones = [self.part1, self.part2, self.part3, self.part4]

        for index,part in enumerate(particiones):
            indexI = sizeMbr + (index*sizePart)  ## int donde inicia la particion
            indexF = sizeMbr + ((index+1)*sizePart) ## int  donde finaliza
            dataPart = data[indexI : indexF] ## obtener rango de bits
            part = Partition()
            part.deserialize(dataPart)  ## deserializar bits de la particion 


    def createCopy(self):

        return Mbr(self)