

cur_dir=`pwd`
cd ..
prev_dir=`pwd`
echo $cur_dir
cd $cur_dir


python_exe=`which python`


ico_file='example_python_test_program.ico'
version_file='version.txt'
main_py='main.py'
out_name='python_gui_app'

rm -r ./dist

$python_exe -m PyInstaller --clean --onefile --nowindow -w -i $ico_file --version-file $version_file -n $out_name $main_py

cp $cur_dir/tp_core/test.py $cur_dir/dist/test.py
cp $cur_dir/tp_core/test_runner.py $cur_dir/dist/test_runner.py
