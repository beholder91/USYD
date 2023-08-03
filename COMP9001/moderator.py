"""
Author: Kehao Chen
SID: 520305074
Unikey: kche3315
"""

import sys
from datetime import datetime


# self defined errors
class InvalidLineError(Exception):
    pass


class InvalidNameError(Exception):
    pass


class InvalidScoreError(Exception):
    pass


class InvalidFormatError1(Exception):
    pass


class InvalidFormatError2(Exception):
    pass


class InvalidDateError(Exception):
    pass


class ChronologicalError1(Exception):
    pass


class ChronologicalError2(Exception):
    pass


class AssertionError1(Exception):
    pass


# User class used in part6
class User:
    def __init__(self, name):
        self.name = name
        self.engagement = float(0)
        self.expressiveness = float(0)
        self.offensiveness = float(0)

    def process_message(self, message: str, banned_words: list) -> bool:
        try:
            assert type(message) == str  # if the message is not a string, return False

            if message.find("\t") != -1:  # it is a reply
                self.engagement += 1
            else:
                self.engagement += 1.5

            if message.find("!") != -1:  # find ! in message
                if message.find("?") != -1:  # find ? in message
                    if message.find("\t") != -1:  # it is a reply
                        self.expressiveness += 2
                    else:  # it is a post
                        self.expressiveness += 3
                else:  # message only contains !
                    if message.find("\t") != -1:
                        self.expressiveness += 1
                    else:
                        self.expressiveness += 1.5
            else:  # doesn't find ! in message
                if message.find("?") == -1:  # doesn't find ? in message
                    if message.find("\t") != -1:
                        self.expressiveness -= 1
                    else:
                        self.expressiveness -= 1.5

            # start checking banned words in the message
            i = 0
            while i < len(banned_words):
                if message.find(banned_words[i]) != -1:  # find a banned word
                    if message.find("\t") != -1:
                        self.offensiveness += 1
                        break  # only plus 1 whatever how much banned words found
                    else:
                        self.offensiveness += 1.5
                        break
                i += 1

            # nothing wrong above
            return True
        except AssertionError:
            return False

    def calculate_personality_score(self) -> int:
        score = self.expressiveness - self.offensiveness
        if score > self.engagement:
            return int(self.engagement)
        else:
            return int(score)


# check the format validation for each line in people file
def is_valid_line(line):
    i = 0
    while i < len(line):
        if line[i] == ",":
            if i == 0:
                return False  # comma is the first character
            elif i == len(line) - 1:  # doesn't contain comma
                return False
        i += 1
    if i == len(line):
        if line[-1] == "\n":  # the last char must be \n
            return True


# check the validation of name
def is_valid_name(name):
    # nothing
    if name == "":
        return False
    # space only
    elif name.isspace():
        return False
    # valid cases
    i = 0
    while i < len(name):
        if name[i] == " " or name[i].isalpha() == True or name[i] == "-":  # is a space of letter
            i += 1
        else:
            return False
    # nothing false for all characters
    if i == len(name):
        return True


# check the validation of score
def is_valid_score(score):
    if -10 <= score <= 10:
        return True
    else:
        return False


# check the validation of file header
def is_valid_header(filename):
    file = open(filename, "r")
    file_list = file.readlines()

    # check the first line of the file is not empty
    if file_list[0] == "\n":
        return False
    # check the second line is empty
    elif file_list[1] != "\n":
        return False
    else:
        return True


# check the format of datetime
def date_format(date):
    try:
        # check numbers
        i = 0
        while i < 4:
            assert date[i].isdigit() == True
            i += 1

        i = 2
        while i < 7:
            assert date[3 * i - 1].isdigit() == True
            assert date[3 * i].isdigit() == True
            i += 1

        # check symbols
        assert date[4] == "-"
        assert date[7] == "-"
        assert date[10] == "T"
        assert date[13] == ":"
        assert date[16] == ":"

        # nothing wrong then valid
        return True

    except AssertionError:
        return False


