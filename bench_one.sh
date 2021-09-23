echo "$1 $2" 
o1=`./build/tests/$1  $2 & ./build/tests/$1  $2 -c localhost`
#echo $o1
echo "------      ------      ------      "
o1=`./build/tests/$1_opt  $2 & ./build/tests/$1_opt  $2 -c localhost`