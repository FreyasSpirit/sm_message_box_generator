# Huge thank you to sixfold (plof27) for helping with this!

# In its current state, this will turn all unique large message boxes into
# the text entered in MORPH_STR, etc.  If you want to modify ammo message boxes
# or otherwise need help, feel free to message us on discord.

# Thank you to PJboy's disassembly for the format of the message box data
# http://patrickjohnston.org/bank/85

import sys

FUNCTION_PTR_TABLE = """
lorom

org $85869B

;;; $869B: Message definitions ;;;
;{
; Summary of ASM routines:
;     $825A: Write large message box tilemap
;     $8289: Write small message box tilemap

;     $83C5: Draw shoot button and set up PPU for large message box
;     $83CC: Draw run button and set up PPU for large message box
;     $8436: Set up PPU for large message box
;     $8441: Set up PPU for small message box

; In addition to using the correct ASM routines, the message tilemap will have to b
;e the right size;
; *however*, the size of the message tilemap is calculated by subtracting the messa
;ge tilemap pointer from *the next entry's message tilemap pointer*.
; This is why there are terminator entries (1Bh and 1Dh)

;                        ___________ Modify message box (e.g. draw special button)
;and set up PPU
;                       |     ______ Draw initial message box tilemap
;                       |    |     _ Message tilemap
;                       |    |    |
dw     $8436,$8289,$96C0 ; 1: Energy tank
dw     $83C5,$825A,$9700 ; 2: Missile
dw     $83C5,$825A,$9800 ; 3: Super missile
dw     $83C5,$825A,$9900; 4: Power bomb
dw     $841D,$825A,$9A00; 5: Grappling beam
dw     $841D,$825A,$9B00 ; 6: X-ray scope
dw     $841D,$825A,$9C00 ; 7: Varia suit
dw     $841D,$825A,$9D00 ; 8: Spring ball
dw     $841D,$825A,$9E00 ; 9: Morphing ball
dw     $841D,$825A,$9F00 ; Ah: Screw attack
dw     $841D,$825A,$A000 ; Bh: Hi-jump boots
dw     $841D,$825A,$A100 ; Ch: Space jump
dw     $841D,$825A,$A200 ; Dh: Speed booster
dw     $841D,$825A,$A300 ; Eh: Charge beam
dw     $841D,$825A,$A400 ; Fh: Ice beam
dw     $841D,$825A,$A500 ; 10h: Wave beam
dw     $841D,$825A,$A600 ; 11h: Spazer
dw     $841D,$825A,$A700 ; 12h: Plasma beam
dw     $841D,$825A,$A800 ; 13h: Bomb
dw     $8436,$8289,$A900 ; 14h: Map data access completed
dw     $8436,$8289,$A9C0 ; 15h: Energy recharge completed
dw     $8436,$8289,$AA80 ; 16h: Missile reload completed
dw     $8441,$8289,$AB40 ; 17h: Would you like to save?
dw     $8436,$8289,$AC40 ; 18h: Save completed
dw     $8436,$8289,$AC80 ; 19h: Reserve tank
dw     $841D,$8289,$ACC0 ; 1Ah: Gravity suit
dw     $841D,$8289,$ADC0 ; 1Ah: Terminator
dw     $8441,$8289,$AB40 ; 1Ch: Would you like to save? (Used by gunship)
dw     $8436,$8289,$AC40 ; 1Dh: Terminator. (Save completed, unused)
"""