# check chronological
def is_chronological(earlier_dt: str, later_dt: str):
    format_dt = "%Y-%m-%dT%H:%M:%S"
    date1 = datetime.strptime(earlier_dt, format_dt)
    date2 = datetime.strptime(later_dt, format_dt)
    if date1 < date2:
        return True
    else:
        return False


# check words file format
def check_words(word):
    if word == "":
        return False
    elif word.isspace():
        return False
    else:
        return True


# Part3: Personality scores
def rank_people():
    try:
        # find the location of -log
        c = 1
        while c <= 5:
            if sys.argv[2 * c - 1] == "-log":
                break
            c += 1

        # find the location of -people
        k = 1
        while k <= 5:
            if sys.argv[2 * k - 1] == "-people":
                assert is_valid_header(sys.argv[2 * k]) == True  # check file head valid
                break
            k += 1

        people_read_file = open(sys.argv[2 * k], 'r')
        people_all_lines = people_read_file.readlines()

        # not index position, but actual position in the file
        people_line = 3
        while people_line < len(people_all_lines) + 1:
            # check line format valid
            if not is_valid_line(people_all_lines[people_line - 1]):
                raise InvalidLineError
            # separate the line into a list with 2 elements
            line_list = people_all_lines[people_line - 1].strip("\n").split(",")
            # check name valid
            if not is_valid_name(line_list[0]):
                raise InvalidNameError
            # check score valid
            elif not is_valid_score(int(line_list[1])):  # may occur ValueError when convert string to int
                raise InvalidScoreError
            people_line += 1

        # no error happened, create the log file
        if people_line == len(people_all_lines) + 1:
            log_file = open(sys.argv[2 * c], "w")
            log_file.close()

        #  close the readable file
        people_read_file.close()

        # sort the score in descending order
        l = 2
        list1 = []  # store the name & scores in this list
        while l < len(people_all_lines):
            list2 = people_all_lines[l].strip("\n").split(",")
            list1.append(list2)
            l += 1

        # input the name_score list and return the score
        def sort_key(input_line):
            return int(input_line[1])

        # apply the sort function on score
        list1.sort(key=sort_key, reverse=True)

        # re-write the file
        people_write_file = open(sys.argv[2 * k], 'w')

        # write the first two lines, the second line is empty
        print(people_all_lines[0], file=people_write_file)

        # write the content of lines
        m = 0
        while m < len(list1):
            print(list1[m][0], ",", list1[m][1], file=people_write_file, sep="")
            m += 1
        people_write_file.close()

    except AssertionError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The people file header is incorrectly formatted", file=log_file)
        log_file.close()
    except InvalidLineError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The people entry is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()
    except InvalidNameError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The user's name is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()
    except InvalidScoreError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The personality score is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()
    except ValueError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The personality score is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()


