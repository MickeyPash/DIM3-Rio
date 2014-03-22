DIM3 Team Zeta
========
Application deployed at: http://brunomperes.pythonanywhere.com/


#### Running virtualenv
`source env/bin/activate`

to stop running the virtual environment it, type:

`deactivate`

Alternative:

#### Install virtualenvwrapper
`sudo pip install virtualenvwrapper`

#### Set WORKON_HOME to your virtualenv dir
`export WORK_HOME=~/.virtualenvs`

#### Open your .bashrc file with your favourite editor
`nano ~/.bashrc` And add this line to the end of it:
`source /usr/local/bin/virtualenvwrapper.sh`
Save and restart terminal

#### List your virtual environments
`lsvirtualenv -b`

#### Run the environment
`workon [env]`

![ScreenShot](http://octodex.github.com/images/pythocat.png)
