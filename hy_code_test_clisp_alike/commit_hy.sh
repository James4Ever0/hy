cd /Users/jamesbrown/Library/Python/3.8/lib/python/site-packages/hy

mkdir hy_code_test_clisp_alike
cd hy_code_test_clisp_alike

cp /Users/jamesbrown/Desktop/works/hy_code_test_clisp_alike/*.hy .
cp /Users/jamesbrown/Desktop/works/hy_code_test_clisp_alike/*.py .
cp /Users/jamesbrown/Desktop/works/hy_code_test_clisp_alike/*.sh .

cd /Users/jamesbrown/Library/Python/3.8/lib/python/site-packages/hy
cp /Users/jamesbrown/Desktop/works/hy_code_test_clisp_alike/commit_hy.sh .
git add .
git commit -m 'init'
git push origin master