import struct, time

class PdfWriter(object):
    def __init__(self):
        self.version = b'1.4'
        self.producer = 'eBook Maker by Arindam'
        self.header = b'%%PDF-%s\n' % self.version
        self.header += b"%\xe2\xe3\xe4\xe5\n"
        self.pages = []         # list of page ids
        self.offset = len(self.header)
        self.obj_offsets = []   # list of byte offsets

    def begin(self, filename):
        pdf_date = time.strftime("(D:%Y%m%d%H%M%S%z')")
        self.creation_date = pdf_date[:20] + "'" + pdf_date[20:]
        self.stream = open(filename, 'wb')
        self.stream.write(self.header)

    def createPage(self, w=595, h=842, Contents='[]', Resources='<< /ProcSet [/PDF] >>'):
        w, h = int(round(w)), int(round(h))
        page = PdfObj(Type='/Page', MediaBox='[0 0 %d %d]'%(w,h), Parent='3 0 R')
        page['Resources'] = Resources
        page['Contents'] = Contents
        return page

    def addPage(self, page):
        self.addObj(page)
        self.pages.append(page.id)

    def addObj(self, obj, stream=None, id=0):
        if id:
            obj.id = id
            self.obj_offsets.insert(0, self.offset)
        else:
            obj.id = len(self.obj_offsets) + 4
            self.obj_offsets.append(self.offset)

        strng = obj.toString(stream=stream)
        self.stream.write(strng)
        self.offset += len(strng)
        return obj.id   # object identifier

    def finish(self):
        #save catalog, xref table and close file
        pages = PdfObj(Type='/Pages', Count=len(self.pages), Kids=self.pages)
        self.addObj(pages, id=3)
        info = PdfObj(Producer='(%s)'%self.producer, CreationDate=self.creation_date)
        self.addObj(info, id=2)
        catalog = PdfObj(Type='/Catalog', Pages=pages)
        self.addObj(catalog, id=1)
        # Create the xref table
        xref_count = len(self.obj_offsets)+1
        xref = 'xref\n0 %d\n'% xref_count
        xref += '0000000000 65535 f \n'
        for offset in self.obj_offsets:
            xref += '%010d 00000 n \n'% offset
        trailer = PdfDict(Size=xref_count, Root=catalog, Info=info)
        xref += 'trailer\n' + trailer.toString()
        xref += 'startxref\n%d\n'% self.offset
        self.stream.write(xref.encode())
        self.stream.write(b'%%EOF')
        self.stream.close()

class PdfObj(object):
    def __init__(self, **kw):
        self.content = PdfDict()
        self.id = 0
        for key, value in kw.items():
            self.content[key] = value

    def toString(self, stream=None):
        ''' must be called after adding obj to writer otherwise id will be 0'''
        if stream:
            if type(stream) != bytes : stream = stream.encode()
            self.content['Length'] = len(stream)
        strng = '%d 0 obj\n'% self.id + self.content.toString()
        strng = strng.encode()
        if stream:
            strng += b'stream\n' + stream + b'\nendstream\n'
        return strng + b'endobj\n'

    def __setitem__(self, key, value):
        self.content[key] = value

    def __getitem__(self, key):
        return self.content[key]

class PdfDict(dict):
    def toString(self):
        strng = ''
        for key, val in self.items():
            if type(val)==PdfDict:
                strng += '/%s %s'% (key, val.toString())
            elif type(val)==PdfObj:
                strng += '/%s %d 0 R\n'%(key, val.id)
            elif type(val)==list:                   # val is list of Obj id
                strng += '/%s [\n'% key
                for i in val:
                    strng += '%d 0 R\n'% i
                strng += ']\n'
            else:                                   # val is bytes or int
                strng += '/%s %s\n'%(key, str(val))
        strng = '<<\n%s>>\n'% strng
        return strng

def parse_png(rawdata):
    pngidat = b""
    palette = []
    i = 16
    while i < len(rawdata):
        # once we can require Python >= 3.2 we can use int.from_bytes() instead
        n, = struct.unpack(">I", rawdata[i - 8 : i - 4])
        if i + n > len(rawdata):
            raise Exception("invalid png: %d %d %d" % (i, n, len(rawdata)))
        if rawdata[i - 4 : i] == b"IDAT":
            pngidat += rawdata[i : i + n]
        elif rawdata[i - 4 : i] == b"PLTE":
            for j in range(i, i + n, 3):
                # with int.from_bytes() we would not have to prepend extra
                # zeroes
                color, = struct.unpack(">I", b"\x00" + rawdata[j : j + 3])
                palette.append(color)
        i += n
        i += 12
    bitPerComponent = rawdata[24]
    return pngidat, palette, bitPerComponent

def readFile(filename):
    f = open(filename, 'rb')
    data = f.read()
    #f.seek(0,2)
    #size=f.tell()
    f.close()
    return data

# transformation order : translate -> rotate -> scale
def pageMatrix(w, h, rotation):
    rot = rotation%360
    if h > w : w, h = 595.0, 595.0*h/w  # width is 595 pt for smaller side
    else: w, h = 595.0*w/h, 595.0
    trans_dict = {0:'0 0', 90:'0 %.4f'%w, 180:'%.4f %.4f'%(w,h), 270:'%.4f 0'%h}
    rot_dict = {0:'1 0 0 1', 90:'0 -1 1 0', 180:'-1 0 0 -1', 270:'0 1 -1 0'}
    matrix = '%s %s cm\n'%(rot_dict[rot], trans_dict[rot]) # translate and then rotate
    matrix += '%.4f 0 0 %.4f 0 0 cm\n'% (w, h)      # finally scale to page size
    if rot in (90, 270) : w,h = h,w
    return w, h, matrix
