import zipfile, re
z = zipfile.ZipFile('Barrobot_Manual.pptx')
names = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)], key=lambda x: int(re.search(r'\d+', x.split('/')[-1]).group()))
allcolors = {}
with open('slides_text.txt', 'w', encoding='utf-8') as out:
    for n in names:
        xml = z.read(n).decode('utf-8')
        texts = re.findall(r'<a:t>(.*?)</a:t>', xml, re.S)
        colors = re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', xml)
        for c in colors:
            allcolors[c] = allcolors.get(c,0)+1
        out.write(f"=== {n} ===\n")
        out.write(" | ".join(t for t in texts if t.strip()))
        out.write("\n\n")
print("wrote slides_text.txt")
print("COLORS USED (hex: count):")
for c,ct in sorted(allcolors.items(), key=lambda x:-x[1]):
    print(f"#{c}  x{ct}")
