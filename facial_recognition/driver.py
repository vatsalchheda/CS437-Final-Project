# Standard python imports
import time
import sys
import hashlib
import os
from gpiozero import LED

# User Defined RAVN imports
from make_hash import hash_password
from config import passwords
from config import users
from face_req_driver import face_req_seq
from config import emails
from led import led_op
from speech import speech_to_text
from biometric_fingerprint import fingerprint
from config import positions
from config import pos_no, usr_no
from example_enroll import enroll_user
from headshots import take_screenshot
from train_model import retrain_ravn
from send_test_email import send_mail


start_time = time.ctime()

# Open the log file
try:
    f = open("Activity_log.txt", "w")
except Exception as err:
    print('FATAL ERROR ::: ERR 01 ::: Could not create Activity_log')
    sys.exit()

f.write("####################### 3 LOG FILE #######################\n\n")
f.write('\n The smart lock RAVN is turned on ::: ' + str(start_time) +'\n')


# Match the first password to begin authentication.
while True:
    msg01 = 'PLEASE ENTER THE COMMON PASSWORD TO BEGIN 3-WAY AUTHORIZATION'
    msg02 = 'OR ENTER "ESCAPE" TO QUIT'
    print(msg01)
    print(msg02)
    
    f.write('\n' + msg01 +'\n')
    common_password = input()
    if common_password == 'ESCAPE':
        break

    common_password_hash = hash_password(common_password)
    saved_common_password_hash = passwords['common']
    f.write('\n ' + 'The hash of common password entered by the user ::: ' + str(common_password_hash) +'\n')
    f.write('\n ' + 'The hash of common password saved in the system ::: ' + str(saved_common_password_hash) +'\n')
    flag_common = False
    if common_password_hash == saved_common_password_hash:
        flag_common = True
    if flag_common:
        f.write('\n MATCH SUCCESSFUL' +'\n')
        break
    else:
        f.write('\n MATCH FAILED'   +'\n')
        print('PLEASE TRY AGAIN')
        continue

# Starting with facial recognition
f.write('\n ' +  'STEP 1 ::: ATTEMPTING FACIAL RECOGNITION' +'\n')
try:
    f2 = open("Alert_log.txt", "a")
except Exception as err:
    print('FATAL ERROR ::: ERR 02 ::: Could not create Alert_log')
    sys.exit()
try:
    face_detected = face_req_seq()
    print('Face Dectected ::: ' + str(face_detected))
    f.write('\n FACE DETECTED ::: ' + str(face_detected) +'\n')
except Exception as err:
    print('FATAL ERROR ::: ERR 03 ::: Could not run Facial Recognition')
    print('Error message ::: ' + str(err))
    f.write('\n FATAL ERROR ::: ERR 03 ::: Could not run Facial Recognition'   +'\n')
    sys.exit()

print(face_detected, list(users.values()))
if face_detected in list(users.values()):
    f.write('\n FACE Authorized ::: ' + str(face_detected) +'\n')
else:
    f.write('\n INTRUDER ALERT ::: Unknow user tried to unlock RAVN smart lock'   +'\n')
    f2.write('\n Current time ::: ' + str(time.ctime()))
    f2.write('\n Unauthorized Access')
    f2.close()
    f.close()
    try:
        send_mail(1)
    except Exception as err:
        f.write('FATAL ERROR 13 ::: Failed to send email to authorized users.')
        print('FATAL ERROR 13 ::: Failed to send email to authorized users.')
        sys.exit()
    sys.exit()



# switch on the led to display the current status and progress
# led_op('on', 19, 5)
led = LED(19) # Red light
led.on()
f.write('\n First LED turned on. ' + '\n')


# step 2 audio recognition
try:
    text = speech_to_text()
    hashed_text = hash_password(text.lower())
except Exception as err:
    f.write('\n FATAL ERROR ::: ERR 04 ::: Could not run Speech-to-text')
    print('FATAL ERROR ::: ERR 04 ::: Could not run Speech-to-text')
    sys.exit()

