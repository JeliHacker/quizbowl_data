from PyPDF2 import PdfReader

reader = PdfReader("2022_Pace_NSC/Packet01.pdf")
text = ""
for page in reader.pages:
    text += page.extractText() + "\n"

file = open("packet1.txt", "w")
file.write(text)
file.close()