# part4: reading the forum
def validate_forum():
    try:
        # find the location of -log
        c = 1
        while c <= 5:
            if sys.argv[2 * c - 1] == "-log":
                log_file = open(sys.argv[2 * c], "w")
                log_file.close()
                break
            c += 1

        fl = 1  # forum location
        while fl <= 5:
            if sys.argv[2 * fl - 1] == "-forum":
                assert is_valid_header(sys.argv[2 * fl]) == True  # check file header
                break
            fl += 1

        forum_read_file = open(sys.argv[2 * fl], "r")
        forum_all_lines = forum_read_file.readlines()

        # line 3 is a reply, invalid format for reply before post
        if forum_all_lines[2].find("/t") != -1:
            raise InvalidFormatError1

        # check format of every post
        forum_line = 0
        while forum_line < (len(forum_all_lines) - 2) / 3:
            if forum_all_lines[3 * forum_line + 2].find("\n") != -1:  # find /n in line
                if forum_all_lines[3 * forum_line + 2].find("\t") != -1:  # find /t in line
                    if forum_all_lines[3 * forum_line + 3].find("\t") == -1:  # doesn't find /t in nextline
                        error_line = 3 * forum_line + 3  # record the line that error happened
                        raise InvalidFormatError2
                    elif forum_all_lines[3 * forum_line + 4].find("\t") == -1:
                        error_line = 3 * forum_line + 4
                        raise InvalidFormatError2
                else:  # doesn't find /t in line
                    if forum_all_lines[3 * forum_line + 3].find("\t") != -1:  # find \t in nextline
                        error_line = 3 * forum_line + 3
                        raise InvalidFormatError2
                    elif forum_all_lines[3 * forum_line + 4].find("\t") != -1:
                        error_line = 3 * forum_line + 4
                        raise InvalidFormatError2
            else:  # doesn't find /n in line
                error_line = 3 * forum_line + 2
                raise InvalidFormatError2

            forum_line += 1

        # check the datetime
        date_line = 0
        while date_line < (len(forum_all_lines) - 2) / 3:
            date = forum_all_lines[3 * date_line + 2].strip("\n").strip("\t")
            if not date_format(date):
                raise InvalidDateError

            date_line += 1

        # check user's name
        name_line = 0
        while name_line < (len(forum_all_lines) - 2) / 3:
            name = forum_all_lines[3 * name_line + 3].strip("\n").strip("\t")
            if not is_valid_name(name):
                raise InvalidNameError

            name_line += 1

        # check chronological
        valid_date_line = 1
        while valid_date_line < (len(forum_all_lines) - 2) / 3:
            if forum_all_lines[3 * valid_date_line + 2].find("\t") != -1:  # it is a reply
                # this time must after the former one whatever is a post or a reply
                if not is_chronological(forum_all_lines[3 * valid_date_line - 1].strip("\n").strip("\t"),
                                        forum_all_lines[3 * valid_date_line + 2].strip("\n").strip("\t")):
                    raise ChronologicalError1
            else:  # it is a post
                post_lines = 1
                while post_lines <= valid_date_line:
                    if forum_all_lines[3 * (valid_date_line - post_lines) + 2].find("\t") == -1:  # it is a post
                        # must after all the post before
                        if not is_chronological(
                                forum_all_lines[3 * (valid_date_line - post_lines) + 2].strip("\n").strip("\t"),
                                forum_all_lines[3 * valid_date_line + 2].strip("\n").strip("\t")):
                            raise ChronologicalError2
                    post_lines += 1
            valid_date_line += 1

        forum_read_file.close()

    except AssertionError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The forum file header is incorrectly formatted", file=log_file)
        log_file.close()
    except InvalidFormatError1:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The reply is placed before a post on line 3", file=log_file)
        log_file.close()
    except InvalidFormatError2:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The post has an invalid format on line {}".format(error_line), file=log_file)
        log_file.close()
    except InvalidDateError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The datetime string is invalid on line {}".format(3 * date_line + 3),
              file=log_file)
        log_file.close()
    except InvalidNameError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The user's name is invalid on line {}".format(3 * name_line + 4), file=log_file)
        log_file.close()
    except ChronologicalError1:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The reply is out of chronological order on line {}".
              format(3 * valid_date_line + 3), file=log_file)
        log_file.close()
    except ChronologicalError2:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: forum file read. The post is out of chronological order on line {}".
              format(3 * valid_date_line + 3), file=log_file)
        log_file.close()


