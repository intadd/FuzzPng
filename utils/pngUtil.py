import zlib
from utils import printUtil
import random

Printer_=printUtil.Printer()

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
        chunkLengthInt = int.from_bytes(PngData[seek:seek+4],byteorder='big')
        chunkLengthByte = PngData[seek:seek+4]
        seek=seek+4

        chunkName = PngData[seek:seek+4]
        seek=seek+4

        chunkBody= PngData[seek:seek+chunkLengthInt]
        seek=seek+chunkLengthInt

        chunkCrc= PngData[seek:seek+4]
        seek=seek+4
        
        nowChunkDict["length"] = chunkLengthByte
        nowChunkDict["name"] = chunkName
        nowChunkDict["body"] = chunkBody
        nowChunkDict["crc"] = chunkCrc
        copyDict = nowChunkDict.copy()

        allChunkDict[index]= copyDict
        index+=1
 
    return sig,allChunkDict

def All_Chunk_Viwer(AllChunkDict):

    Printer_.functionCall("Chunk Summary ") # Summary 
    print(f"\t[*] Count of Chunks : {len(AllChunkDict.keys())}")
    chunkList=AllChunkDict.values()
    chunkCountDict={}
    count=1
    for _ in chunkList:
        name=_.get("name").decode()
        if(chunkCountDict.get(name,False)):
            chunkCountDict[name]=count
        else:
            count=1
            chunkCountDict[name]=count
        count+=1
    print(f"\t[*] Chunks Names : {', '.join(list(dict.fromkeys(chunkCountDict.keys())))}")
    print(f"\t[*] Chunks Count : ",end='')
    for chunkName,count in chunkCountDict.items():
        print(f"{chunkName}:{count}",end=', ')
    print() 

    Printer_.functionCall("Chunk Detail")     # All Chunk Print
    for index,chunk in enumerate (AllChunkDict.values()):
        Printer_.red(f"\t{index}, Chunk Name : {chunk.get('name').decode()}")
        print(f"\t\t[*] Chunk Body Length : {chunk.get('length')}")

        if(int.from_bytes(chunk.get('length'),byteorder='big')>=10):
            print(f"\t\t[*] Chunk Body : {chunk.get('body')[:10]}...")
        else:
            print(f"\t\t[*] Chunk Body : {chunk.get('body')}")

        print(f"\t\t[*] Chunk Crc : {chunk.get('crc')}")

        if (ChunkDesc.get(chunk.get('name').decode()),False):
            print(f"\t\t[*] Description: {ChunkDesc.get(chunk.get('name').decode())}")
        else:
            print("Error Unkown Chunk Name")
        
        if (CRC_Check(chunk.get('name')+chunk.get('body'),chunk.get('crc'))):
            print(f"\t\t[*] CRC Check .. OK ")


def Read_IHDR(ChunkDict):
 
    chunkLength= ChunkDict.get("length")
    IHDR_Signature = ChunkDict.get("name")
    IHDR_Body= ChunkDict.get("body")
    IHDR_Crc = ChunkDict.get("crc")

    if(IHDR_Signature == b"IHDR" or chunkLength == 13):
        Printer_.functionCall("PNG INFO - IHDR Chunk") # Summary 
 
    else:
        return False

    PNG_width= int.from_bytes(IHDR_Body[:4],byteorder='big')
    PNG_height= int.from_bytes(IHDR_Body[4:8],byteorder='big')
    PNG_bit_depth = IHDR_Body[8:9].hex()
    PNG_color_type = int.from_bytes(IHDR_Body[9:10],byteorder='big')
    Compression = IHDR_Body[10:11].hex()
    Filter = IHDR_Body[11:12].hex()
    Interlace = IHDR_Body[12:13].hex()
    CRC= IHDR_Body[13:]

    print(f"\t[*] Width : {PNG_width}")
    print(f"\t[*] Height : {PNG_height}")
    print(f"\t[*] Bit Depth : {PNG_bit_depth}") 
    print(f"\t[*] Color Type : {PNG_color_type}")
    print("\t[*] \t==> Name :",Color.get(PNG_color_type).get('Name'))
    print("\t[*] \t==> Description :",Color.get(PNG_color_type).get("Description"))
    print(f"\t[*] Compression : {Compression}")
    print(f"\t[*] Filter : {Filter}")
    print(f"\t[*] Interlace : {Interlace}")

    IHDR={}
    IHDR['width']=PNG_width
    IHDR['height']=PNG_height
    IHDR['color']=PNG_color_type
    IHDR['bitDepth']=PNG_bit_depth

    return IHDR 

def make_ChunkDict(Length,Name,Body):
    oneChunk={}
    oneChunk["length"]= Length
    oneChunk["name"] = Type
    oneChunk["body"] = Data
    make_crc= CRC_make(Type+Data)
    oneChunk["crc"] =  make_crc
    return oneChunk

def Chunk_combine(chunkList,path):
    newPNG=b'\x89PNG\r\n\x1a\n' #sig

    for oneChunkDict in chunkList:
        for data in oneChunkDict.values():
            newPNG+=data

    newFile = open(path, "wb")
    newFile.write(newPNG)