usr = ''
usrs = list(users.values())
if face_detected == usrs[0]:
    usr = 'User1'
elif face_detected == usrs[1]:
    usr = 'User2'
else:
    usr = 'User3'
usr_name = users[usr]
print(usr_name)
f.write('\n Authorized user ::: ' + str(usr_name) + ' trying to unlock using their personal password.')
f.write('\n Speech to text (hashed) ::: ' + str(hashed_text))

personal_password = passwords[usr_name]
f.write('\n Users hashed personal password ::: ' + str(personal_password))

if personal_password == hashed_text:
    f.write('\n Personal Password Matched.')
else: 
    f.write('\n Personal Password Mismatched.')
    sys.exit()

led = LED(13) # Yellow light
led.on()
f.write('\n Second LED turned on. ' + '\n')

# STEP 3
# Finger print test, biometric authorization
f.write('\n Attempting Biometric authorization ' + '\n')
print('Please place your finger on the machine when it turns red')
time.sleep(10)
try:
    pos = fingerprint()
except Exception as err:
    f.write('\n FATAL ERROR ::: ERR 05 ::: Could not run biometric authorization')
    print('FATAL ERROR ::: ERR 05 ::: Could not run biometric authorization')
    sys.exit()

if int(pos) == -1:
    f.write('\n Biometric authorization failed')
    print('Biometric authorization failed')
    sys.exit()
elif int(pos) != int(positions[usr_name]):
    f.write('\nBiometric authorization failed ::: User mismatch')
    print('Biometric authorization failed ::: User mismatch')
    sys.exit()
else:
    f.write('\n Biometric authorization successfull')
    print('Biometric authorization successfull')

print("####################### WELCOME " + str(usr_name) + "#######################")
f.write("\n ####################### WELCOME " + str(usr_name) + "#######################")

# Lighting the last LED
led = LED(26) # Green light
led.on()
f.write('\n Final LED turned on. ' + '\n')

print("\n------------>" + str(usr_name) + "Enter 1 to open the RAVN vault, 2 to register a new user, 3 for shared account")
try:
    choice = int(input())
except Exception as err:
    f.write('\n Wrong key entered, please repeat the authorization process')
    print('Wrong key entered, please repeat the authorization process')
    sys.exit()

if choice not in [1, 2, 3]:
    f.write('\n Wrong key entered, please repeat the authorization process')
    print('Wrong key entered, please repeat the authorization process')
    sys.exit()

if choice == 1:
    f.write('\n RAVN Vault is not open, you may now access the contents of the safe.')
    print('RAVN Vault is not open, you may now access the contents of the safe.')