# Part5: censoring the forum
def censor_forum():
    try:
        # find the location of -log
        c = 1
        while c <= 5:
            if sys.argv[2 * c - 1] == "-log":
                log_file = open(sys.argv[2 * c], "w")  # create log file first
                log_file.close()
                break
            c += 1

        wl = 1  # word location
        while wl <= 5:
            if sys.argv[2 * wl - 1] == "-words":
                assert is_valid_header(sys.argv[2 * wl]) == True
                break
            wl += 1

        # read words-file, and put every word in a list
        words_read_file = open(sys.argv[2 * wl], "r")
        words_all_lines = words_read_file.readlines()  # banned words start from line3 (index: 2)
        words_read_file.close()

        # check the format of words-file
        words_line = 2
        while words_line < len(words_all_lines):
            if words_all_lines[words_line].find("\n") != -1:  # has newline char
                if not check_words(words_all_lines[words_line].strip("\n")):
                    raise InvalidFormatError1
            else:  # no newline char
                raise InvalidFormatError1
            words_line += 1

        # test the validation as part4
        validate_forum()
        read_log_file = open(sys.argv[2 * c], "r")
        log_file_list = read_log_file.readlines()
        read_log_file.close()

        # if something wrong, the log file will not be empty
        if log_file_list != []:
            quit()

        # find the location of forum file
        fl = 1  # forum location
        while fl <= 5:
            if sys.argv[2 * fl - 1] == "-forum":
                break
            fl += 1

        # open the forum file, put every line in a list
        forum_read_file = open(sys.argv[2 * fl], "r")
        forum_all_lines = forum_read_file.readlines()
        forum_read_file.close()

        # start replacing banned words
        forum_new_lines = [forum_all_lines[0], forum_all_lines[1]]  # make a new list and add header

        # start to check the post
        forum_line = 2
        while forum_line < len(forum_all_lines):
            if forum_line % 3 != 1:  # not the message of the post, do not change
                forum_new_lines.append(forum_all_lines[forum_line])  # add the line directly
            else:  # the message of the post, need to check
                message = forum_all_lines[forum_line]  # the message of post, a string
                lower_message = message.lower()  # change th message into lower case
                symbol = (" ", "\n", "\t", ",", ".", "'", '"', "(", ")", "!", "?")

                # a function to check if a char is in symbol
                def has_symbol(char):
                    i = 0
                    while i < len(symbol):
                        if char == symbol[i]:
                            return True
                        i += 1
                    if i == len(symbol):
                        return False

                i = 2  # except the header of the words file
                while i < len(words_all_lines):
                    ban_word = words_all_lines[i].strip("\n").lower()  # banned word in lower case

                    while True:  # a message could appear a ban word more than once.
                        index = lower_message.find(ban_word)
                        if index != -1:  # find a banned word
                            if has_symbol(lower_message[index - 1]):
                                if has_symbol(lower_message[index + len(ban_word)]):
                                    # replace banned words in lower message
                                    lower_message = lower_message.replace(ban_word,
                                                                          len(ban_word) * "*")
                                else:
                                    # replace another symbol, in case of infinite interation
                                    lower_message = lower_message.replace(ban_word,
                                                                          len(ban_word) * "@")
                            else:
                                lower_message = lower_message.replace(ban_word, len(ban_word) * "#")
                        else:  # not find any banned word
                            break
                    i += 1

                # all banned words have converted into * in lower_message
                list_message = list(message)  # convert every char in message into list

                k = 0
                while k < len(list_message):
                    if lower_message[k] == "*":
                        list_message[k] = "*"
                    k += 1

                message = "".join(list_message)  # join each element in the list into a string
                forum_new_lines.append(message)  # add the cryptographic message into list

            forum_line += 1

        forum_write_file = open(sys.argv[2 * fl], "w")
        j = 0
        while j < len(forum_new_lines):
            print(forum_new_lines[j], file=forum_write_file, end="")
            j += 1

        forum_write_file.close()

    except AssertionError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: words file read. The words file header is incorrectly formatted", file=log_file)
        log_file.close()
    except InvalidFormatError1:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: words file read. The banned word is invalid on line {}".format(words_line + 1), file=log_file)
        log_file.close()


