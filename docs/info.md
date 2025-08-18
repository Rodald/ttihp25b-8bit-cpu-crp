<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->
# 8-Bit CRP CPU

## How it works

The 8-Bit CRP CPU is a simple, custom-designed processor implemented in Verilog.  
It follows a classic 8-bit CPU architecture with separate datapath and control units, allowing it to execute basic instructions such as arithmetic, logic, and data transfer operations.  

The CPU consists of the following main components:

- **ALU (Arithmetic Logic Unit):** Performs arithmetic operations like addition and subtraction, as well as logical operations such as AND, OR, and XOR.  
- **Registers:** Stores temporary data and intermediate results. A register file holds multiple registers accessible by instructions.  
- **Controller:** Decodes instructions and generates control signals to orchestrate data movement and ALU operations.  
- **Datapath:** Connects all components and manages the flow of data between registers, ALU, and memory.  
- **Multiplexers:** Select inputs for the ALU or register file based on the current instruction.  
- **State Counter:** Manages the instruction execution cycle, controlling fetch, decode, execute, and writeback stages.  

The CPU has an 8-bit data interface (`DI0`–`DI7` for inputs and `DO0`–`DO7` for outputs) and bidirectional pins for additional memory or peripherals.

---
## How to test

Explain how to use your project

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
