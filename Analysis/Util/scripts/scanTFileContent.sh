
#!/bin/bash
echo "qqq" | root -q -l -b "scanTFileContent.C+(\"${1}\")" | less -S


