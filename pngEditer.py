import zlib
from utils.pngUtil import * 
import os


def main():
    target = "./DummyPng/5x5.png"
    try:
        with open(target, "rb") as f:
            PngBytes=f.read()
            print(" Read PNG OK = ) ")
    except Exception as e:
        print(f"ERROR : {e}")
    
    Signature,chunkDict=Chunk_divide(PngBytes)
    IHDR=Read_IHDR(chunkDict.get(0))
    outputPath='./output/'
    for i in range(0,50):
        newChunkList=[]
        newIdatChunk=newRandomIDAT(IHDR,chunkDict)
        for originChunk in chunkDict.values():
            if(originChunk.get('name') == b"IDAT"):
                newChunkList.append(newIdatChunk)
            else:
                newChunkList.append(originChunk)
        PNG_path= os.path.join(outputPath,f"{i}.png")
        Chunk_combine(newChunkList,PNG_path)

main()
