# 8-Bit CRP CPU

## How it works

The 8-Bit CRP CPU is a simple, custom-designed processor implemented in Verilog.  
It follows a classic **Von Neumann architecture**, where instructions and data share the same memory space. The CPU is based on a **multicycle design**, meaning that each instruction takes a variable number of clock cycles to complete.

The main components of the CPU include:

- **ALU (Arithmetic Logic Unit):** Performs arithmetic operations like addition and subtraction, as well as logical operations such as AND, OR, XOR, shifts (LSR, LSL/ASL, ASR), and comparison operations.  
- **Registers:** 16 general-purpose 8-bit registers, with registers 14 and 15 reserved for memory addressing in `LD` and `ST` instructions (R14 = lower 8 bits, R15 = upper 7 bits). A dedicated **stack pointer** starts at `0x7FFF` and counts downward.  
- **Controller:** Decodes instructions and generates control signals to orchestrate data movement, ALU operations, memory access, and branching.  
- **Datapath:** Connects all components and manages the flow of data between registers, ALU, and memory.  
- **Multiplexers:** Select ALU and register file inputs depending on the current instruction.  
- **State Counter:** Manages the instruction execution cycle, controlling fetch, decode, execute, and writeback stages.

The CPU supports **16-bit instruction width**. Instructions are categorized as R-type, I-type, and J-type:

- **R-type:** Register-to-register operations (e.g., ADD, SUB, AND, OR). Includes a function field for the exact operation.  
- **I-type:** Immediate operations, using an 8-bit immediate value (e.g., ADDI, SUBI, ANDI).  
- **J-type:** Jump instructions, which are relative and may be signed or unsigned depending on the opcode.

The CPU communicates with external memory via:

- **8-bit data bus:** `DI0–DI7` for memory input, `DO0–DO7` for memory output.  
- **15-bit address bus:** `A0–A14` for memory addressing.  
- **Write Enable (WE):** Connected to an external buffer (`DO15`), controlling memory writes.

Memory write protocol:

1. **Clock cycle 1:** Place the 8-bit data to write on `DO0–DO7` and set `WE` high. The data is temporarily stored externally.  
2. **Clock cycle 2:** Provide the 15-bit target address on `A0–A14`. Memory writes the previously buffered data to this address.

Instruction storage in memory:

- Each 16-bit instruction occupies **two consecutive addresses**:
  - Even addresses: lower 8 bits of the instruction
  - Odd addresses: upper 8 bits of the instruction

---

