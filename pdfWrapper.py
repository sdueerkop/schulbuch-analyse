import os
import glob
import re

import readFromPDF

input_directory = input("Please enter directory to search: ")
homeDir = os.path.expanduser('~')
saveDir = '{}/ConcordanceResults/'.format(homeDir)
filetype = "*.pdf"
search_string = input_directory + filetype

keyword = "Schüler"


def lst_files():
    for filename in glob.iglob(search_string, recursive=True):
        yield filename

def saveResult(filename,keyword,dict_result,page_number):
    filename = re.findall('\w+\.pdf$',filename)
    filename = filename[0]
    output_file = '{}{}_keyword_{}.txt'.format(saveDir,filename,keyword)
    f = open(output_file,'wt', encoding='utf-8')
    f.write(filename+'\n')
    f.write('-' * 30 + '\n\n')
    page_number = set(page_number)
    page_number = list(page_number)
    page_number.sort()
#    print(page_number)
    for n in page_number:
        try:
            #print(n)
            f.write(str(n)+'\n')
            temp_result = dict_result[str(n)]
            #print(temp_result)
            f.write(str(temp_result) +'\n\n')
#            print()
        except KeyError as e:
            print(e)
            print()
#    print(output_file)
#    print(page_number)
    f.close()

def main():
    
    # Check if directory exists, else create
    if os.access(saveDir, os.F_OK):
        print('SETUP CHECK: Saving directory exists')
    else:
        print('SETUP CHECK: Creating directory')
        os.mkdir(saveDir)

    for f in lst_files():
        print("Processing:",f)
        d = readFromPDF.process_PDF(f)
        print("Länge vor search:",len(d))
        try:
            dict_result, page_number = readFromPDF.search(d,keyword)
#            print("Seitenzahl:", page_number)
#            print("Ergebnis:",dict_result)
        except TypeError:
            print("Could not open file. Skipping")
        saveResult(f,keyword,dict_result,page_number)

        


if __name__ == "__main__":
    main()
