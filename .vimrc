autocmd FileType python map <buffer> <F9> <esc>:w<CR>:!clear<CR>:exec '!ampy -p /dev/tty.usbmodem101 run' shellescape(@%, 1)<CR>
autocmd FileType python imap <buffer> <F9> <esc>:w<CR>:!clear<CR>:exec '!ampy -p /dev/tty.usbmodem101 run' shellescape(@%, 1)<CR>

autocmd FileType python map <buffer> <F8> <esc>:w<CR>:!clear<CR>:exec '!ampy -p /dev/tty.usbmodem1101 run' shellescape(@%, 1)<CR>
autocmd FileType python imap <buffer> <F8> <esc>:w<CR>:!clear<CR>:exec '!ampy -p /dev/tty.usbmodem1101 run' shellescape(@%, 1)<CR>
