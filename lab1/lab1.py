from docx import Document

def rgb_to_binary(rgb):
    binary_values = [format(component, '08b')[2:] for component in rgb]
    binary_string = ''.join(binary_values)
    return binary_string

def get_binary_color(docx_file):
    listofcolors=[]
    doc = Document(docx_file)
    
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            for char in run.text:
                print(f"Character: {char}")
                print(f"Text Color: {run.font.color.rgb}")
                print(f"Background Color: {run.font.highlight_color}")
                print(f"Font Size: {run.font.size.pt} pt")
                print("-" * 20)
                if run.font.color is not None:
                    rgb = run.font.color.rgb
                    binary_color = rgb_to_binary(rgb)
                listofcolors.append(binary_color)
    print(listofcolors)
    listofcolors = list(map(lambda x: x.replace('000000000000000000', '0'), listofcolors))
    listofcolors = list(map(lambda x: x.replace('000001000001000001', '1'), listofcolors))
    print(listofcolors)
    stringofcolors = ''.join(listofcolors)
    print(stringofcolors)


    binary_chunks = [stringofcolors[i:i+8] for i in range(0, len(stringofcolors), 8)]

    encodings = {
        'cp866': 'cp866',
        'KOI8-R': 'koi8-r',
        'Windows-1251': 'windows-1251',
    }

    decoded_strings = {encoding: "" for encoding in encodings}

    for chunk in binary_chunks:
        chunk_bytes = int(chunk, 2).to_bytes(len(chunk) // 8, byteorder='big')
        
        for encoding_name, encoding in encodings.items():
            decoded_strings[encoding_name] += chunk_bytes.decode(encoding)

    for encoding_name, decoded_string in decoded_strings.items():
        print(f"{encoding_name}: {decoded_string}")



get_binary_color("variant01.docx")