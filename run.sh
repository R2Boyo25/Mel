if [ "$(dpkg-query -W -f='${Version}' python3-venv)" == "" ]; then
    echo "python3-venv not found - installing it with apt"
    sudo apt install python3-venv
fi
python3 bot.py $@
