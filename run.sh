if [ "$(dpkg-query -W -f='${Version}' python3-venv)" == "" ]; then
    echo "python3-venv not found - installing it with apt"
    sudo apt install python3-venv
fi
if [ ! -f requirements.txt ]; then
    echo "Cd to dir containing project files!"
else
    if [ ! -d venv ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    if [ ! -d venv/lib/python*/site-packages/discord ]; then
        pip3 install -r requirements.txt
    fi
    python3 bot.py
fi
