import requests #importing the requried libraries
import hashlib
import sys

#Start seeing the code from below to understand
def request_api_data(query_char):#it checks and gives responce to the console whether the data is found on the hash table or not
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching {res.status_code}, check api')
    return res
def get_password_leaks(hashes,hashes_to_check):
    hashes = (lines.split(':') for lines in hashes.text.splitlines())
    for h,count in hashes:
       if h == hashes_to_check:
           return count
    return 0


def pwned_api_check(password): #it converts the password to sha1 hash then forwards the first 5 hex code to request_api_data function
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    first5 , tail = sha1password[:5],sha1password[5:]
    responce = request_api_data(first5)
    return get_password_leaks(responce,tail) #it searchs the tail value to the responce and find the final data

def main(args):
    for password in args: #it seperates the aruguments and pass to the api function
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times..you should change it.') #if the password is not secure
        else:
            print(f'{password} was not found you are good to go!.') #if the password is secure
    return 'done!'
if __name__ == '__main__':#This function is giving the arguments which were taken from a .txt file to the main function
    f = open(sys.argv[1])
    r = f.read().split()
    main(r)
