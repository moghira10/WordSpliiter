## Word Splitter
import os
from nltk.corpus import words
from Trie import Trie
from SpellChecker import SpellCheck


class WordSplitter(object):
    def __init__(self, directory_name):
        self.data_path = os.path.join(os.path.abspath(os.path.join("..", os.path.abspath('..'))), directory_name)
        self.csv_path = os.path.join(self.data_path, "csv")
        self.txt_path = os.path.join(self.data_path, "txt")
        self.splitList = list()
        self.irrelevant = ''
        self.MAX_SCORE = 0
        self.PREVIOUS = ''
        self.english = set()
        self.trie = Trie()
        self.sc = SpellCheck('dataset')
        with open(os.path.join(self.csv_path, "words.csv"), "r") as fin:
            for data in fin.readlines():
                self.trie.insert(data.strip().lower())
                self.english.add(data.strip().lower())
        # with open(os.path.join(self.csv_path, "nltk_words.csv"), "r") as fin:
        #     for data in fin.readlines():
        #         self.trie.insert(data.strip().lower())
        with open(os.path.join(self.csv_path, "hindi.csv"), "r") as fin:
            for data in fin.readlines():
                self.trie.insert(data.strip().lower())

    # Returns edge ngram with start offset
    def edgengram(self, str, start=2):
        egrams = []
        for i in range(start, len(str) + 1):
            egrams.append(str[0:i])
        return egrams

    # Check if english word
    def is_english(self, word):
        return word in self.english

    def get_tokens(self):
        return self.splitList

    def get_irrelevant_tokens(self):
        return self.irrelevant

    def subsequence(self, collocatedText):
        # Recursive Python program to check if a string is subsequence
        # of another string

        # Returns true if str1[] is a subsequence of str2[]. m is
        # length of str1 and n is length of str2
        def isSubSequence(string1, string2, m, n, score=0, match=0):

            # print(string1 + "-> " + str(m) + " " + string2 +  "-> " + str(n))
            # Base Cases
            if m == 0:    return score
            if n == 0:    return -1

            # If last characters of two strings are matching
            if string1[m - 1] == string2[n - 1]:
                match = 1
                score += 1
                return isSubSequence(string1, string2, m - 1, n - 1, score, match)
            else:
                score = 0
                match = 0
                if len(string1) > m:
                    m = m + 1

            # If last characters are not matching
            return isSubSequence(string1, string2, m, n - 1, score, match)

        # Driver program to test the above function  raeejhumkasaree
        prefixList = self.trie.get_all_with_prefix(collocatedText[:2])
        token = ''
        for word in prefixList:
            m = len(word)
            n = len(collocatedText)
            subsequence_score = isSubSequence(word, collocatedText, m, n)

            # if subsequence_score >= 0:
            #     print(word + " : " + str(subsequence_score))

            if (word not in collocatedText and len(word) > 1) or word == self.PREVIOUS:
                self.irrelevant = collocatedText[:1]
                continue

            self.PREVIOUS = word
            # Check for the most accurate match
            if subsequence_score >= 0 and len(word) > 1:
                if subsequence_score >= self.MAX_SCORE:
                    token = word
                    self.MAX_SCORE = subsequence_score
            else:
                self.irrelevant = collocatedText[:1]

        return token

    def split(self, collocatedText,prevTokenIndex=0):
        if not collocatedText:
            return

        if len(self.splitList) == prevTokenIndex+1:
            lastToken = self.splitList[prevTokenIndex]
            if lastToken[-1] == 's':
                collocatedText = 's' + collocatedText
                prevTokenIndex += 1


        spell_token = self.sc.spellCheck(collocatedText)

        if spell_token:
            collocatedText = spell_token

        token = self.subsequence(collocatedText)

        if token and len(token) > 2:
            self.splitList.append(token)
            self.MAX_SCORE = 0
            collocatedText = collocatedText.replace(token, "")
        else:
            if self.irrelevant:
                collocatedText = collocatedText.replace(self.irrelevant, "", 1)
            elif token and len(token) <= 2:
                collocatedText = collocatedText.replace(token, "", 1)

        self.split(collocatedText,prevTokenIndex)


    def run(self, product_title):
        product_list = list()
        for data in product_title.split():
            if '#' in data:
                self.splitList = list()
                self.irrelevant = list()
                self.split(data.split("#")[1].strip())
                value = self.get_tokens()
                for val in value:
                    product_list.append(val)
            else:
                product_list.append(data.strip())
        # bool_list = [any(item in some for some in self.cate) for item in product_list]
        # if True in bool_list:
        return " ".join(product_list)

# ws = WordSplitter('dataset')
# # ws.split("wristwatchescases")
# # material stainless steeldial window material type glassdial material type stainless steelwater resistance depth waterproofmovement quartzband mm mmdial di ameter cmband width cmboxes cases material paperclasp type pin bucklegender menstyle fashion casualcondition new tagsdial display analogfeature nonecase shape roundband material type leatherband length cmcase thickness mmmodel number sb brand name new brandboxes cases material opp bagis customized yesgender unisexspain relojes hombrebrazil relogio femininofemale watch clock womencompany bgg watchwater resistance waterproof life daily life waterproof swimming diving band colors picturestyle dress watchnovel rhinestone ball small dial men wristwatch trendy luxury pu leather watch girls clock hours unisex quartz watch
# ws.split("steeldial")
# print(ws.get_tokens())

# st = time.time()
# TODO lenengasaree
# TODO handle designersaree s trailing second word
# ws.split('sbags')
# ws.split('slimfit')
# ws.split('blackplasticdigitalrectangularbraceletbandledwatchforboys')
# print(time.time() - st)
