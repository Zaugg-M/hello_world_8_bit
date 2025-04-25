"""
Author: Michael Zaugg
hello_world.py
Date: 4-25-25
"""
import time
import os

"""
8-bit CPU Simulator

Registers:
  PC  - Program Counter
  MAR - Memory Address Register
  MBR - Memory Buffer Register
  IR  - Instruction Register
  A   - Accumulator

Instructions:
  0x10 - LDI A, immediate  (Load immediate into A)
  0x20 - OUT A              (Output character in A)
  0xFF - HLT                (Halt)
"""

class CPUVisualizer:
    def __init__(self, memory, delay=0.5):
        self.memory = memory
        self.delay = delay
        self.reset()

    def reset(self):
        self.PC = 0
        self.MAR = 0
        self.MBR = 0
        self.IR = 0
        self.A = 0
        self.running = True
        self.last_op = ''
        self.output = ''

    def _clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def _bits(self, value):
        bits = []
        for i in range(7, -1, -1):
            bit = (value >> i) & 1
            bits.append('●' if bit else '○')
        return ''.join(bits)

    def render(self):
        self._clear_screen()
        print('8-bit CPU State')
        print('-------------')
        print(f"PC : [{self._bits(self.PC)}]  {self.PC:#04x}")
        print(f"MAR: [{self._bits(self.MAR)}]  {self.MAR:#04x}")
        print(f"MBR: [{self._bits(self.MBR)}]  {self.MBR:#04x}")
        print(f"IR : [{self._bits(self.IR)}]  {self.IR:#04x}")
        print(f"A  : [{self._bits(self.A)}]  {self.A:#04x}")
        print()
        print(f"Last Operation: {self.last_op}")
        print("Display:")
        print(self.output)
        print('-------------')

    def fetch(self):
        self.MAR = self.PC
        opcode = self.memory[self.PC]
        self.MBR = opcode
        self.IR = opcode
        self.last_op = f"FETCH opcode {opcode:#04x} from {self.PC:#04x}"
        self.PC = (self.PC + 1) & 0xFF

    def decode_execute(self):
        opcode = self.IR

        if opcode == 0x10:
            # Load immediate into A
            self.MAR = self.PC
            value = self.memory[self.PC]
            self.MBR = value
            self.A = value
            self.last_op = f"LDI A <- {value:#04x}"
            self.PC = (self.PC + 1) & 0xFF

        elif opcode == 0x20:
            # Output character in A
            char = chr(self.A)
            self.output += char
            self.last_op = f"OUT '{char}'"

        elif opcode == 0xFF:
            # Halt execution
            self.running = False
            self.last_op = 'HLT'

        else:
            # Unknown opcode
            self.running = False
            self.last_op = f"UNKNOWN {opcode:#04x}" + " (HALT)"

    def step(self):
        self.fetch()
        self.render()
        time.sleep(self.delay)

        self.decode_execute()
        self.render()
        time.sleep(self.delay)

    def run(self):
        while self.running:
            self.step()

        # Final display
        self.render()
        print('== Operation Complete ==')
        input('Press Enter to exit')


if __name__ == '__main__':
    # Prepare "Hello, World!" program in memory
    message = "Hello, World!"
    program = []

    # Build instructions: LDI + char, OUT, then HLT
    for ch in message:
        program.append(0x10)
        program.append(ord(ch))
        program.append(0x20)
    program.append(0xFF)

    # Load program into 256-byte memory
    memory = [0x00] * 256
    for addr, byte in enumerate(program):
        memory[addr] = byte

    # Run the CPU visualizer
    cpu = CPUVisualizer(memory, delay=0.3)
    cpu.run()