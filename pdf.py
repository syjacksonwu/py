import fitz
import os

def delete_watermark(src, dst, width=963, height=215):
    doc = fitz.open(src)


    for page in range(doc.pageCount):
        images = doc.getPageImageList(page)
        page_content = doc.loadPage(page)      getText("Provided")

        for content in doc[page]._getContents():
            c = doc._getXrefStream(content)
            for _, _, width, height, _, _, _, img, _ in images:
                if width == width and height == height:
                    c = c.replace("/{} Do".format(img).encode(), b"")
            doc._updateStream(content, c)

    dir = os.path.dirname(dst)
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(dir)
    doc.save(dst)

SRC = "D:\\py\\pdf1.pdf"
DST = "D:\\py\\pdf1_out.pdf" 
delete_watermark(SRC, DST)