# Part6
def evaluate_forum():
    try:
        # find the location of -log
        c = 1
        while c <= 5:
            if sys.argv[2 * c - 1] == "-log":
                log_file = open(sys.argv[2 * c], "w")
                log_file.close()
                break
            c += 1

        # -------------------------------------------------test the validation as part4
        validate_forum()
        read_log_file = open(sys.argv[2 * c], "r")
        log_file_list = read_log_file.readlines()
        read_log_file.close()

        # if something wrong, the log file will not be empty
        if log_file_list != []:
            quit()

        # -------------------------------------------------test the validation as part5
        wl = 1  # word location
        while wl <= 5:
            if sys.argv[2 * wl - 1] == "-words":
                assert is_valid_header(sys.argv[2 * wl]) == True
                break
            wl += 1

        # read words-file, and put every word in a list
        words_read_file = open(sys.argv[2 * wl], "r")
        words_all_lines = words_read_file.readlines()  # banned words start from line3 (index: 2)
        words_read_file.close()

        # check the format of words-file
        words_line = 2
        while words_line < len(words_all_lines):
            if words_all_lines[words_line].find("\n") != -1:  # has newline char
                if not check_words(words_all_lines[words_line].strip("\n")):
                    raise InvalidFormatError1
            else:  # not newline char
                raise InvalidFormatError1
            words_line += 1

        # --------------------------------------------------test the validation of part 3
        # find the location of -people
        pl = 1
        while pl <= 5:
            if sys.argv[2 * pl - 1] == "-people":
                if not is_valid_header(sys.argv[2 * pl]):  # check file head valid
                    raise AssertionError1
                break
            pl += 1

        people_read_file = open(sys.argv[2 * pl], 'r')
        people_all_lines = people_read_file.readlines()
        people_read_file.close()

        # not index position, but actual position in the file
        people_line = 3
        while people_line < len(people_all_lines) + 1:
            # check line format valid
            if not is_valid_line(people_all_lines[people_line - 1]):
                raise InvalidLineError
            line_list = people_all_lines[people_line - 1].strip("\n").split(",")
            # check name valid
            if not is_valid_name(line_list[0]):
                raise InvalidNameError
            # check score valid
            elif not is_valid_score(int(line_list[1])):  # may occur ValueError when convert string to int
                raise InvalidScoreError
            people_line += 1

        # ____________________________________________________________________________________________
        # ------------------all validate works done, start the calculation part ----------------------#

        fl = 1  # forum location
        while fl <= 5:
            if sys.argv[2 * fl - 1] == "-forum":
                break
            fl += 1

        forum_read_file = open(sys.argv[2 * fl], "r")
        forum_all_lines = forum_read_file.readlines()
        forum_read_file.close()

        # clean the forum file list, only name & message retain
        fls = 1
        forum_name_lines = []  # the new list of forum, only contains name
        forum_message_lines = []  # only contains messages
        while fls <= (len(forum_all_lines) - 2) / 3:
            forum_name_lines.append(forum_all_lines[3 * fls].strip("\n").strip("\t"))
            forum_message_lines.append(forum_all_lines[3 * fls + 1].strip("\n"))
            fls += 1

        # clean the words file list
        words_list = []
        wls = 2
        while wls < len(words_all_lines):
            word = words_all_lines[wls].strip("\n")
            words_list.append(word)
            wls += 1

        name_message = {}  # create a dictionary to store name and corresponding message
        e = 0
        while e < len(forum_name_lines):
            f = 0
            while f < len(name_message):
                if forum_name_lines[e] == list(name_message.keys())[f]:
                    name_message[forum_name_lines[e]].append(forum_message_lines[e])
                    break
                f += 1
            if f == len(name_message):
                name_message[forum_name_lines[e]] = forum_message_lines[e].split("   ##    ")  # make a list
            e += 1

        # split the dictionary into two list with corresponding index
        # a name could contain many messages
        forum_name_lines = list(name_message.keys())
        forum_message_lines = list(name_message.values())

        # start instantiating
        name_score = {}  # create a dictionary to store user's name and their score
        i = 0
        while i < len(forum_name_lines):
            # make instance
            user = User(forum_name_lines[i])
            # check every message the user published
            j = 0
            while j < len(forum_message_lines[i]):
                # calculate the offensiveness
                user.process_message(forum_message_lines[i][j], words_list)
                j += 1
            # calculate the score
            user_score = user.calculate_personality_score()
            # append the name and score into the list
            name_score[user.name] = user_score
            i += 1

        # handle the people file into a dictionary
        name_score_original = {}
        pls = 2
        while pls < len(people_all_lines):
            line = people_all_lines[pls].strip("\n").split(",")
            name_score_original[line[0]] = int(line[1])
            pls += 1

        # now we get two dictionaries, add the new one to the exist one
        # use while loop instead of for loop, need separate the dictionary here
        original_name = list(name_score_original.keys())
        original_score = list(name_score_original.values())
        add_name = list(name_score.keys())
        add_score = list(name_score.values())

        m = 0
        while m < len(original_name):
            n = 0
            while n < len(add_name):
                if original_name[m] == add_name[n]:
                    original_score[m] += add_score[n]
                    break
                n += 1
            m += 1

        # cap in range (-10, 10)
        z = 0
        while z < len(original_score):
            if original_score[z] > 10:
                original_score[z] = 10
            elif original_score[z] < -10:
                original_score[z] = -10
            z += 1

        # sorted the list
        original_score, original_name = zip(*sorted(zip(original_score, original_name), reverse=True))

        # write people file
        people_write_file = open(sys.argv[2 * pl], 'w')
        # write the header
        print(people_all_lines[0], file=people_write_file, end="")
        print(people_all_lines[1], file=people_write_file, end="")

        write_line = 0
        while write_line < len(original_score):
            print("{},{}".format(original_name[write_line], original_score[write_line]), file=people_write_file)
            write_line += 1

        people_write_file.close()


    # part5 error
    except AssertionError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: words file read. The words file header is incorrectly formatted", file=log_file)
        log_file.close()
    except InvalidFormatError1:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: words file read. The banned word is invalid on line {}".format(words_line + 1), file=log_file)
        log_file.close()
    # part3 error
    except AssertionError1:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The people file header is incorrectly formatted", file=log_file)
        log_file.close()
    except InvalidLineError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The people entry is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()
    except InvalidNameError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The user's name is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()
    except InvalidScoreError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The personality score is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()
    except ValueError:
        log_file = open(sys.argv[2 * c], "w")
        print("Error: people file read. The personality score is invalid on line {}".format(people_line),
              file=log_file)
        log_file.close()


