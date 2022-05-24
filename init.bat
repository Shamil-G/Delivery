echo "# Delivery" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Shamil-G/Delivery.git
git push -u origin main

rem or push an existing repository from the command line
rem git remote add origin https://github.com/Shamil-G/Delivery.git
rem git branch -M main
rem git push -u origin main