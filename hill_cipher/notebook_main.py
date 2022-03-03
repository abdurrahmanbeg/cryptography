import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import encrypt, decrypt


class Notepad(tk.Tk):
    global keyConf, blockConf, key, block
    key = 0
    block = 0
    blockConf = False
    keyConf = False
    ct_text = ''
    pt_text = ''

    def __init__(self):
        super().__init__()
        self.title("Python Notepad - Hill Cipher by AR Beg")
        self.menubar = tk.Menu(self, tearoff=False)
        self['menu'] = self.menubar
        self.menu_file = tk.Menu(self.menubar, tearoff=False)
        self.menu_encrypt = tk.Menu(self.menubar, tearoff=False)
        self.menu_decrypt = tk.Menu(self.menubar, tearoff=False)
        self.menu_key = tk.Menu(self.menubar, tearoff = False)
        self.menu_block = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_encrypt, label='Encrypt')
        self.menubar.add_cascade(menu=self.menu_decrypt, label='Decrypt')
        self.menubar.add_cascade(menu=self.menu_key, label='Key')
        self.menubar.add_cascade(menu=self.menu_block, label='Block Size')
        self.menu_file.add_command(label='Exit', command=self.destroy)
        self.menu_encrypt.add_command(label='By file ... ', command=self.open_file)
        self.menu_encrypt.add_command(label='By text input', command=self.insert_text)
        self.menu_encrypt.add_command(label='Encrypt', command=self.encrypt)
        self.menu_decrypt.add_command(label='By file ... ', command=self.open_file)
        self.menu_decrypt.add_command(label='By text input', command=self.insert_text)
        self.menu_decrypt.add_command(label='Decrypt', command=self.decrypt)
        self.menu_key.add_command(label='Configure ... ', command=self.key_input)
        self.menu_block.add_command(label='Configure ... ', command=self.block_input)
        self.info_var = tk.StringVar()
        self.info_var.set('> Please select input source from the menu <')
        self.info_bar = tk.Label(self, textvariable=self.info_var, bg='#333', fg='white')
        self.info_bar.configure(anchor=tk.W, font='-size -14 -weight bold', padx=5, pady=5)
        self.text = ScrolledText(self, font='-size -16')
        self.info_bar.pack(side=tk.TOP, fill=tk.X)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.file = None


    def open_file(self, event=None):
        """Open file and update infobar"""
        file = filedialog.askopenfilename(title='Open', filetypes=(('Text', '*.txt'), ('All Files', '*.*')))
        if file:
            self.file = pathlib.Path(file)
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, self.file.read_text())
            self.info_var.set(self.file.absolute())

    def insert_text(self, event=None):
        self.file = None
        self.text.delete('1.0', tk.END)
        userinput = askstring('Enter PT', 'Plain Text:')
        self.text.insert(tk.END, userinput + "\n")

    def key_input(self, event=None):
        global keyConf, key
        print("Key input configuration selected")
        key = askstring('Key', 'Please enter the key in characters: (e.g. JHLNEHFGCVOJDXVI)')
        try:
            if blockConf:
                key = encrypt.convertToInt(key)
                key = encrypt.convertToMatrix(key, block)
                print("Key: " + str(key))
                if decrypt.checkInvert(key):
                    #self.text.insert(tk.END, "Key check: Invertible\n")
                    keyConf = True
                else:
                    showinfo('Invalid', 'Key is not invertible, please re-enter')
                    #self.text.insert(tk.END, "Key check: NOT invertible\n")
                    keyConf = False
            else:
                showinfo('Alert', 'Please enter a block size first!')
        except:
            showinfo('Invalid', 'Please enter a valid key')
            keyConf = False
    def block_input(self, event=None):
        global blockConf, block
        print("Block size configuration selected")
        block = askstring('Block size', 'Please enter the block size:')
        try:
            block = int(block)
            blockConf = True
        except:
            showinfo('Error', 'Please enter an integer')
            blockConf = False

    def encrypt(self, event=None):
        global ct_text
        plaintext = self.text.get('1.0',tk.END)
        plaintext = plaintext.strip()
        print("Key: " + str(keyConf) + "| Block: " + str(blockConf) + "| PT: " + plaintext + "| Len " + str(len(plaintext)) )
        if blockConf & keyConf:
            plaintext = plaintext.replace('\n', '')
            plaintext = plaintext.replace(' ', '')
            plaintext = plaintext.upper()
            print("Encrypt PT: " + str(plaintext) + "\nKey: " + str(key) + "\nBlock size: " + str(block))
            self.text.insert(tk.END, "Encrypting ... \n")
            ct_text = encrypt.encrypt(plaintext, key,block)
            self.text.insert(tk.END, "Cipher text: " + str(ct_text) + "\n")
            ct_text = "".join(ct_text)
            self.text.insert(tk.END, "--> From P text: " + plaintext + "| Length: " + str(len(plaintext))+"\n")
            self.text.insert(tk.END, "--> Cipher text: " + ct_text + "| Length: " + str(len(ct_text))+"\n")
            self.compare(ct_text, plaintext)
        elif blockConf:
            showinfo('Error', 'Please configure key')
        elif keyConf:
            showinfo('Error', 'Please configure block size')
        else:
            showinfo('Error', 'Please configure key and block size')

    def decrypt(self, event=None):
        global pt_text
        print("Decrypt " + self.text.get('1.0', tk.END))
        if blockConf & keyConf:
            print("CT: " + ct_text + "\nKey: " + str(key) + "\nBlock size: " + str(block))
            self.text.insert(tk.END, "Decrypting ... \n")
            pt_text = decrypt.decrypt(ct_text,key,block)
            self.text.insert(tk.END, "Plain text: " + str(pt_text) + "\n")
            pt_text = "".join(pt_text).removesuffix('Z')
            self.text.insert(tk.END, "Plain text: " + pt_text + "\n")
            self.text.insert(tk.END, "--> From C text: " + ct_text + "| Length: " + str(len(ct_text)) + "\n")
            self.text.insert(tk.END, "--> Plain text: " + pt_text + "| Length: " + str(len(pt_text)) + "\n")
            self.compare(ct_text, pt_text)
        elif blockConf:
            showinfo('Error', 'Please configure key')
        elif keyConf:
            showinfo('Error', 'Please configure block size')
        else:
            showinfo('Error', 'Please configure key and block size')

    def compare (self, text1, text2):
            if text1 == text2:
                self.text.insert(tk.END,"The plain text and cipher text are equal.\n")
            else:
                self.text.insert(tk.END, "The plain text and cipher text are not equal.\n")

if __name__ == '__main__':
    app = Notepad()
    app.mainloop()