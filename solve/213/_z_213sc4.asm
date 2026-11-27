bits 64
_start:
    mov rbx, rsp
    mov r12, 0x4000
.scan:
    mov rax, [rbx]
    cmp rax, 3
    jne .next
    mov rcx, [rbx+8]
    sub rcx, 0x40
    test rcx, 0xfff
    jnz .next
    test rcx, rcx
    jz .next
    lea rsi, [rcx+0x202060]
    mov rax, 1
    mov rdi, 1
    mov rdx, 100
    syscall
    cmp rax, 0
    jg .done
.next:
    add rbx, 8
    dec r12
    jnz .scan
.done:
    mov rax, 60
    xor rdi, rdi
    syscall
