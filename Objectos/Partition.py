import ctypes
from typing import Any
import struct,traceback


from Utils.Utils import encode_str


class Partition(ctypes.Structure):
    _fields_= [
        ('part_status', ctypes.c_char),
        ('part_type', ctypes.c_char),
        ('part_fit', ctypes.c_char),
        ('part_start', ctypes.c_int),
        ('part_s', ctypes.c_int),
        ('part_name', ctypes.c_char*16)
    ]

    def const(self) -> str: return '1s 1s 1s i i 16s'
    
    def __init__(self):
        self.part_status = b'\0'
        self.part_type =  b'\0'
        self.part_fit = b'\0'
        self.part_start = -1
        self.part_s = -1
        self.part_name = b'\0'*16 

    def setInfo(self,status,type,fit,start,s,name):   
        self.part_status = encode_str(status,1)   
        self.part_type = encode_str(type,1)   
        self.part_fit = encode_str(fit,1)     
        self.part_start = start
        self.part_s = s
        self.part_name = encode_str(name,16)
        
    def showInfo(self):## \ [:size]
        print("\n\t","*"*20)
        print("\t",f"PARTICION NAME: -{self.part_name.decode()}-")
        print("\t",f"TYPE: -{self.part_type.decode()}-")
        print("\t",f"FIT: -{self.part_fit.decode()}-")
        print("\t",f"SIZE: -{self.part_s}-")


    ###################
    ###################
    ###################

    def serialize(self) -> bytes:
        """
        RETURN: byte file de la clase Partition()
            convertida a binario
        """
        return struct.pack(
            self.const(),
            self.part_status,
            self.part_type,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_name
        )


    def deserialize(self,data:bytes):
        """Asigna los valores deserializados al objeto Particion actual"""
        try:
            (self.part_status,
            self.part_type,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_name ) = struct.unpack(self.const(),data)
        except:
            traceback.print_exc()

    def bitSize(self) -> int:
        """RETURN: el tamaño (int) de la clase EPartition()"""
        return struct.calcsize(self.const())






###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

class EPartition (ctypes.Structure):
    _fields_= [
        ('part_status', ctypes.c_char),
        ('part_fit', ctypes.c_char),
        ('part_start', ctypes.c_int),
        ('part_s', ctypes.c_int),
        ('part_next', ctypes.c_int),
        ('part_name', ctypes.c_char*16)
    ]

    def __init__(self):
        self.part_status = b'\0'
        self.part_fit = b'\0'
        self.part_start = -1
        self.part_s = -1
        self.part_next =  -1
        self.part_name = b'\0'*16 


    def const(self): return '1s 1s i i i 16s'
    
    def setInfo(self,status:chr,fit:chr,start:int,s:int,next:int,name:str):
        self.part_status = encode_str(status,1)
        self.part_fit = encode_str(fit,0)
        self.part_start = start
        self.part_s = s
        self.part_next = next
        self.part_name = encode_str(name,16)

    def showInfo(self):## \ [:size]
        print("\n\t","*"*20)
        print("\t",f"EPARTICION NAME: {self.part_name.decode()}")
        print("\t",f"FIT: {self.part_fit.decode()}")
        print("\t",f"SIZE: {self.part_s}")

    ###################
    ###################
    ###################

    def serialize(self) -> bytes:
        """RETURN: byte file de la clase Epartition() convertida a binario"""
        return struct.pack(
            self.const(),
            self.part_status,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_next,
            self.part_name
        )


    def deserialize(self,data:bytes):
        """Asigna los valores deserializados al objeto EParticion actual"""
        try:
            (self.part_status,
            self.part_fit,
            self.part_start,
            self.part_s,
            self.part_next,
            self.part_name ) = struct.unpack(self.const(),data)
        except:
            traceback.print_exc()

    def bitSize(self) -> int:
        """RETURN: el tamaño (int) de la clase EPartition()"""
        return struct.calcsize(self.const())