import zlib
from utils.pngUtil import * 
import os


def main():
    print(" RUN OK = ) ")
    target = "./DummyPng/basi0g01.png"
    target = "./DummyPng/5x5.png"

#    target = "./test1.png"
    try:
        with open(target, "rb") as f:
            PngBytes=f.read()
            print(" Read PNG OK = ) ")
    except Exception as e:
        print(f"ERROR : {e}")
    
    Signature,chunkDict=Chunk_divide(PngBytes)
    IHDR=Read_IHDR(chunkDict.get(0))
    All_Chunk_Viwer(chunkDict)
    decompress(chunkDict)
        

    '''
    print(os.listdir("./DummyPng/"))
    for fileName in os.listdir("./DummyPng"):
        target=os.path.join("./DummyPng",fileName)
        print(target) 
        try:
            with open(target, "rb") as f:
                PngBytes=f.read()
                print(" Read PNG OK = ) ")
        except Exception as e:
            print(f"ERROR : {e}")
        
        Signature,chunkDict=Chunk_divide(PngBytes)
        Read_IHDR(chunkDict.get(0))
        All_Chunk_Viwer(chunkDict)
        decompress(chunkDict)
    '''
main()
