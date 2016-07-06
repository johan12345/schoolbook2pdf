# coding=UTF-8
import os
import sys
import xml.etree.ElementTree as ET

from multiprocessing.pool import Pool


def decrypt_file(filename_in, filename_out, hex_key):
    key = bytearray.fromhex(hex_key)

    with open(filename_in, "rb") as f:
        input = f.read()

    counter = 0
    output = bytearray()
    while counter < len(input) - 4:
        output.append(input[counter + 4] ^ key[counter & 15])
        counter += 1

    with open(filename_out, "wb") as f:
        f.write(output)


def swf_name(i):
    return dirname + "/pages/page_" + str(i) + ".swf"


def decrypted_swf_name(i):
    return dirname + "/pages_decrypted/page_" + str(i) + ".swf"


def pdf_name(i):
    return dirname + "/pages_pdf/page_" + str(i) + ".pdf"


def swf_to_pdf(filename_in, filename_out):
    command = "gfx2gfx {} -r 1200 {}".format(filename_in, filename_out)
    os.system(command)


for dirname in sys.argv[1:]:
    metadata = ET.parse(dirname + "/desc/metadata.xml")
    print(metadata.find("title").text)

    encryptvector = metadata.find("encryptvector").text

    print("decrypting pages")

    counter = 1
    if not os.path.isdir(dirname + "/pages_decrypted"):
        os.mkdir(dirname + "/pages_decrypted")

    p = Pool(8)
    results = []

    while os.path.isfile(swf_name(counter)):
        if not os.path.isfile(decrypted_swf_name(counter)):
            results.append(p.apply_async(decrypt_file, (swf_name(counter), decrypted_swf_name(counter), encryptvector)))
        counter += 1

    for r in results:
        r.get()
    p.close()

    print("converting to pdf")

    counter = 1
    if not os.path.isdir(dirname + "/pages_pdf"):
        os.mkdir(dirname + "/pages_pdf")

    while os.path.isfile(swf_name(counter)):
        if not os.path.isfile(pdf_name(counter)):
            swf_to_pdf(decrypted_swf_name(counter), pdf_name(counter))
        counter += 1

    print("joining pdf")

    command = "pdfunite {} {}".format(dirname + "/pages_pdf/*.pdf", dirname + "/book.pdf")
    os.system(command)