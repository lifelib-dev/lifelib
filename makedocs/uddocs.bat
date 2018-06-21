:: Remove a constant path of my PC.
python uddocs.py
robocopy uddocs build\html * >uddocs.log
robocopy build\html ..\..\lifelib-docs\docs /mir >> uddocs.log