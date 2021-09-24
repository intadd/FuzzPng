import zlib
from utils.pngUtil import * 

def main():
    print(" RUN OK = ) ")
    target = "./DummyPng/test_case1.png" 

    try:
        with open(target, "rb") as f:
            PngBytes=f.read()
            print(" Read PNG OK = ) ")
    except Exception as e:
        print(f"ERROR : {e}")
    
    Signature,chunkDict=Chunk_divide(PngBytes)
    Read_IHDR(chunkDict.get(0))
    All_Chunk_Viwer(chunkDict)

main()