## Instruction Set Overview
<table border="0" cellpadding="0" cellspacing="0" width="370" style="border-collapse:
 collapse;table-layout:fixed;width:274pt">
 <colgroup><col width="83" style="mso-width-source:userset;mso-width-alt:2958;width:62pt">
 <col width="59" style="mso-width-source:userset;mso-width-alt:2104;width:44pt">
 <col width="19" span="12" style="mso-width-source:userset;mso-width-alt:682;
 width:14pt">
 </colgroup><tbody><tr height="19" style="height:14.4pt">
  <td height="19" class="xl66" width="83" style="height:14.4pt;width:62pt">MENEMONIC</td>
  <td class="xl67" width="59" style="border-left:none;width:44pt">OPCODE</td>
  <td colspan="12" class="xl67" width="228" style="border-right:1.0pt solid black;
  border-left:none;width:168pt">Operands</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">MOV</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl71" style="border-left:none">reg2</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">0000</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">ADD</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl75" style="border-left:none">reg2</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">0001</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">SUB</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl71" style="border-left:none">reg2</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">0010</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">AND</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl75" style="border-left:none">reg2</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">0011</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">OR</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl71" style="border-left:none">reg2</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">0100</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">XOR</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl75" style="border-left:none">reg2</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">0101</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">LD</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl77" style="border-left:none">&nbsp;</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">0110</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">ST</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl78" style="border-left:none">&nbsp;</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">0111</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">PUSH</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl77" style="border-left:none">&nbsp;</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">1000</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">POP</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl78" style="border-left:none">&nbsp;</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">1001</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">PUSHF</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="8" class="xl77" style="border-left:none">&nbsp;</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">1010</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">POPF</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="8" class="xl78" style="border-left:none">&nbsp;</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">1011</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">LSR</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl71" style="border-left:none">reg2</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">1100</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">LSL/ASL</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl75" style="border-left:none">reg2</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">1101</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">ASR</td>
  <td class="xl70" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="4" class="xl71" style="border-left:none">reg2</td>
  <td colspan="4" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">1110</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">CMP</td>
  <td class="xl74" style="border-top:none;border-left:none">0000</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="4" class="xl75" style="border-left:none">reg2</td>
  <td colspan="4" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">1111</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">CMPI</td>
  <td class="xl79" style="border-top:none;border-left:none">0001</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="8" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">ADDI</td>
  <td class="xl80" style="border-top:none;border-left:none">0010</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="8" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">SUBI</td>
  <td class="xl79" style="border-top:none;border-left:none">0011</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="8" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">ANDI</td>
  <td class="xl80" style="border-top:none;border-left:none">0100</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="8" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">ORI</td>
  <td class="xl79" style="border-top:none;border-left:none">0101</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="8" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">XORI</td>
  <td class="xl74" style="border-top:none;border-left:none">0110</td>
  <td colspan="4" class="xl75" style="border-left:none">reg1</td>
  <td colspan="8" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">MOV</td>
  <td class="xl70" style="border-top:none;border-left:none">0111</td>
  <td colspan="4" class="xl71" style="border-left:none">reg1</td>
  <td colspan="8" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">immediate</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">RJMP</td>
  <td class="xl74" style="border-top:none;border-left:none">1000</td>
  <td colspan="12" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">RET</td>
  <td class="xl79" style="border-top:none;border-left:none">1001</td>
  <td colspan="4" class="xl71" style="border-left:none">1101</td>
  <td colspan="4" class="xl71" style="border-left:none">1101</td>
  <td colspan="4" class="xl77" style="border-right:1.0pt solid black;border-left:
  none">&nbsp;</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">RCALL</td>
  <td class="xl80" style="border-top:none;border-left:none">1010</td>
  <td colspan="12" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">JE</td>
  <td class="xl79" style="border-top:none;border-left:none">1011</td>
  <td colspan="12" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">JNE</td>
  <td class="xl80" style="border-top:none;border-left:none">1100</td>
  <td colspan="12" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl69" style="height:14.4pt;border-top:none">JB</td>
  <td class="xl79" style="border-top:none;border-left:none">1101</td>
  <td colspan="12" class="xl71" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
 <tr height="19" style="height:14.4pt">
  <td height="19" class="xl73" style="height:14.4pt;border-top:none">JAE</td>
  <td class="xl80" style="border-top:none;border-left:none">1110</td>
  <td colspan="12" class="xl75" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
 <tr height="20" style="height:15.0pt">
  <td height="20" class="xl82" style="height:15.0pt;border-top:none">JL</td>
  <td class="xl83" style="border-top:none;border-left:none">1111</td>
  <td colspan="12" class="xl84" style="border-right:1.0pt solid black;border-left:
  none">address</td>
 </tr>
</tbody></table>

---

## How to test

1. **Set up external memory**  
   - Use a memory module with read/write capability and 15-bit address lines.  
   - Connect CPU data input pins (`DI0–DI7`) to memory output pins.  
   - Connect CPU data output pins (`DO0–DO7`) to memory input pins.  
   - Connect CPU address pins (`A0–A14`) to memory address pins.  
   - Connect CPU write enable pin (`DO15`) to memory `WE` input via an external buffer.

2. **Load a program**  
   - Instructions are 16 bits wide and occupy two consecutive memory addresses:  
     - Even addresses: lower 8 bits  
     - Odd addresses: upper 8 bits
      
3. **Reset the CPU state**  
   - Set `rst_n` **low** briefly while toggling the clock:  
     1. `rst_n = 0`, `clk = 1`  
     2. `clk = 0`  
     3. `rst_n = 1`  
   - This ensures the CPU starts from a clean state.
    
4. **Provide a clock signal**  
   - The CPU is multi-cycle; instructions need different numbers of clock cycles.  
   - Initialize the program counter (PC/IP) at `0x000`.



5. **Execute instructions**  
   - Start the clock and observe instructions running from memory.  
   - Try basic operations: `MOV`, `ADD`, `SUB`, logical instructions, etc.

6. **Memory access**  
   - Load memory addresses into R14 (low 8 bits) and R15 (high 7 bits).  
   - Use `LD` to read and `ST` to write.

7. **Stack operations**  
   - Test `PUSH` and `POP`. Stack pointer starts at `0x7FFF` and grows downward.

8. **Branching and jumps**  
   - Test relative jumps (`RJMP`, `JE`, `JNE`, etc.).  
   - Remember: `JL` uses signed offsets; others use unsigned.

## External hardware

- **Memory module:** 8-bit data, 15-bit address, supports read/write operations.  
- **Buffer register:** Connected to `DO15` to handle memory `WE` signal.  
- **Clock source:** Provides the clock signal for multicycle operation.  
