This code was made to find some specific errors in a sentence that has always some structure

This structure has two parts IE_NG and CPR which both have some rules what they should or shoudn't contain

The official explanation is inside 'official.txt' as I would really suck in that


All the functions are inside 'func.py' along with some brief explanation and its separated on some major parts such as
the code to find errors in phrase, IE_NG, CPR ..., function trouble_killer() connects all the pieces and returns
all syntax errors which is later called from 'main.py' 

'main.py' also has some commented codes to check data in data.xlsx which contains two sheets(one with correct examples and 
another with wrong examples)




You are free to use these codes however and whenever you wish.



HOW TO SET IT UP:
1. its recommended to create a new environment using Python3 "  python -m venv env   "
2. activate the created env  "  source env/bin/activate   "
3. install all the libraries from requirements.txt  " pip install -r requirements.txt  "
4. now you should be good to go :) try to launch  "  python main.py  " and you should see 

['There is a missing open/closing ( ) or [ ] or { }', "You didn't put any digits or letter 'g' as glossary"]

as result(found errors)

5. you are free to manipulate with code and change as you wish


PS: please keep all these files in the same directory
PS2: sorry for the english inside 'official.txt', its not my work