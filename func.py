"""
Index entry +
_ +
number/glossary/nothing +
(cross reference(separate by comma o semicolon) ….)

Index Entry = IE
Number Glossary = NG
Cross Reference Parenthesis = CRP

example = "human being(s)_101-231, 399, g (véanse también human rights; declaration, liberty)"

where 	"human being(s)" 		= 	Index Entry --> IE
		"101-231, 399, g"		= 	Number Glossary --> NG
		"(véanse .....liberty)"	=	Cross Reference Parenthesis --> CRP

each sentence always contains: human + '_' in IE_NG + (CPR)
when véanse inside: ',' in CPR part
when véase inside: usually ';' in CPR or a shorter CPR(no ',' inside)
when también: contains digits in IE_NG or ' g ' || '_g '
.......
"""
import re

# variables
syntax_errors = []

errors = {
    "space_err"	 	: "Two or more spaces in your sentence",
    "/_err" 	 	: "You put a space next to '/' or something around not correct",
    "digit_err" 	: "There is a number higher than 1000, does your book really contains that many pages?",
    "IE_NG_err" 	: "Didn't match any of 45 possible IE_NG entries",
    "véanse_err" 	: "No ','  or space after comma inside CRP",
    # tested length on 1250 examples
    "véase_err" 	: "No ';' in CRP or CRP seems to be too long",
    "véase_not_err"	: "There is no 'véase' nor 'véanse' in CPR part",
    "también_err" 	: "You didn't put any digits or letter 'g' as glossary",
    "véase_num_err"	: "You shoudn't have any digits included",
    "_err" 			: "Wrong spacing next to symbol '_ underscore' or '/' or totally missing",
    "double_g_err" 	: "More than one g (glossary)",
    "ending_err" 	: "Missing a closing parantheses ')' in the end",
    "comma_err" 	: "Unexpected symbol around a comma ','",
    "brackets_err" 	: "There is a missing open/closing ( ) or [ ] or { }",
    "doubled_err" 	: "One of following symbols doubled: underscore _ / , ; : ",
    "order_err" 	: "Found digits in CRP",
    "order2_err" 	: "Digits(number of pages) and g(glossary) not in right order",
    "order3_err"	: "Found an underscore in CPR part",
}


# checks for common errors in the sentence
# sheet is the one with over 1200 example, used as a database for IE_finder()
def trouble_killer(phrase, IE_NG_part, CPR_part, sheet):
    global syntax_errors, errs

    syntax_errors.clear()

    # two or more spaces in the sentence
    if "  " in phrase:
        syntax_errors.append(errors["space_err"])

    # a digit higher than 1000 (suspiciously many pages)
    if "****" in phrase or "*****" in IE_NG_part:
        syntax_errors.append(errors["digit_err"])

    # checks for mistakes around commas
    comma_err_finder2(phrase)

    # checks for duplicated symbols
    duplicator_finder(phrase)

    # checks for balanced parentheses in sentence
    parentheses_err_finder(phrase)

    if "*" in phrase and (" g" in phrase or "_g" in phrase):

        if " g" in phrase:
            if phrase.find(" g") < phrase.find("*"):
                syntax_errors.append(errors["order2_err"])

        else:
            if phrase.find("_g") < phrase.find("*"):
                syntax_errors.append(errors["order2_err"])

    # call a func to find specific errors in IE_NG
    IE_NG_trouble_killer(IE_NG_part, CPR_part, sheet)

    # call a func to find specific errors in CPR
    CPR_trouble_killer(CPR_part, IE_NG_part)

    return syntax_errors


