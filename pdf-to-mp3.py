# this script converts pdf files to mp3 in the language of your choice

import os
import glob
import PyPDF2
from googletrans import Translator, LANGUAGES
from gtts import gTTS


def PdfConverter():
    while True:
        
        # Create an mp3 folder if it doesn't exist
        def create_mp3_folder():
            current_dir = os.getcwd()

            mp3_folder_path = os.path.join(current_dir, 'mp3')
            if not os.path.exists(mp3_folder_path):
                os.makedirs(mp3_folder_path)

        # Create a pdf folder if it doesn't exist
        def create_pdf_folder():
            current_dir = os.getcwd()
            
            pdf_folder_path = os.path.join(current_dir, 'pdf')
            if not os.path.exists(pdf_folder_path):
                os.makedirs(pdf_folder_path)

        # Get a list of PDF files in the pdf folder
        def get_pdf_files():
            pdf_files = glob.glob('pdf/*.pdf')
            
            if len(pdf_files) == 0:
                print('No pdf files to convert')
                return None

            # List files
            print('List of PDF files:')
            for i, file_path in enumerate(pdf_files):
                file_name = os.path.basename(file_path)
                print(f'{i+1}. {file_name}')
            
            return pdf_files


        # We get the file that needs to be converted and convert it according to the selected language
        def get_pdf_file_and_convert(pdf_files):
            # Get the number of the file to be converted
            while True:
                file_number = input('Enter PDF file number to convert to MP3 or enter "0" to exit: ')
                try:
                    file_number = int(file_number)
                    if file_number == 0:
                        return None
                    if file_number < 1 or file_number > len(pdf_files):
                        print(f'The number must be from 1 to {len(pdf_files)}')
                    else:
                        return pdf_files[file_number-1]
                except ValueError:
                    print('Enter an integer')

        # Create a pdf folder if it hasn't already been created
        create_pdf_folder()

        # Create an mp3 folder if it hasn't already been created
        create_mp3_folder()

        # Get a list of PDFs
        pdf_files = get_pdf_files()
        if pdf_files is None:
            print("End of the program.")
            exit()

        # Get the number of the file to be converted
        pdf_file_to_convert = get_pdf_file_and_convert(pdf_files)
        if pdf_file_to_convert is None:
            print("End of the program.")
            exit()

        # Getting the playback language
        print('Select playback language: 1. English, 2. Polish, 3. Ukrainian, 4. Keep original.')

        while True:
            language_choice = input('Enter language number: ')
            if language_choice in ['1', '2', '3', '4']:
                break
            print('Incorrect choice. Try again.')
        language_map = {'1': 'en', '2': 'pl', '3': 'uk'}
        language = language_map[language_choice] if language_choice != '4' else None


        # Open PDF file
        pdf_file = open(pdf_file_to_convert, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize the text object
        text = ''
        
        # Iterate through all the pages of the PDF file and get the text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num].extract_text()
            text += page.strip().replace("\n", " ").replace(" ' ", "'")

        # Translate text if needed
        if language:
            translator = Translator()
            translation_text = ''
            for i in range(0, len(text), 5000):
                text_chunk = text[i:i+5000]
                translation = translator.translate(text_chunk, dest=language)
                translation_text += translation.text
            text = translation_text
        # Recognize text and get language code
        elif language == None:
            translator = Translator()
            text_chunk = text[:5000]
            detected = translator.detect(text_chunk)
            lang_code = detected.lang
            language = lang_code
            
        # Synthesizing speech and saving the audio file
        print("The file is being written. Waitin...")
        tts = gTTS(text=text, lang=language, slow=False)
        
        mp3_file_name = os.path.splitext(os.path.basename(pdf_file_to_convert))[0] + '.mp3'
        mp3_file_path = os.path.join('mp3', mp3_file_name)

        tts.save(mp3_file_path)
        print(f'{mp3_file_name} file successfully created in mp3 folder.\n')
        
        # Selection result
        while True:
            try:
                choice_result = int(input('Make a choice: 1. Continue, 2. Exit: '))
                if choice_result == 1:
                    break
                elif choice_result == 2:
                    print("End of the program.")
                    exit()
            except ValueError:
                print("Invalid number entered. Try again.")

        continue


if __name__ == '__main__':
    PdfConverter()