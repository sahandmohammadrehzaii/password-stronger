

import string
import getpass


def check_password_strength():
   password = getpass.getpass('لطفا پسوورد تان را وارد کنید: ')
   strength = 0
   remarks = ''
   lower_count = upper_count = num_count = wspace_count = special_count = 0

   for char in list(password):
       if char in string.ascii_lowercase:
           lower_count += 1
       elif char in string.ascii_uppercase:
           upper_count += 1
       elif char in string.digits:
           num_count += 1
       elif char == ' ':
           wspace_count += 1
       else:
           special_count += 1

   if lower_count >= 1:
       strength += 1
   if upper_count >= 1:
       strength += 1
   if num_count >= 1:
       strength += 1
   if wspace_count >= 1:
       strength += 1
   if special_count >= 1:
       strength += 1

   if strength == 1:
       remarks = ('این رمز عبور بسیار بدی است.'
           ' هر چه زودتر آن را تغییر دهید.')
   elif strength == 2:
       remarks = ('این یک رمز عبور ضعیف است.'
           ' شما باید از رمز عبور سخت تری استفاده کنید.')
   elif strength == 3:
       remarks = 'رمز عبور شما مشکلی ندارد، اما می توان آن را بهبود بخشید.'
   elif strength == 4:
       remarks = ('حدس زدن رمز عبور شما سخت است.'
           ' اما شما می توانید آن را حتی امن تر کنید.')
   elif strength == 5:
       remarks = ('حالا که یک رمز عبور قوی است!!!'
           ' هکرها شانسی برای حدس زدن کلمه عبور ندارند!!!')

   print('رمز عبور شما دارد:-')
   print(f'{lower_count} حروف کوچک')
   print(f'{upper_count} حروف بزرگ')
   print(f'{num_count} ارقام')
   print(f'{wspace_count} فضاهای خالی')
   print(f'{special_count} special characters')
   print(f'امتیاز رمز عبور: {strength / 5}')
   print(f'ملاحظات: {remarks}')


def check_pwd(another_pw=False):
   valid = False
   if another_pw:
       choice = input(
           'آیا می خواهید قدرت رمز عبور دیگری را بررسی کنید (y/n) : ')
   else:
       choice = input(
           'آیا می خواهید قدرت رمز عبور خود را بررسی کنید (y/n) : ')

   while not valid:
       if choice.lower() == 'y':
           return True
       elif choice.lower() == 'n':
           print('شما از برنامه خارج شدید')
           return False
       else:
           print('ورودی نامعتبر است...لطفا دوباره امتحان کنید. \n')


if __name__ == '__main__':
   print('===== به شناساگر سید سهیل موسوی خوش آمدید =====')
   check_pw = check_pwd()
   while check_pw:
       check_password_strength()
       check_pw = check_pwd(True)