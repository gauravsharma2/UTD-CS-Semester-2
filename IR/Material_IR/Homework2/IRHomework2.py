import glob
import time
import os
import re
import nltk
nltk.download('omw-1.4')
import sys
from datetime import datetime
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from xml.dom import minidom
from porter_stemmer_tartarus import PorterStemmer

lemmas_postings_map = dict()
stems_postings_map = dict()


class Main:
    def _init_(self):
        pass

    def update_token_count_map(self, tokens_list):
        token_freq_map = dict()
        for token in tokens_list:
            if token not in token_freq_map.keys():
                token_freq_map[token] = 1
            else:
                token_freq_map[token] = token_freq_map.get(token) + 1
        return token_freq_map

    def get_max_tf(self, token_count_map):
        sorted_token_count_map = sorted(token_count_map, key=token_count_map.get, reverse=True)
        res = sorted_token_count_map[0]
        max_tf = token_count_map.get(res)
        return max_tf

    def remove_stop_words(self, tokens_list, stop_words):
        filtered_tokens_list = []
        for token in tokens_list:
            if token not in stop_words:
                filtered_tokens_list.append(token)
        return filtered_tokens_list

    def get_tokens(self, document, stop_words):
        split_path = document.split('/')
        docID = split_path[len(split_path) - 1]
        # to get the doc ID (only digits, remove cranfield text)
        docID = int(docID[9:])
        doc = minidom.parse(document)
        text_node = doc.getElementsByTagName("TEXT")
        text_child = text_node[0].firstChild
        text = text_child.nodeValue
        text_list = text.splitlines()

        tokens_per_doc = []

        for text in text_list:
            text = text.lower()
            text_without_punc = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            tokens_list = text_without_punc.split(" ")
            tokens_list_1 = [token for token in tokens_list if token != '' and not token.isnumeric()]

            for l in tokens_list_1:
                tokens_per_doc.append(l)
            doc_len = len(tokens_per_doc)

            filtered_tokens = my_obj.remove_stop_words(tokens_per_doc, stop_words)
        return filtered_tokens, docID, doc_len

    #Lemmatization
    def get_lemmas_posting_list(self, list_of_documents, stop_words):
        posting_list_info = []
        lemmatizer = WordNetLemmatizer()
        terms_count = 0

        max_tf_docID = list()
        max_doclen_docID_list = list()

        for doc in list_of_documents:
            filtered_tokens, docID, doc_len = self.get_tokens(doc, stop_words)

            lemmas = []
            tokens_per_doc1 = set()

            for w in filtered_tokens:
                    lemmas.append(lemmatizer.lemmatize(w))
            token_count_map = my_obj.update_token_count_map(lemmas)
            max_tf = my_obj.get_max_tf(token_count_map)
            max_tf_docID.append((docID, max_tf))
            max_doclen_docID_list.append((docID, doc_len))

            for i in lemmas:
                    tokens_per_doc1.add((i, docID, token_count_map.get(i), max_tf, doc_len))
                    #tokens_per_doc1.add((i, docID, token_count_map.get(i), 0, doc_len))
            #terms_count = terms_count+len(tokens_per_doc1)
            posting_list_info.append(tokens_per_doc1)
        #print(terms_count)

        return posting_list_info, max_tf_docID, max_doclen_docID_list

    #Stemming
    def get_stems_posting_list(self, list_of_documents, stop_words):
        posting_list_info = []
        max_tf_docID_list = list()
        max_doclen_docID_list = list()

        for doc in list_of_documents:
            filtered_tokens, docID, doc_len = self.get_tokens(doc, stop_words)

            tokens_per_doc1 = set()

            stemmer = PorterStemmer()
            stems = [stemmer.stem(token, 0, len(token)-1) for token in filtered_tokens]

            token_count_map = my_obj.update_token_count_map(stems)
            max_tf = my_obj.get_max_tf(token_count_map)

            max_tf_docID_list.append((docID, max_tf))
            max_doclen_docID_list.append((docID, doc_len))

            for i in stems:
                tokens_per_doc1.add((i, docID, token_count_map.get(i), max_tf, doc_len))
            posting_list_info.append(tokens_per_doc1)

        return posting_list_info, max_tf_docID_list, max_doclen_docID_list

    def create_index(self, posting_list_info, output_file):
        f = open(output_file,"w+")
        hmap = dict()

        for doc_set in posting_list_info:

            for item in doc_set:
                posting_list = list()
                term = item[0]
                postings = (item[1], item[2], item[3], item[4])
                posting_list.append(postings)
                df = 1
                if term not in hmap.keys():
                    hmap[term] = (df,posting_list)
                else:
                    prev_postings = hmap.get(term)
                    prev_posting_list = prev_postings[1]
                    prev_posting_list.append(postings)
                    sorted_postings_list = sorted(prev_posting_list, key=lambda x: x[0])
                    new_df = prev_postings[0]+1
                    hmap[term] = (new_df, sorted_postings_list)
                    
        number_of_postings= len(hmap.keys())
        for key in sorted(hmap.keys()):
            term = key
            val = hmap[key]
            df = val[0]
            postings = val[1]
            posting_structure = '-->'.join(str(i) for i in postings)
            f_structure = term+"\t"+str(df)+"\t"+posting_structure
            f.write(f_structure)
            f.write("\n")

        return hmap,number_of_postings

    def block_compression(self, lemmas_uncompressed_dict, output_file):
        my_obj = Main()
        block = ''
        file = open(output_file, 'w+')
        for term in sorted(lemmas_uncompressed_dict.keys()):
            block += str(len(term))
            block += term
        file.write(block)
        file.write("\n")

        count = 0
        term_string = ""
        for term in sorted(lemmas_uncompressed_dict.keys()):
            value = lemmas_uncompressed_dict.get(term)
            gap_list = []
            df = value[0]
            posting_list = value[1]
            first_posting = posting_list[0]
            doc_id = first_posting[0]
            gap_list.append(doc_id)
            i = 1
            while i < len(posting_list):
                gap_list.append(posting_list[i][0] - posting_list[i - 1][0])
                i += 1

            binary_string = ""

            for gaps in gap_list:
                gamma_code = str(my_obj.gamma_code(gaps))
                binary_string+=gamma_code

            term_string += str(len(term))
            term_string += term
            if count % 4 == 0:
                pointer = len(term_string)
                file.write(str(df)+":"+binary_string+":"+str(pointer)+"\n")
                term_string = ""
            else:
                file.write(str(df) + ":" + binary_string+"\n")
            count += 1

    def get_frontcodingstring(self, terms_list):
        frontCodingString = ""
        sz, ret = zip(*terms_list), ""
        for c in sz:
            if len(set(c)) > 1:
                break
            ret += c[0]
        frontCodingString += str(len(terms_list[0])) + ret + "*" + terms_list[0][len(ret):] + str(1) + "<>"
        i = 1
        while (i < len(terms_list)):
            temp_str = terms_list[i]
            res = temp_str[len(ret):]
            frontCodingString += res + str(i + 1) + "<>"
            i += 1
        frontCodingString = frontCodingString[:-len("<>")]
        return frontCodingString


    def front_coding(self, stems_uncompressed_dict, output_file):
        file = open(output_file, 'w+')
        my_obj = Main()
        frontCodingString = ""
        count = 0
        temp_list = list()

        for term in sorted(stems_uncompressed_dict.keys()):
            temp_list.append(term)

            if count % 8==0:
                frontCodingString += my_obj.get_frontcodingstring(temp_list)
                temp_list = list()

            count += 1

        remaining_terms = list()
        k = -4
        while k<0:
            remaining_terms.append(sorted(stems_uncompressed_dict.keys())[k])
            k+=1
        frontCodingString += my_obj.get_frontcodingstring(remaining_terms)
        file.write(frontCodingString)
        file.write("\n")

        #compress postings of stems
        pointer = 0
        term_string = ""
        for term in sorted(stems_uncompressed_dict.keys()):
            value = stems_uncompressed_dict.get(term)
            gap_list = []
            df = value[0]
            posting_list = value[1]
            first_posting = posting_list[0]
            doc_id = first_posting[0]
            gap_list.append(doc_id)
            i = 1
            while i < len(posting_list):
                gap_list.append(posting_list[i][0] - posting_list[i - 1][0])
                i += 1

            binary_string = ""

            for gaps in gap_list:
                delta_code = str(my_obj.delta_code(gaps))
                binary_string += delta_code

            term_string += str(len(term))
            term_string += term
            if pointer % 8 == 0:
                pointer_temp = len(term_string)
                file.write(str(df) + ":" + binary_string + ":" + str(pointer_temp) + "\n")
                term_string = ""
            else:
                file.write(str(df) + ":" + binary_string + "\n")
            pointer += 1


    def unary_code(self, number):
        unary = ""
        i = 0
        while i<number:
            unary+=str(1)
            i+=1
        unary = unary+str(0)
        return unary

    def gamma_code(self, num):
        my_obj = Main()
        binary_num = str(bin(num))
        offset = binary_num[3:]
        offset_length = len(offset)
        length = my_obj.unary_code(offset_length)
        gamma_code = str(length) + str(offset)
        return gamma_code

    def delta_code(self, num):
        my_obj = Main()
        binary_num = str(bin(num))
        offset = binary_num[3:]
        offbin = binary_num[2:]
        gammacode = my_obj.gamma_code(len(offbin))
        delta_code = gammacode + offset
        return delta_code

    def get_results_for_terms(self, term_postings_dict):
        terms_list = ["reynolds", "nasa", "prandtl", "flow", "pressure", "boundary", "shock"]
        terms_list = list(item.lower() for item in terms_list)
        result = list()

        for key in term_postings_dict:
            if key in terms_list:
                value = term_postings_dict[key]
                df = value[0]
                inverted_list_len = sys.getsizeof(value[1])
                inverted_list = value[1]
                tf = 0
                for i in inverted_list:
                    tf = tf + i[1]
                result.append((key, df, inverted_list_len, tf))
        return result

    def get_result_for_NASA(self, term_postings_dict):
        
        value = term_postings_dict.get('nasa')
        df = value[0]
        inverted_list = value[1]
        result = list()

        i=0
        while(i<3):
            posting = inverted_list[i]
            tf = posting[1]
            doclen = posting[3]
            max_tf = posting[2]
            result.append((df, tf, doclen, max_tf))
            i+=1
        return result

    def get_largest_smallest_df(self, term_postings_dict):
        sorted_term_postings_list = sorted(term_postings_dict.items(), key=lambda x: x[1][0])

        first_item = sorted_term_postings_list[0]
        smallest_df = first_item[1][0]

        last_item = sorted_term_postings_list[-1]
        largest_df = last_item[1][0]

        smallest_df_terms = list()
        largest_df_terms = list()

        for item in sorted_term_postings_list:
            df = item[1][0]
            if df == smallest_df:
                smallest_df_terms.append(item[0])
            else:
                break

        for item in reversed(sorted_term_postings_list):
            df = item[1][0]
            if df == largest_df:
                largest_df_terms.append(item[0])
            else:
                break

        return smallest_df, largest_df, smallest_df_terms, largest_df_terms


