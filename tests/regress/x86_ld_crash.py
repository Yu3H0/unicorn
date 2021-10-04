from unicorn import *
from unicorn.x86_const import *
from capstone import *

# extract from ld.so
shellcode = [0x55, 0x89, 0xE5, 0x57, 0x56, 0x53, 0xE8, 0xE0, 0x9F, 0x01, 0x00, 0x81, 0xC3, 0xF5, 0x57, 0x02, 0x00, 0x83, 0xEC, 0x3C, 0x0F, 0x31, 0x89, 0x93, 0xE4, 0xF8, 0xFF, 0xFF, 0x8D, 0x93, 0x34, 0xFF, 0xFF, 0xFF, 0x89, 0x83, 0xE0, 0xF8, 0xFF, 0xFF, 0x8B, 0x83, 0x34, 0xFF, 0xFF, 0xFF, 0x89, 0xD6, 0x2B, 0xB3, 0x00, 0x00, 0x00, 0x00, 0x89, 0x93, 0x60, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x89, 0xB3, 0x58, 0x05, 0x00, 0x00, 0x74, 0x5A, 0xBF, 0xFF, 0xFF, 0xFF, 0x6F, 0xEB, 0x1C, 0x8D, 0x76, 0x00, 0xB9, 0x21, 0x00, 0x00, 0x70, 0x29, 0xC1, 0x89, 0xC8, 0x89, 0x94, 0x83, 0x78, 0x05, 0x00, 0x00, 0x83, 0xC2, 0x08, 0x8B, 0x02, 0x85, 0xC0, 0x74, 0x37, 0x83, 0xF8, 0x21, 0x76, 0xEB, 0x89, 0xF9, 0x29, 0xC1, 0x83, 0xF9, 0x0F, 0x76, 0xD9, 0x8D, 0x0C, 0x00, 0xD1, 0xF9, 0x83, 0xF9, 0xFC, 0x0F, 0x86, 0xDB, 0x02, 0x00, 0x00, 0xF7, 0xD1, 0x89, 0x94, 0x8B, 0x40, 0x06, 0x00, 0x00, 0x83, 0xC2, 0x08, 0x8B, 0x02, 0x85, 0xC0, 0x75, 0xD2, 0x89, 0xF6, 0x8D, 0xBC, 0x27, 0x00, 0x00, 0x00, 0x00, 0x85, 0xF6, 0x74, 0x68, 0x8B, 0x83, 0x88, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0x84, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0x8C, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0x90, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0xBC, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0xD4, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0x3C, 0x06, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x83, 0xA4, 0x06, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x03, 0x01, 0x70, 0x04, 0x8B, 0x93, 0xC8, 0x05, 0x00, 0x00, 0x85, 0xD2, 0x74, 0x0A, 0x83, 0x7A, 0x04, 0x11, 0x0F, 0x85, 0x24, 0x04, 0x00, 0x00, 0x8B, 0x83, 0xBC, 0x05, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x10, 0x8B, 0x8B, 0xC4, 0x05, 0x00, 0x00, 0x83, 0x79, 0x04, 0x08, 0x0F, 0x85, 0xEB, 0x03, 0x00, 0x00, 0x8B, 0x8B, 0x10, 0x06, 0x00, 0x00, 0x85, 0xC9, 0x74, 0x0D, 0xF7, 0x41, 0x04, 0xFE, 0xFF, 0xFF, 0xFF, 0x0F, 0x85, 0xB5, 0x03, 0x00, 0x00, 0x8B, 0x8B, 0xF0, 0x05, 0x00, 0x00, 0x85, 0xC9, 0x74, 0x0D, 0xF7, 0x41, 0x04, 0xF7, 0xFF, 0xFF, 0xFF, 0x0F, 0x85, 0x7F, 0x03, 0x00, 0x00, 0x8B, 0x8B, 0xEC, 0x05, 0x00, 0x00, 0x85, 0xC9, 0x0F, 0x85, 0x52, 0x03, 0x00, 0x00, 0x8B, 0xBB, 0xB4, 0x05, 0x00, 0x00, 0x85, 0xFF, 0x0F, 0x85, 0x25, 0x03, 0x00, 0x00, 0x85, 0xF6, 0x0F, 0x85, 0xA4, 0x00, 0x00, 0x00, 0x8B, 0x8B, 0x74, 0x06, 0x00, 0x00, 0x85, 0xC9, 0x0F, 0x84, 0x96, 0x00, 0x00, 0x00, 0x8D, 0xB3, 0x58, 0x05, 0x00, 0x00, 0x83, 0xEC, 0x0C, 0x80, 0x8B, 0xEC, 0x06, 0x00, 0x00, 0x04, 0x56, 0xE8, 0x00, 0x95, 0x00, 0x00, 0x8D, 0x83, 0x00, 0x90, 0xFD, 0xFF, 0x89, 0xB3, 0x6C, 0x05, 0x00, 0x00, 0x89, 0x83, 0x04, 0x07, 0x00, 0x00, 0x8D, 0x83, 0x38, 0x09, 0x00, 0x00, 0x89, 0x83, 0x08, 0x07, 0x00, 0x00, 0x8D, 0x83, 0xFB, 0x47, 0xFF, 0xFF, 0x89, 0x83, 0x0C, 0x07, 0x00, 0x00, 0x0F, 0x31, 0x89, 0x83, 0x40, 0x05, 0x00, 0x00, 0x89, 0x93, 0x44, 0x05, 0x00, 0x00, 0x58, 0x8D, 0x83, 0x30, 0xAE, 0xFD, 0xFF, 0x89, 0xAB, 0x2C, 0xFF, 0xFF, 0xFF, 0x5A, 0x50, 0xFF, 0x75, 0x08, 0xE8, 0x81, 0x61, 0x01, 0x00, 0x89, 0xC6, 0x0F, 0x31, 0x2B, 0x83, 0xE0, 0xF8, 0xFF, 0xFF, 0x1B, 0x93, 0xE4, 0xF8, 0xFF, 0xFF, 0x83, 0xC4, 0x10, 0xF6, 0x83, 0x00, 0xF9, 0xFF, 0xFF, 0x80, 0x89, 0x45, 0xE0, 0x89, 0x55, 0xE4, 0x0F, 0x85, 0x53, 0x02, 0x00, 0x00, 0x8D, 0x65, 0xF4, 0x89, 0xF0, 0x5B, 0x5E, 0x5F, 0x5D, 0xC3, 0x90, 0x85, 0xC0, 0x0F, 0x84, 0x18, 0x02, 0x00, 0x00, 0x8B, 0x48, 0x04, 0x8B, 0x83, 0xC0, 0x05, 0x00, 0x00, 0x8B, 0x78, 0x04, 0x8B, 0x83, 0x14, 0x06, 0x00, 0x00, 0x89, 0x4D, 0xC8, 0x89, 0x4D, 0xD4, 0x89, 0x45, 0xC4, 0x8B, 0x45, 0xC4, 0x89, 0x7D, 0xD0, 0x01, 0xCF, 0x89, 0x7D, 0xCC, 0x89, 0xCF, 0x85, 0xC0, 0x74, 0x06, 0x8B, 0x48, 0x04, 0x8D, 0x0C, 0xCF, 0x85, 0xD2, 0x74, 0x2E, 0x8B, 0x83, 0xD4, 0x05, 0x00, 0x00, 0x8B, 0x93, 0x80, 0x05, 0x00, 0x00, 0x8B, 0x78, 0x04, 0x8B, 0x52, 0x04, 0x8B, 0x45, 0xD0, 0x01, 0xD7, 0x29, 0xD0, 0x3B, 0x7D, 0xCC, 0x89, 0x45, 0xC4, 0x8B, 0x45, 0xD0, 0x0F, 0x44, 0x45, 0xC4, 0x03, 0x55, 0xC8, 0x01, 0xD0, 0x89, 0x45, 0xCC, 0x8B, 0x93, 0x90, 0x05, 0x00, 0x00, 0x39, 0x4D, 0xD4, 0x8B, 0x42, 0x04, 0x89, 0x45, 0xC8, 0x73, 0x32, 0x8B, 0x45, 0xD4, 0x89, 0xF2, 0x03, 0x10, 0x80, 0x78, 0x04, 0x08, 0x0F, 0x85, 0xCC, 0x01, 0x00, 0x00, 0x8B, 0x45, 0xD4, 0xEB, 0x13, 0x90, 0x8D, 0x74, 0x26, 0x00, 0x8B, 0x10, 0x01, 0xF2, 0x80, 0x78, 0x04, 0x08, 0x0F, 0x85, 0xB4, 0x01, 0x00, 0x00, 0x83, 0xC0, 0x08, 0x01, 0x32, 0x39, 0xC8, 0x72, 0xE9, 0x8B, 0xBB, 0x3C, 0x06, 0x00, 0x00, 0x85, 0xFF, 0x0F, 0x84, 0x73, 0x02, 0x00, 0x00, 0x8D, 0x05, 0x40, 0x00, 0x00, 0x00, 0x39, 0x4D, 0xCC, 0x89, 0x45, 0xD0, 0x8D, 0x83, 0xE0, 0xFB, 0xFE, 0xFF, 0x89, 0x45, 0xC0, 0x0F, 0x86, 0x92, 0xFE, 0xFF, 0xFF, 0x89, 0x75, 0xC4, 0x90, 0x8D, 0x74, 0x26, 0x00, 0x8B, 0x7D, 0xC4, 0x03, 0x39, 0x8B, 0x41, 0x04, 0x8B, 0x55, 0xD0, 0x89, 0x7D, 0xD4, 0x89, 0xC7, 0x0F, 0xB6, 0xF0, 0xC1, 0xEF, 0x08, 0xC1, 0xE7, 0x04, 0x03, 0x7D, 0xC8, 0x8B, 0x47, 0x04, 0x03, 0x84, 0x1A, 0x18, 0x05, 0x00, 0x00, 0x0F, 0xB6, 0x57, 0x0C, 0x83, 0xE2, 0x0F, 0x80, 0xFA, 0x0A, 0x0F, 0x84, 0xEA, 0x00, 0x00, 0x00, 0x83, 0xEE, 0x06, 0x83, 0xFE, 0x23, 0x77, 0x4A, 0x8B, 0x94, 0xB3, 0x00, 0x48, 0xFF, 0xFF, 0x01, 0xDA, 0xFF, 0xE2, 0x8D, 0xB4, 0x26, 0x00, 0x00, 0x00, 0x00, 0xB9, 0xFF, 0xFD, 0xFF, 0x6F, 0x29, 0xC1, 0x83, 0xF9, 0x0B, 0x0F, 0x87, 0xA0, 0x00, 0x00, 0x00, 0xF7, 0xD8, 0x89, 0x94, 0x83, 0x48, 0xFE, 0xFF, 0xBF, 0xE9, 0xE2, 0xFC, 0xFF, 0xFF, 0x66, 0x90, 0x8B, 0x45, 0xD0, 0x8B, 0x75, 0xD4, 0x8B, 0x84, 0x18, 0x58, 0x07, 0x00, 0x00, 0x03, 0x06, 0x2B, 0x47, 0x04, 0x89, 0x06, 0x8D, 0x74, 0x26, 0x00, 0x83, 0xC1, 0x08, 0x39, 0x4D, 0xCC, 0x0F, 0x87, 0x6C, 0xFF, 0xFF, 0xFF, 0xE9, 0xF1, 0xFD, 0xFF, 0xFF, 0x8D, 0xB4, 0x26, 0x00, 0x00, 0x00, 0x00, 0x8B, 0x75, 0xD4, 0x8B, 0x46, 0x04, 0x03, 0x47, 0x04, 0x8B, 0x7D, 0xD0, 0x2B, 0x84, 0x1F, 0x58, 0x07, 0x00, 0x00, 0x89, 0x46, 0x04, 0x8B, 0x45, 0xC0, 0x89, 0x06, 0xEB, 0xCB, 0x8D, 0x76, 0x00, 0x8B, 0x7D, 0xD4, 0x89, 0x07, 0xEB, 0xC1, 0x89, 0xF6, 0x8D, 0xBC, 0x27, 0x00, 0x00, 0x00, 0x00]
baseaddr = 0x47bb800
crash_point = 0x47bba6e # mov eax, [ebx + 0x5d4]

uc = Uc(UC_ARCH_X86, UC_MODE_32)

uc.mem_map(baseaddr - baseaddr%0x1000, 0x4000) # code
uc.mem_map(0x8000, 0x1000) # stack
uc.mem_map(0x1000, 0x1000) # [ebx + 0x5d4]
uc.mem_write(0x1000 + 0x5d4, b"\xff\xff\xff\xff")
uc.mem_write(baseaddr, bytes(shellcode))
uc.reg_write(UC_X86_REG_EIP, crash_point)
uc.reg_write(UC_X86_REG_ESP, 0x90000)
uc.reg_write(UC_X86_REG_EBX, 0x1000)
uc.emu_start(begin=crash_point, until=0, count=2)
print(f"eax={bytes(uc.mem_read(0x1000+ 0x5d4, 4))}")