# checks for errors in the IE_NG part of the sentence
def IE_NG_trouble_killer(IE_NG_part, CPR_part, sheet):

    entry_error = True
    all_IE_NGs = IE_finder(sheet)

    # check if IE NG structure is correct
    for entry in all_IE_NGs:

        if entry.replace("*", "") in IE_NG_part.replace("*", ""):
            entry_error = False
            break
        else:
            continue

    # if no IE NG structure was found in database
    if entry_error == True:
        syntax_errors.append(errors["IE_NG_err"])

    # a space or other mistake next to "/", only two versions of index entry with "/" exist
    if "/" in IE_NG_part and ("human(s)/being" not in IE_NG_part and "human/being" not in IE_NG_part):
        syntax_errors.append(errors["/_err"])

    # check number of digits when "también" and status of "g" (glossary)
    if "también" in CPR_part:

        # g appears always as " g " or "_g "
        if IE_NG_part.count("*") <= 1 and (" g " not in IE_NG_part and "_g " not in IE_NG_part):
            syntax_errors.append(errors["también_err"])

        elif IE_NG_part.count("_g") + IE_NG_part.count(" g") > 1:
            syntax_errors.append(errors["double_g_err"])
        # there might be an error, imagine having "human global" in IE_NG_part, this wouldn't find correctly "g" at all
        # for that its impossible in every situation to get right order of g/glossary

    # check for syntax "_" error
    if " _" in IE_NG_part or "_ " in IE_NG_part or "_" not in IE_NG_part:
        syntax_errors.append(errors["_err"])

    # check for syntax "/" error
    if " /" in IE_NG_part or "/ " in IE_NG_part:
        syntax_errors.append(errors["_err"])


# checks for errors in the CPR part of the sentence
def CPR_trouble_killer(CPR_part, IE_NG_part):

    # check for syntax "/" error
    if "_" in CPR_part:
        syntax_errors.append(errors["order3_err"])

    # check for comma, order err inside CRP
    comma_err_finder(CPR_part, IE_NG_part)

    # # check for closing ending paranthesis, sometimes there's a long space in the end --> check last 20 letters
    # # closed for now, didn't work for some reason
    # if CPR_part[-1:] != ")":
    # 	for n in range(1, 100):
    # 		print(CPR_part[-n:])

    # 		if CPR_part[-n:] != " " or CPR_part[-n:] != ")":
    # 			syntax_errors.append(errors["ending_err"])
    # 			break


# seaches through all possible IE and NG versions
def IE_finder(sheet):
    index_entry = set()  # stores all possible IE

    for i in range(1, sheet.max_row + 1):
        value = sheet.cell(column=1, row=i).value

        if value != None:

            if "véase" in value:
                IE_NG = value[:value.find("véase")-1]

            if "véanse" in value:
                IE_NG = value[:value.find("véanse")-1]

            entry = re.sub("\d", "*", IE_NG)
            index_entry.add(entry)

        else:
            pass
    return index_entry


# check for comma, order err inside CRP
def comma_err_finder(CPR_part, IE_NG_part):

    if "véanse" in CPR_part:

        if("*") in CPR_part:
            syntax_errors.append(errors["order_err"])

        if ", " not in CPR_part:
            syntax_errors.append(errors["véanse_err"])

    # véase always have ";" inside CRP or len max 27 long (set on 42 for more tolerance)
    elif "véase" in CPR_part:

        if("*") in CPR_part:
            syntax_errors.append(errors["order_err"])

        if ";" not in CPR_part and len(CPR_part) > 42:
            syntax_errors.append(errors["véase_err"])

        if IE_NG_part.count("*") > 0 and "también" not in CPR_part:
            syntax_errors.append(errors["véase_num_err"])

    # every sentence must contain "véase" or "véanse"
    else:
        syntax_errors.append(errors["véase_not_err"])


# check for mistakes around commas
def comma_err_finder2(phrase):
    commas = [comma.start() for comma in re.finditer(',', phrase)]

    if len(commas) > 0:
        for i in commas:

            if phrase[i + 1] != " ":
                syntax_errors.append(errors["comma_err"])

            elif not re.match("[a-z0-9*]", str(phrase[i + 2])):
                syntax_errors.append(errors["comma_err"])


# check for duplicated symbols
def duplicator_finder(phrase):
    special_symbols = "_/,;:"

    for sym in special_symbols:
        if sym in phrase:
            symbol = [symb.start() for symb in re.finditer(sym, phrase)]

            for i in symbol:
                if phrase[i + 1] == sym:
                    syntax_errors.append(errors["doubled_err"])


# check for balanced parentheses in sentence
def parentheses_err_finder(phrase):

    for i in range(3):
        open_brackets = ["({[", 0]
        close_brackets = [")}]", 0]

        for sym in phrase:

            if str(sym) == open_brackets[0][i]:
                open_brackets[1] += 1

            elif str(sym) == close_brackets[0][i]:
                close_brackets[1] += 1

        if open_brackets[1] != close_brackets[1]:
            syntax_errors.append(errors["brackets_err"])