elif choice == 2:
    pass
    # take user name as input
    print('Please enter the name of the new user ::: ')
    new_usr = input().lower()
    # run register fingerprint file
    time.sleep(1)
    try:
        enroll_user()
    except Exception as err:
        f.write('FATAL ERROR 07 ::: Failed to register the fingerprint of the new user.')
        print('FATAL ERROR 07 ::: Failed to register the fingerprint of the new user.')
        sys.exit()
    
    # ass position to config file
    pos_no += 1
    positions[new_usr] = 'User' + str(pos_no)
    f.write('\n USER ' + str(new_usr) + "'s fingerprint has been registered")
    print('\n USER ' + str(new_usr) + "'s fingerprint has been registered")
    
    # mkdir with user name in datasets folder
    try:
        current_script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        dataset_dir = os.path.join(current_script_dir, 'dataset')
        usr_name_dir = os.path.join(dataset_dir, new_usr)
        if not os.path.exists(usr_name_dir):
            os.mkdir(usr_name_dir)
    except Exception as err:
        f.write('FATAL ERROR 08 ::: Failed to make a dataset for the new user.')
        print('FATAL ERROR 08 ::: Failed to make a dataset for the new user.')
        sys.exit()


    # run headhsots.py and instruct user to take 50 photos
    time.sleep(1)
    try:
        take_screenshot(new_usr)
    except Exception as err:
        f.write('FATAL ERROR 09 ::: Failed to click images of the new user.')
        print('FATAL ERROR 09 ::: Failed to click images of the new user.')
        sys.exit()
    print('User screenshots taken')

    # run train.py
    f.write('Training the RAVN face recognition model -- started ::: ' + str(time.ctime()))
    print('Training the RAVN face recognition model --started ::: ' + str(time.ctime()))
    try:
        retrain_ravn()
    except Exception as err:
        f.write('FATAL ERROR 10 ::: Failed to retrain RAVN model.')
        print('FATAL ERROR 10 ::: Failed to retrain RAVN model.')
        sys.exit()
    f.write('Training the RAVN face recognition model -- completed ::: ' + str(time.ctime()))
    print('Training the RAVN face recognition model -- completed ::: ' + str(time.ctime()))

    # add user to config.py
    usr_no += 1
    key = 'User' + str(usr_no)
    users[key] = new_usr
    f.write('\n USER ' + str(new_usr) + "'s fingerprint has been registered")
    print('\n USER ' + str(new_usr) + "'s fingerprint has been registered")
    

    # prompt user for a personal password
    print('Please enter the password of the new user ::: ')
    new_usr_psswd = input()

    # hash the password
    try:
        new_usr_psswd_hashed = hash_password(new_usr_psswd)
    except Exception as err:
        f.write('FATAL ERROR 11 ::: Failed to hash user password.')
        print('FATAL ERROR 11 ::: Failed to hash user password.')
        sys.exit()

    # add hashed password to config.py
    passwords[new_usr] = new_usr_psswd_hashed

    # prompt user for email
    print('Please enter the email of the new user ::: ')
    new_usr_email = input()
    emails[new_usr] = new_usr_email

    # write changes to config file
    try:
        # Save the updated config back to the file
        with open('config.py', 'w') as file:
            file.write("# config file to save passwords\n")
            file.write("# passwords are encrypted for safety\n")
            file.write("# so that looking at the source code doesn't reveal the passwords\n")
            file.write(f"passwords = {passwords}\n")
            file.write(f"usr_no = {usr_no}\n")
            file.write(f"users = {users}\n")
            file.write(f"pos_no = {pos_no}\n")
            file.write(f"positions = {positions}\n")
            file.write(f"emails = {emails}\n")
    except Exception as err:
        f.write('FATAL ERROR 12 ::: Failed to write changes to config file.')
        print('FATAL ERROR 12 ::: Failed to write changes to config file.')
        sys.exit()
elif choice == 3:
    print('Trying to access the shared lock')
    print('Enter the name of the user you have a joint account with ::: ')
    jname = input().lower()
    print('Please place your finger on the machine when it turns red')
    time.sleep(10)
    try:
        pos = fingerprint()
    except Exception as err:
        f.write('\n FATAL ERROR ::: ERR 05 ::: Could not run biometric authorization')
        print('FATAL ERROR ::: ERR 05 ::: Could not run biometric authorization')
        sys.exit()

    if int(pos) == -1:
        f.write('\n Biometric authorization failed')
        print('Biometric authorization failed')
        sys.exit()
    elif int(pos) != int(positions[jname]):
        f.write('\nBiometric authorization failed ::: User mismatch')
        print('Biometric authorization failed ::: User mismatch')
        sys.exit()
    else:
        f.write('\n Biometric authorization successfull')
        print('Biometric authorization successfull')


print('Plese press "SECURE" to close and lock the vault')
inp = ""
while inp != "SECURE":
    inp = input()

for _ in range(5): print('Securing the RAVN system ..');  time.sleep(1)
f.write('\n RAVN has been secured and locked.')
f.write('\n RAVN closing time ::: ' + str(time.ctime()))
f.write("\n ####################### END #######################\n")
f.close()

# Send email about registeration of new user
try:
    send_mail(2, usr_name, new_usr)
except Exception as err:
    print('FATAL ERROR 13 ::: Failed to send email to authorized users.')
    sys.exit()

print('Execution successfull.')