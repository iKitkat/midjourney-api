source pyenv_3.10.12/bin/activate && cd midjourney-api
#source py_venv_3.10/bin/activate && cd midjourney-api 
# stop
pgrep -a python|awk -F " " '/task_bot|server/ {print $1}'|xargs -i kill -9 {}
# start
nohup python task_bot.py &
nohup python server.py &
#python server.py
