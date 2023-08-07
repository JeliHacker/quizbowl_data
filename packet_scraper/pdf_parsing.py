import re
import pdfplumber


def read_pdf_with_pdfplumber_extract_words_adjusted(file_path, space_threshold=10):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            words = page.extract_words()
            # Initialize the previous word to the first word
            prev_word = words[0]
            for word in words[1:]:
                # Add a space if this word is far enough from the previous word
                if word['x0'] - prev_word['x1'] > space_threshold:
                    text += " "
                text += word['text']
                prev_word = word
            text += "\n"
    return text


# Adjusted PDF text extraction
pdf_text = read_pdf_with_pdfplumber_extract_words_adjusted('/Users/jeligooch/Desktop/git/quizbowl_data/packet_scraper/highschool/2023 PACE NSC/Round 01.pdf')

# Tournament and round number
tournament = 'PACE 2023'
round_number = 'Round 01'

# Split text into question-answer pairs
pairs = re.split(r'\n(?=\d+\.)', pdf_text)

# Initialize list to store parsed data
data = []

# Iterate over pairs and extract questions and answers
for pair in pairs:
    question = re.search(r'(?<=\d\.)[^A]*', pair)
    answer = re.search(r'(?<=ANSWER:)[^\n]*', pair)
    if question and answer:
        data.append({
            'tournament': tournament,
            'round': round_number,
            'question': question.group(0).strip(),
            'answer': answer.group(0).strip()
        })

# Print first few question-answer pairs
for item in data[:5]:
    print(item)
