.data
num: .word 46000
.text
main:
la s6 num
lw s7,0(s6)
#lw s10,1(s11)读取测试数据x s11:0xffff_fff0
li a7, 5
ecall 
#get n, and set in register a0
#addi a0,a0,1
addi s10,a0,0
addi a0,x0,1
addi s9,a0,0
lp:
jal fact
bge a0,s10 finish
addi s9,s9,1
addi a0,s9,0
jal lp

fact:
addi sp, sp,-12 #adjust stack for 2 items
sw ra, 4(sp) #save the return address
sw a0, 0(sp) #save the argument n
#print a0
addi s5,x0,1
cycle1:
addi s5,s5,1
bge s7,s5,cycle1
li a7 1
ecall

#if判断
slti t0, a0, 2 #test for n<2
beq t0, zero, L1 #if n>=2,go to L1
addi a0, zero, 1 #else return 1

#第二个输出循环
#addi s1,x0,1
#addi s2,sp,0
#print2:
#sw a0,0(s2):0(s2)代表输出位置
#addi s1,s1,1
#bne s1,s0,print2
addi s5,x0,1
cycle2:
addi s5,s5,1
bge s7,s5,cycle2
li a7 1
ecall#because in this situation,a0 must be 1

addi sp, sp, 12 #pop 2 items off stack
jr ra #return to caller
L1:
addi a0, a0, -2 #n>=1; argument gets(n-2)
jal fact #call fact with(n-2)
addi t2, a0, 0 #
sw t2, 8(sp)
addi s5,x0,1
cycle3:
addi s5,s5,1
bge s7,s5,cycle3
li a7 1
ecall# t2 is a0

lw a0, 0(sp) #return from jal: restore argument
lw ra, 4(sp) #restore the return address
addi a0, a0, -1 #n>=1; argument gets(n-1)
jal fact #call fact with(n-1)
addi t1, a0, 0 #
lw a0, 0(sp) #return from jal: restore argument
addi s5,x0,1
cycle4:
addi s5,s5,1
bge s7,s5,cycle4
li a7 1
ecall

lw ra, 4(sp) #restore the return address
lw t2, 8(sp)

addi s5,x0,1
cycle5:
addi s5,s5,1
bge s7,s5,cycle5
li a7 1
ecall

addi sp, sp, 12 #adjust stack pointer to pop 2 items
add a0, t2, t1 #return fact(n-1)+fact(n-2)
jr ra #return to the caller

finish:
#lw 输出
