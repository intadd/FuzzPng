import zlib
from utils.pngUtil import * 

def Chunk_divide(PngData):
    seek=8
    sig=PngData[:seek]    # Signature, 8 bytes 
    
    chunkLength=None      # Chunk Body Legnth, 4 bytes
    chunkName=None        # Chunk Name, 4 bytes
    chunkBody=None        # Chunk Body, ChunkLength Bytes
    chunkCrc=None         # CRC

    nextChunkName=None
    index=0
    allChunkDict={}
    nowChunkDict={}

    while(chunkName != b'IEND'):
        chunkLength = int.from_bytes(PngData[seek:seek+4],byteorder='big')
        seek=seek+4

        chunkName = PngData[seek:seek+4]
        seek=seek+4

        chunkBody= PngData[seek:seek+chunkLength]
        seek=seek+chunkLength

        chunkCrc= PngData[seek:seek+4]
        seek=seek+4
        
        nowChunkDict["length"] = chunkLength
        nowChunkDict["name"] = chunkName
        nowChunkDict["body"] = chunkBody
        nowChunkDict["crc"] = chunkCrc
        copyDict = nowChunkDict.copy()

        allChunkDict[index]= copyDict
        index+=1
 
    return sig,allChunkDict

def main():
    print(" RUN OK = ) ")

    #targetList= [ "./DummyPng/24_bit.png", "./DummyPng/8_bit.png",  "./DummyPng/4_bit.png",  "./DummyPng/1_bit.png"]
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