ETANK_MISSILE_SUPER_PB = """
; '    ENERGY TANK    '
dw $000E, $000E, $000E, $000E, $000E, $000E, $284E, $284E, $284E, $284E, $28E4, $28ED, $28E4, $28F1, $28E6, $28F8, $284E, $28F3, $28E0, $28ED, $28EA, $284E, $284E, $284E, $284E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '          MISSILE         '
; '                          '
; '         |miss|                 '
; '  select |ile | & press the A button.  '
dw $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $28EC, $28E8, $28F2, $28F2, $28E8, $28EB, $28E4, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $304B, $3049, $704B, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $28B9, $28BA, $28BB, $284E, $304C, $304A, $704C, $284E, $28C8, $284E, $28B0, $28B1, $28B2, $28C0, $28C1, $28D1, $28E0, $28D3, $28B5, $28B6, $28B7, $28CB, $284E, $284E, $000E, $000E, $000E

; '      SUPER MISSILE       '
; '                          '
; '         [sup                 '
; '   select er] & press the B button.  '
dw $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $28F2, $28F4, $28EF, $28E4, $28F1, $284E, $28EC, $28E8, $28F2, $28F2, $28E8, $28EB, $28E4, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $3034, $7034, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $28B9, $28BA, $28BB, $284E, $3035, $7035, $284E, $28C8, $284E, $28B0, $28B1, $28B2, $28C0, $28C1, $28D1, $3CE1, $28D3, $28B5, $28B6, $28B7, $28CB, $284E, $284E, $000E, $000E, $000E

; '        POWER BOMB        '
; '                          '
; '       [pow                   '
; ' select er] & set it with the R button. '
dw $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $28EF, $28EE, $28F6, $28E4, $28F1, $284E, $28E1, $28EE, $28EC, $28E1, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $284E, $284E, $284E, $284E, $3036, $7036, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $284E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $284E, $28B9, $28BA, $28BB, $284E, $3037, $7037, $284E, $28C8, $284E, $28C5, $28C6, $28C7, $284E, $28BE, $28BF, $28C0, $28C1, $28D1, $38F1, $28D3, $28B5, $28B6, $28B7, $28CB, $284E, $000E, $000E, $000E
"""

BETWEEN_BOMBS_AND_GRAVITY = """
; '  MAP DATA ACCESS  '
; '                   '
; '    COMPLETED.     '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3CEC, $3CE0, $3CEF, $3C4E, $3CE3, $3CE0, $3CF3, $3CE0, $3C4E, $3CE0, $3CE2, $3CE2, $3CE4, $3CF2, $3CF2, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3C4E, $3C4E, $3CE2, $3CEE, $3CEC, $3CEF, $3CEB, $3CE4, $3CF3, $3CE4, $3CE3, $3CFA, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '  ENERGY RECHARGE  '
; '                   '
; '    COMPLETED.     '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3CE4, $3CED, $3CE4, $3CF1, $3CE6, $3CF8, $3C4E, $3CF1, $3CE4, $3CE2, $3CE7, $3CE0, $3CF1, $3CE6, $3CE4, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3C4E, $3C4E, $3CE2, $3CEE, $3CEC, $3CEF, $3CEB, $3CE4, $3CF3, $3CE4, $3CE3, $3CFA, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '  MISSILE RELOAD   '
; '                   '
; '    COMPLETED.     '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3CEC, $3CE8, $3CF2, $3CF2, $3CE8, $3CEB, $3CE4, $3C4E, $3CF1, $3CE4, $3CEB, $3CEE, $3CE0, $3CE3, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $384E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $384E, $384E, $3CE2, $3CEE, $3CEC, $3CEF, $3CEB, $3CE4, $3CF3, $3CE4, $3CE3, $3CFA, $384E, $384E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '  WOULD YOU LIKE   '
; '  TO SAVE?         '
; '                   '
; '  =>YES      NO    '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3CF6, $3CEE, $3CF4, $3CEB, $3CE3, $3C4E, $3CF8, $3CEE, $3CF4, $3C4E, $3CEB, $3CE8, $3CEA, $3CE4, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3CF3, $3CEE, $3C4E, $3CF2, $3CE0, $3CF5, $3CE4, $3CFE, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
dw                        $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $38CC, $38CD, $3CF8, $3CE4, $3CF2, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $2CED, $2CEE, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '  SAVE COMPLETED.  '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3CF2, $3CE0, $3CF5, $3CE4, $3C4E, $3CE2, $3CEE, $3CEC, $3CEF, $3CEB, $3CE4, $3CF3, $3CE4, $3CE3, $3CFA, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '   RESERVE TANK    '
dw $000E, $000E, $000E, $000E, $000E, $000E, $284E, $284E, $284E, $28F1, $28E4, $28F2, $28E4, $28F1, $28F5, $28E4, $284E, $28F3, $28E0, $28ED, $28EA, $284E, $284E, $284E, $284E, $000E, $000E, $000E, $000E, $000E, $000E, $000E
"""

AFTER_GRAVITY = """
; Terminator
dw $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000 

; '  =>YES      NO    ' (unused)
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $38CC, $38CD, $3CF8, $3CE4, $3CF2, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $2CED, $2CEE, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '  =>YES      NO    '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $38CC, $38CD, $3CF8, $3CE4, $3CF2, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $3C4E, $2CED, $2CEE, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

; '    YES    =>NO    '
dw $000E, $000E, $000E, $000E, $000E, $000E, $3C4E, $3C4E, $3C4E, $3C4E, $2CF8, $2CE4, $2CF2, $3C4E, $3C4E, $3C4E, $3C4E, $38CC, $38CD, $3CED, $3CEE, $3C4E, $3C4E, $3C4E, $3C4E, $000E, $000E, $000E, $000E, $000E, $000E, $000E

dw 0000
"""