# Part 2: Command line arguments, main function
def main():
    try:
        cmd_list = ["task", "log", "forum", "words", "people"]
        task_list = ["rank_people", "validate_forum", "censor_forum", "evaluate_forum"]

        # check missing argument in command line
        i = 0
        while i < 5:
            j = 0
            while j < (len(sys.argv) - 1) / 2:
                if sys.argv[2 * j + 1] == "-" + cmd_list[i]:
                    break
                j += 1
            if j == (len(sys.argv) - 1) / 2:  # doesn't find the argument
                raise AssertionError
            i += 1

        # valid command line input
        if i == 5:  # all arguments are provided
            # check task
            a = 0
            while a < (len(sys.argv) - 1) / 2:
                if sys.argv[2 * a + 1] == "-task":
                    b = 0
                    while b < len(task_list):
                        if sys.argv[2 * a + 2] == task_list[b]:
                            break
                        b += 1
                    if b == len(task_list):  # doesn't find the valid task
                        raise NotImplementedError
                a += 1

            # check file readable
            k = 1
            while k <= 5:
                if sys.argv[2 * k - 1] == "-forum":
                    read_file = open(sys.argv[2 * k], 'r')
                    read_file.close()
                elif sys.argv[2 * k - 1] == "-words":
                    read_file = open(sys.argv[2 * k], 'r')
                    read_file.close()
                elif sys.argv[2 * k - 1] == "-people":
                    read_file = open(sys.argv[2 * k], 'r')
                    read_file.close()
                k += 1

        # not any error raise
        print("Moderator program starting...")

        # find the position of task
        task_line = 0
        while task_line < (len(sys.argv) - 1) / 2:
            if sys.argv[2 * task_line + 1] == "-task":
                if sys.argv[2 * task_line + 2] == task_list[0]:
                    rank_people()
                    break
                elif sys.argv[2 * task_line + 2] == task_list[1]:
                    validate_forum()
                    break
                elif sys.argv[2 * task_line + 2] == task_list[2]:
                    censor_forum()
                    break
                elif sys.argv[2 * task_line + 2] == task_list[3]:
                    evaluate_forum()
                    break
            task_line += 1

    except AssertionError:
        print("No {} arguments provided.".format(cmd_list[i]))
    except NotImplementedError:
        print("Task argument is invalid.")
    except Exception:
        print("{} cannot be read.".format(sys.argv[2 * k]))


# program start
if __name__ == '__main__':
    main()
