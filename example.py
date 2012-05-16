from blowfish import Blowfisher

if __name__ == '__main__':
    bf = Blowfisher('really_good_secret')
    token = bf.encode('some_param=some_value,another_param=val|val2|val3')
    string = bf.decode(token)
    print token
    print string
