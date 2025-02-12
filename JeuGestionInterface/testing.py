def readgametoplayerpos():
    """Ouvre le txt contenant la position de la caméra."""
    with open('Save/cvaluessaves.txt', 'r') as f:
        save = f.read().replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(",")
    return save

print(readgametoplayerpos())