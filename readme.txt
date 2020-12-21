Information:

    This code was made to find specific errors in a sentence that has always a structure

    This structure has two parts IE_NG and CPR which both have some rules what they should or shoudn't contain

    The official explanation is inside 'official.txt' as I would really suck in that


    All the functions are inside 'func.py' along with some brief explanation and its separated on major parts such as
    the code to find errors in phrase, IE_NG, CPR ..., function trouble_killer() connects all the pieces and returns
    all syntax errors which is later called from within 'main.py' 

    'main.py' also has 2 commented code blocks to check data in data.xlsx which contains two sheets(one with mostly correct examples and 
    another with wrong examples)




Instructions: (terminal commands used on Ubuntu, for windows might differ)

    1. its recommended to create a new environment using Python3        "  python -m venv env   "
    2. activate the created env                                         "  source env/bin/activate   "
    3. install all the libraries from requirements.txt                  "  pip install -r requirements.txt  "
    4. now you should be good to go :) try to launch                    "  python main.py  " 
       and you should see result(found errors)

    ['There is a missing open/closing ( ) or [ ] or { }', "You didn't put any digits or letter 'g' as glossary"]

    5. you are free to manipulate with code and change as you wish


PS: please keep all these files in the same directory
PS2: sorry for the english inside 'official.txt', its not my doing