:: Remove a constant path of my PC.
python uddocs.py
robocopy uddocs build\html * >uddocs.log
robocopy build\html ..\docs /mir >> uddocs.log