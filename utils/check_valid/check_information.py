

import re



#check email for register
def Check_Email(email):
    print('sdsd'*90)
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    email =email
    if re.fullmatch(regex, email):
       
        return True
    else:
        return False
            
#check phone for register
    
def check_phone(phone):
    phone = phone
    mobile_regex = "^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$"
    if(re.search(mobile_regex, phone)):
       return True

    return False
# #check username for register
def check_username(username):
    if len(username)>=5:
        usernamefilter="=)(*&^%$#@!~/-+|:?><"
        username = username
        if username[0]=='_' or username[0] in usernamefilter:
            return False
        for ch in username:
            if ch in usernamefilter:
                return  False
        return True
    return False



def check_codeposty(codeposty):
    codeposty_regex =re.compile(r"/\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b/gm")
    if re.fullmatch(codeposty_regex,codeposty):
        return True
    return False

