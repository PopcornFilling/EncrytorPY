# import things we need
from getpass import getpass
from termcolor import cprint
import os 
from Crypto.Cipher import AES 
from Crypto.Hash import SHA256
from Crypto import Random  
import time

# Encrytor side
def encrypt(key, filename):
    chunksize = 64*1024 
    outputFile = "(BLOCKED)" + filename 
    filesize = str(os.path.getsize(filename)).zfill(16) 
    IV = Random.new().read(16) 

    encryptor = AES.new(key, AES.MODE_CBC, IV) 
    
    with open(filename, 'rb') as infile: 
        with open(outputFile, 'wb') as outfile: 
            outfile.write(filesize.encode('utf-8')) 

            while True: 
                chunk = infile.read(chunksize) 

                if len(chunk) == 0: 
                    break 
                elif len(chunk) % 16 != 0: 
                    chunk += b' ' * (16 - (len(chunk) % 16)) 

                outfile.write(encryptor.encrypt(chunk)) 
                 

# Decryptor side
def  decrypt(key, filename): 
    chunksize = 64*1024
    outputFile = filename[11:]

    with open(filename, 'rb') as infile: 
        filesize = int(infile.read(16)) 
        IV = infile.read(16) 
        
        decrytor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile: 
            while True: 
                chunk = infile.read(chunksize) 

                if len(chunk) == 0: 
                    break
                outfile.write(decrytor.decryt(chunk)) 
            outfile.truncate(filesize) 

# the Key
def GETKEY(password): 
    hasher = SHA256.new(password.encode('utf-8')) 
    return hasher.digest() 

# Terminal UI
def mainScreen():
    os.system('clear')
    cprint("""	
	 /$$$$$$$$                                           /$$                        
	| $$_____/                                          | $$                        
	| $$       /$$$$$$$   /$$$$$$$  /$$$$$$  /$$   /$$ /$$$$$$    /$$$$$$   /$$$$$$ 
	| $$$$$   | $$__  $$ /$$_____/ /$$__  $$| $$  | $$|_  $$_/   /$$__  $$ /$$__  $$
	| $$__/   | $$  \ $$| $$      | $$  \__/| $$  | $$  | $$    | $$  \ $$| $$  \__/
	| $$      | $$  | $$| $$      | $$      | $$  | $$  | $$ /$$| $$  | $$| $$      
	| $$$$$$$$| $$  | $$|  $$$$$$$| $$      |  $$$$$$$  |  $$$$/|  $$$$$$/| $$      
	|________/|__/  |__/ \_______/|__/       \____  $$   \___/   \______/ |__/      
                                        	/$$  | $$                              
                                       	       |  $$$$$$/                                    
                                                \______/                                            
                                              

                                        Version :: 0.00 
                                      Made by linux-fisher
                                                                         """, 'green' , attrs=['bold'])  
    print('    Choose Option \n')
    cprint('        1 - Encrypt' , 'red')
    cprint('        2 - Decrypt', 'red')  
    print("\n")
    mod = input("> What would you like to do... ")
    if mod in ["Encrypt", "encrypt", "1"]:
        filename = input('The file you want to Encrypt: ') 
        password = getpass("Pass: ") 
        encrypt(GETKEY(password), filename)
        time.sleep(0.5) 
        print("\n")
        cprint("DONE", 'green') 
    elif mod in ["Decrypt", "decrypt", "2"]: 
        filename = input('Pick a file you want to Decrypt: ')
        password = getpass('Password: ') 
        time.sleep(1)
        decrypt(GETKEY(password), filename) 
        cprint("DONE", 'green') 
    else: 
        print("No options Selected. Clearing... ") 
        time.sleep(0.3) 

if __name__ == '__main__': 
    mainScreen()