def CRC_make(chunkData):
    return zlib.crc32(chunkData).to_bytes(4, byteorder="big")



def CRC_Check(chunkData,CRC):
    if(zlib.crc32(chunkData) == int.from_bytes(CRC,byteorder='big')):
        return True
    else:
        return False

def decompress(chunkDict):
    idatBody=b''
    for oneChunk in chunkDict.values():
        if(oneChunk.get('name') == b'IDAT'): # 각각의 IDAT 청크의 body Concat함
            print(f"IDAT Chunk Bytes Length: {len(oneChunk.get('body'))}")
            idatBody+= oneChunk.get('body') #Concat
    print(len(idatBody))
    ImageData = zlib.decompress(idatBody) # IDAT decompress
    print(f"IDAT Chunk Decompress Bytes Length:{len(ImageData)}")
    print("="*20)
    Printer_.red(f"IDAT Chunks (Compresed) :")
    print(idatBody)
    print("="*20)
    Printer_.yellow(f"Image Raw :")
    print(ImageData)
    print("="*20)
    Printer_.green("Image Raw (int-array):")
    width=5
    height=5
    channel=3
    seek=0
    oneRowBytesLength= channel *(width) +1 # 한줄 당 들어가는 bytes 수 

    png_idat_raw=[ x for x in ImageData ]
    print("== Origin == ")
    for row in range(0, len(png_idat_raw)//oneRowBytesLength):
        print(png_idat_raw[seek:seek+oneRowBytesLength])
        seek+=oneRowBytesLength


def newRandomIDAT(IHDR, allChunkDict):
    width=IHDR.get('width')
    height=IHDR.get("height")
    colorType=IHDR.get("color")
    bitDepth=int(IHDR.get("bitDepth"))

    if(colorType==2):
        channel=3* (bitDepth//8)

    oneRowBytesLength= channel *(width) +1 # 한줄 당 들어가는 bytes 수 

    print("== New == ")
    new_idat_rat=[]
    seek = 0 
    new_idat=[]
    for row in range(0, height):
        oneRow=[]
        for index in range(0,oneRowBytesLength-1): #random 
            oneRow.append(random.randint(0,255))
        oneRow.insert(0,0) # filter 기입
        print(oneRow)
        new_idat_rat.extend(oneRow)

    name=b'IDAT'
    newBody= compress(bytes(bytearray(new_idat_rat)))
    make_crc= CRC_make(name+newBody)

    oneChunk={}
    oneChunk["length"]= len(newBody).to_bytes(4, byteorder="big")
    oneChunk["name"] = b'IDAT'
    oneChunk["body"] = newBody
    oneChunk["crc"] =  make_crc

    return oneChunk




def compress(RawImageData):
    NewCompress =  zlib.compress(RawImageData,-1)

    return NewCompress 


# Color Type in IHDR Chunk Options
Color={
    0: {'AllowDepth':[1,2,4,8,16],'Name':'Grayscale','Description':'Gray Scale'},
    2: {'AllowDepth':[8,16],'Name':'TrueColor','Description':'Only RGB'},
    3: {'AllowDepth':[1,2,4,8],'Name':'Indexed-color','Description':'??'},
    4: {'AllowDepth':[8,16],'Name':'Grayscale+Alpha','Description':'GrayScale+Alpha'},
    6: {'AllowDepth':[8,16],'Name':'TrueColor+Alpha','Description':'RGB+Alpha'},
}
# Chunk Name
ChunkDesc= {
        # Main Chunk
        'IHDR' : '''must be the first chunk; it contains width,height,bit depth, color type,compression method,filter method,interlace method''', 
        'PLTE' : '''contains the palette: a list of colors.''', 
        'IDAT' : '''The IDAT chunk contains the actual image data, which is the output stream of the compression algorithm''',
        'IEND' : '''marks the image end; the data field of the IEND chunk has 0 bytes/is empty''',
        # Sub Chunk 
        'bKGD' : 'Default Background Color',
        'cHRM' : 'Chromaticity coordinates of the display primaries and white point.', 
        'dSIG' : 'For storing digital signatures.',
        'eXIf' : 'Stores Exif metadata',
        'gAMA' : 'Specifies gamma. The gAMA chunk contains only 4 bytes, and its value represents the gamma...',
        'hIST' : 'Can store the histogram, or total amount of each color in the image.',
        'iCCP' : 'ICC color profile.',
        'iTXt' : 'Contains a keyword and UTF-8 text',
        'pHYs' : 'Holds the intended pixel size',
        'sBIT' : '(significant bits) indicates the color-accuracy of the source data',
        'sPLT' : 'Suggests a palette to use if the full range of colors is unavailable.',
        'sRGB' : 'Indicates that the standard sRGB color space is used',
        'sTER' : 'Stereo-image indicator chunk for stereoscopic images',
        'tEXt' : 'Can store text that can be represented in ISO/IEC 8859-1, with one key-value pair for each chunk.',
        'tIME' : 'Stores the time that the image was last changed.',
        'tRNS' : 'Contains transparency information.',
        'zTXt' : 'Contains compressed text',
}

