import sys

cookiestring=input('Please input your cookie: ')
cookie=cookiestring.replace('"','\\"')
print('Convertion complete, now you can put the following string to your config: \n')
print(cookie)
input('Press ENTER to contiune...')