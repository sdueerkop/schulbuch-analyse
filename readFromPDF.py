#! /usr/bin/python3

################################################
# Program for reading text from a PDF pagewise #
# Using PyPDF2
################################################

import time
import os
import re

import PyPDF2
import argparse

def cli_interface():
    # Use the argparse module so the user can pass a keyword as an argument to
    # the programm on the command line.
    
    # Create a parser object
    cli_parser = argparse.ArgumentParser(description='Open a PDF by filename')
    # Add the argument for the filename
    cli_parser.add_argument('filename', metavar='f', type=str, help='the name of the file to read')
    # Add the argument for the keyword
    cli_parser.add_argument('keyword', metavar='k', type=str, help='the keyword to search for')
    # Parse the arguments and store them in a variable
    args = cli_parser.parse_args()
    # Convert arguments to a dictionary
    dict_of_args = vars(args)
    # Assign the argument given on the command line to the variable
    # filename
    filename = dict_of_args['filename']
    keyword = dict_of_args['keyword']
    return filename, keyword

def process_PDF(filename):
    # Open file in read- and binary mode
    pdfFile = open(filename,'rb')
    
    # Create a pdfReader object
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    
    # Store total number of pages in a variable
    number_of_pages = pdfReader.numPages
    
    # Create an empty dictionary to store the pages in
    dict_of_pages = {}
    
    # Get text from each page
    for p in range(number_of_pages):
        pageObj = pdfReader.getPage(p)
        page_text = pageObj.extractText()
        dict_of_pages[p] = page_text
    #    print('-'*10 + 'Page' + str(p) + '-'*10)
    #    print(page_text)
    
    # Strip each string in the dictionary of extra whitespace
    for i in range(number_of_pages):
        temp_string = dict_of_pages[i]
        new_string = (" ".join(temp_string.split()))
        dict_of_pages[i] = new_string
    
    pdfFile.close()
   # print(dict_of_pages)
    return dict_of_pages

def concordance(string,a_set):
    dict_of_findings = {}
    # Convert string to list
    lst = string.split()
   # print("Liste aus der string:",lst)
   # print("Passende Wörter:",a_set)
    for word in a_set:
        try:
            pos = lst.index(word)
            prv = pos-8
            flw = pos+8
            conc_lst = lst[prv:pos]+lst[pos:flw]
            conc_string = " ".join(conc_lst)
            #print(conc_string)
            dict_of_findings[word] = conc_string
        except ValueError as e:
            print("ValueError: Skipping that word!")
            print(e)
            print()
            continue
    return dict_of_findings

def search(dictionary,keyword):
    n = len(dictionary)
    dict_of_findings = {}
    # The keyword has to be separated from the previous word by whitespace and can have a suffix
    expr = re.compile(r'(\b%s\w*\b)' % keyword, re.I)
    for i in range(n):
        string = dictionary[i]
        # Get only unique values
        re_result = set(expr.findall(string))
        if len(re_result) != 0:
   #         print("\nKeyword found on page ", i)
   #         print(re_result)
            returned_dict = concordance(string,re_result)
            if returned_dict:
                dict_of_findings[str(i)] = returned_dict
            else:
                pass
            #print(dict_of_findings)
        else:
            pass
    lst_of_matching_pages = list(dict_of_findings.keys())
    lst_of_matching_pages = [int(item) for item in lst_of_matching_pages]    
    lst_of_matching_pages.sort()
    return dict_of_findings, lst_of_matching_pages
        


def main():
    print("readFromPDF.py")
    filename, keyword = cli_interface()
    print("Processing pdf...")
    main_dict = process_PDF(filename) 
#    print(main_dict[0])
    search(main_dict,keyword)

if __name__ == "__main__":
    main()
