import requests
import hashlib
import sys


def request_api_data(quere_char):
    url = "https://api.pwnedpasswords.com/range/" + quere_char
    res = requests.get(url)
    print(res)
    if res.status_code != 200:
        raise RuntimeError(f"Error Fetching: {res.status_code} , check the api and try again")
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # check password if it exist in api response
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return get_password_leaks_count(response, tail)


def main(argv):
    for password in argv:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should change your password')
        else:
            print(f'{password} was NOT found. carry on! it is a great password')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# To use the project Write: python3 checkmypass.py yourPassword
# in the the terminal
