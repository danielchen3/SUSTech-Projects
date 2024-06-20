.text
#
addi a4,x0,0xffffffff
sw a4,6(s11)
init:
jal switchjudge
sw a4,6(s11)
lw a1,2(s11)# test index
##we define a1 should be the case number input
##t6 should always be 0
##t5 should always be -1
##a3 is a and a4 is b
##INIT
#init:
beq a1,t6,case0
addi a1,a1,-1
beq a1,t6,case1
addi a1,a1,-1
beq a1,t6,case2
addi a1,a1,-1
beq a1,t6,case3
addi a1,a1,-1
beq a1,t6,case4
addi a1,a1,-1
beq a1,t6,case5
addi a1,a1,-1
beq a1,t6,case6
addi a1,a1,-1
beq a1,t6,case7


case0:
jal switchjudge
lw t2,3(s11)#test num a
jal switchjudge
lw t3,3(s11)#test num b
slli t2,t2,24
srli t2,t2,16
add t2,t2,t3
sw t2,6(s11)
jal init

case1:
jal switchjudge
lw t2,3(s11)#test num a
sw t2,7(s11)#view
addi sp,sp,-4
sw t2,0(sp)
jal init

case2:
jal switchjudge
lw t3,8(s11)#test num b
sw t3,7(s11)#view
addi sp,sp,-4
sw t3,0(sp)
jal init

case3:
lw a5,4(sp)#num a
lw a6,0(sp)#num b
beq a5,a6,LEDcase3
jal init
LEDcase3:
addi a7,zero,1
sw a7,6(s11)
jal init

case4:
lw a5,4(sp)#num a
lw a6,0(sp)#num b
blt a5,a6,LEDcase4
jal init
LEDcase4:
addi a7,zero,1
sw a7,6(s11)
jal init

case5:
lw a5,4(sp)#num a
lw a6,0(sp)#num b
bge a5,a6,LEDcase5
jal init
LEDcase5:
addi a7,zero,1
sw a7,6(s11)
jal init

case6:
lw a5,4(sp)#num a
lw a6,0(sp)#num b
bltu a5,a6,LEDcase6
jal init
LEDcase6:
addi a7,zero,1
sw a7,6(s11)
jal init

case7:
lw a5,4(sp)#num a
lw a6,0(sp)#num b
bgeu a5,a6,LEDcase7
jal init
LEDcase7:
addi a7,zero,1
sw a7,6(s11)
jal init

switchjudge:
lw t1,1(s11)
bne t1,zero,jump
beq x0,x0, switchjudge
jump:
lw t1,1(s11)
bne t1,zero,jump
jr ra
