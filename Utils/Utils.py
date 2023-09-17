import os



def encode_str(string,size):
    return string.encode('utf-8')[:size].ljust(size,b'\0')



############# convertir a entero
def conInt0(val:int):
    """RETORNA 0 Ó UN ENTERO"""
    try: return int(val)
    except: return 0
    
def conIntNone(val:int):
    """RETORNA NONE Ó UN ENTERO"""
    try: return int(val)
    except: return None  

def conInt1(val:int):
    """RETORNA -1 Ó UN ENTERO"""
    try: return int(val)
    except: return -1
    







### crea un nuevo archivo
def createFile(fpath):
    """Crea un nuevo archivo si este no existiera"""
    file_name = os.path.basename(fpath)
    try:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        
        fileOpen = open(fpath, "wb") 
        fileOpen.close()  
        print(" Se creo el archivo",file_name,fpath)
        return False
    except Exception as e:
        print(f"e:{e}")
        print(f"Archivo  {file_name} ya existe")
        return True
    

### definir el tamaño de un archivo
def defineSizeUnitFile(file,size:int,unit:str):
    """Recorre el archivo  para llenarlo de bites vacios"""
    buffer = b'\0'*1024
    times_to_write =  size  
    if unit == "b": buffer = b'\0'  ## convertir a bytes
    if unit == "m": times_to_write *= 1024  ## convertir a mega
    print(f"Expected File Size: {len(buffer)*times_to_write} bytes")

    try:
        for i in range(times_to_write):file.write(buffer)
        print("=====Size apply successfully!======")
    except Exception as e: print(f" file utils def definesizeufnit: {e}")


### escribir el desplazamiento del archivo
def Fwrite_displacement(file, displacement:int, obj:object):
    """ESCRIBE EL OBJETO EN EL ARCHIVO BINARIO
        file: archivo actual
        obj: objeto que se escribira"""
    #print("Writing in: ", displacement)
    #print("Size data: ",  obj.getSize())
    data = obj.serialize()
    
    file.seek(displacement)
    file.write(data)



##### leer el desplazamiento del archivo

def Fread_displacement(file,displacement,obj):
    """LEE EL DESPLAZAMIENTO Y OBTIENE EL OBJETO DESERIALIZADO"""
    try:
        #print("Reading in: ", displacement)
        file.seek(displacement)
        data = file.read(len(obj.serialize()))
        #print("Size data: ",  len(data))
        obj.deserialize(data)
    except Exception as e:
        print(f"Error reading object err: {e}")








### ELIMINAR ARCHIVO BINARIO
def remove_disk(file_path):
    Q = f"Desea remover el archivo {file_path} presione 's' o 'S': "
    if os.path.exists(file_path):
        if printWarning(Q):
            os.remove(file_path)
            printConsole2(f'The file {file_path} has been successfully removed.')
        else: printConsole(f"Se cancelo la operacion")
    else: printError(f'The file {file_path} does not exist.')
        
















def get_sizeB(size,unit):
    return size if unit == "b" else (size * 1024 if unit == "k" else size * 1024 * 1024 )



### COMENTARIOS DE SALIDA EN CONSOLA
def printConsole(text): print("\033[36m<<System.Console>> {}\033[00m" .format(text))

def printError(error): print("\033[91m<<Error>> {}\033[00m" .format(error))

def printSuccess(success): print("\033[1;32m<<Success>> {}\033[00m" .format(success))

def printComent(text): print("\033[33m\t\t<<Comentario>> {}\033[00m".format(text))


def printConsole2(text):
    """salida azul fuerte """
    print("\033[94m<<System>> {}\033[00m".format(text))


### mensaje de pregunta
def printWarning(question): 
    confirm = "no"
    confirm = input("\033[35m<<System>> {}\033[00m" .format(question))

    return confirm.lower() == "s"
   