# *'s turn into the blank spaces on either side of the message box
MORPH_STR = """
***                          ***
***            orb           ***
***                          ***
***                          ***
"""

BOMBS_STR = """
***                          ***
***     I bet you'd like     ***
***    to have more bombs    ***
***                          ***
"""

CHARGE_STR = """
***                          ***
***    It's dangerous to     ***
***   go alone! Take this.   ***
***                          ***
"""

SPAZER_STR = """
***                          ***
***    Kraid hates certain   ***
***      types of dances     ***
***                          ***
"""

VARIA_STR = """
***                          ***
***       Show this to       ***
***         Mx Croc          ***
***                          ***
"""

HJB_STR = """
***                          ***
***     Meet king cac at     ***
***       the mountain       ***
***                          ***
"""

SPEED_STR = """
***                          ***
***      Go up, up the       ***
***       tower ahead        ***
***                          ***
"""

WAVE_STR = """
***                          ***
***    Aim at the eye of     ***
***    the ghost elephant    ***
***                          ***
"""

GRAPPLE_STR = """
***     Secret is in the     ***
***       chozo at the       ***
***         dead end         ***
***                          ***
"""

GRAVITY_STR = """
***     Go North, West,      ***
***   South, West to find    ***
***     Botwoon's hitbox     ***
***                          ***
"""

SPACE_JUMP_STR = """
***                          ***
***     Show this to the     ***
***          chozo           ***
***                          ***
"""

SPRINGBALL_STR = """
***                          ***
***   Master using it and    ***
***     you can have it      ***
***                          ***
"""

PLASMA_STR = """
***                          ***
***         Power Up         ***
***        With Pride!       ***
***                          ***
"""

ICE_STR = """
***                          ***
***     Lava pool is an      ***
***    entrance to death     ***
***                          ***
"""

SCREW_STR = """
***                          ***
***   Buy medicine before    ***
***         you pogo         ***
***                          ***
"""

XRAY_STR = """
***   Secret power is said   ***
***   to be in the spazer    ***
***           beam           ***
***                          ***
"""

ALL_STR_ARRAY = [
GRAPPLE_STR,
XRAY_STR,
VARIA_STR,
SPRINGBALL_STR,
MORPH_STR,
SCREW_STR,
HJB_STR,
SPACE_JUMP_STR,
SPEED_STR,
CHARGE_STR,
ICE_STR,
WAVE_STR,
SPAZER_STR,
PLASMA_STR,
BOMBS_STR,
GRAVITY_STR
]


def convert(string):
  string = string.upper()
  out = list()
  for char in string:
    if (char == ' '):
      out.append('$284E')
    elif (char == '*'):
      out.append('$000E')
    elif (char == '.'):
      out.append('$28FA')
    elif (char == ','):
      out.append('$28FB')
    elif (char == '\''):
      out.append('$28FD')
    elif (char == '!'):
      out.append('$28FF')
    elif (char == '\n'):
      pass
    else:
      out.append('$' + str(hex(ord(char) + 0x28E0 - 0x41))[2:])
  return out

if __name__ == "__main__":
  # strip newlines
  for idx, string in enumerate(ALL_STR_ARRAY):
    ALL_STR_ARRAY[idx] = ALL_STR_ARRAY[idx].replace('\n', '')

  # ensure all strings are 128 characters long after newlines are removed
  for idx, string in enumerate(ALL_STR_ARRAY):
    length = len(string)
    if length != 128:
      print "Error: string not 128 characters long.  Actual length: " + str(length) + 'index: ' + str(idx)
      print string
      sys.exit(1)
  print FUNCTION_PTR_TABLE
  print 'org $8596C0'  # any address in this range will work, we choose an even number ending in 00
  print ETANK_MISSILE_SUPER_PB
  # Don't print gravity because it needs to be later
  for string in ALL_STR_ARRAY[:-1]:
    print 'dw ' + ', '.join(convert(string)) + ' ; ' + string
  print BETWEEN_BOMBS_AND_GRAVITY
  print 'dw ' + ', '.join(convert(ALL_STR_ARRAY[-1])) + ' ; ' + string  # print gravity
  print AFTER_GRAVITY