if __name__ == '__main__':
    my_obj = Main()
    start_time = time.time()
    print("starting code")
    dir = "/people/cs/s/sanda/cs6322/Cranfield/*"
    #dir = "E:/Edmission_Application/UTD/Classes/IR/HW_2/Homework2/Cranfield/Cranfield/*"
    files = glob.glob(dir)
    
    
    results = "results"
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir,results)
    os.mkdir(path)
    

    stop_words_file =  open("/people/cs/s/sanda/cs6322/resourcesIR/stopwords", "r")
    stop_words = stop_words_file.read().splitlines()
    stop_words = [word.strip() for word in stop_words if word]

    lemmas_posting_list_info, max_tf_docID_list_v1, max_doclen_docID_list_v1 = my_obj.get_lemmas_posting_list(files, stop_words)

    index_v1_uncompressed = path+"/index_version1_uncompressed.txt"
    index_v1_compressed = path+"/index_version1_compressed.txt"


    lemmas_postings_map,number_of_postings_v1 = my_obj.create_index(lemmas_posting_list_info, index_v1_uncompressed)
    end_time1 = time.time()
    print("time taken for building version 1 uncompressed index", end_time1-start_time)

    start_time3 = time.time()
    my_obj.block_compression(lemmas_postings_map, index_v1_compressed)
    end_time3 = time.time()
    print("time taken for building version 1 compressed index", end_time3 - start_time3)

    index_v2_uncompressed = path+"/index_version2_uncompressed.txt"
    index_v2_compressed = path+"/index_version2_compressed.txt"
    
    start_time2 = time.time()
    stems_posting_list_info, max_tf_docID_list_v2, max_doclen_docID_list_v2 = my_obj.get_stems_posting_list(files, stop_words)
    stems_postings_map,number_of_postings_v2 = my_obj.create_index(stems_posting_list_info, index_v2_uncompressed)
    end_time2 = time.time()
    print("time taken for building version 2 uncompressed index", end_time2-start_time2)

    start_time4 = time.time()
    my_obj.front_coding(stems_postings_map, index_v2_compressed)
    end_time4 = time.time()
    print("time taken for building version 2 compressed index", end_time4-start_time4)

    print("------------------------------------------------")
    print("size of the index version 1 uncompressed (in bytes)", os.path.getsize(index_v1_uncompressed))
    print("size of the index version 1 compressed (in bytes)", os.path.getsize(index_v1_compressed))
    print("size of the index version 2 uncompressed (in bytes)", os.path.getsize(index_v2_uncompressed))
    print("size of the index version 1 compressed (in bytes)", os.path.getsize(index_v2_compressed))

    print("------------------------------------------------")

    version1_result = my_obj.get_results_for_terms(lemmas_postings_map)
    print("df, tf , inverted list length for terms given from index version1 :",version1_result)

    version2_result = my_obj.get_results_for_terms(stems_postings_map)
    print("df, tf , inverted list length for terms given from index version2 :",version2_result)

    nasa_result_v1 = my_obj.get_result_for_NASA(lemmas_postings_map)
    print("first 3 posting list of nasa :",nasa_result_v1)

    
    print("number of postings in index version1 :",number_of_postings_v1)
    print("number of postings in index version2 :",number_of_postings_v2)
    smallest_df_v1, largest_df_v1, smallest_df_terms_v1, largest_df_terms_v1 = my_obj.get_largest_smallest_df(lemmas_postings_map)
    smallest_df_v2, largest_df_v2, smallest_df_terms_v2, largest_df_terms_v2 = my_obj.get_largest_smallest_df(stems_postings_map)
    
    print("dictionary terms from index1 with largest df: ",largest_df_terms_v1)
    print("dictionary terms from index1 with smallest df :",smallest_df_terms_v1)
    print("dictionary terms from index2 with largest df:",largest_df_terms_v2)
    print("dictionary terms from index2 with smallest df:",smallest_df_terms_v2)
    
    
    sorted_max_tf_docID_list_v1 = sorted(max_tf_docID_list_v1, key=lambda x: x[1])
    docID_max_tf = sorted_max_tf_docID_list_v1[-1][0]

    print("The document id with largest max_tf", docID_max_tf)

    sorted_max_doclen_docID_list_v1 = sorted(max_doclen_docID_list_v1, key=lambda x: x[1])
    docID_max_doclen = sorted_max_doclen_docID_list_v1[-1][0]

    print("The document id with largest doclen ", docID_max_doclen)