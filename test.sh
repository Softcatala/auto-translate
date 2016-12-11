./program.py -s test/ca/alpha-to-logo.po -t test/es/alpha-to-logo.po -o alpha-to-logo.po > out
diff -u test/expected/alpha-to-logo.po alpha-to-logo.po 
diff -u test/expected/alpha-to-logo.po alpha-to-logo.po > diff.txt



