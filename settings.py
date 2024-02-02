class Settings:
    class Messages:
        NewGame = "Creating game"
        LoadOptions = "Loading options"
        NotTurn = "Wait for your turn, nigger."
        SelfChallenge = "You can't play against yourself, nigger"
        NoUser = lambda x: f"There isn't any member named `{x}`, nigger"

    DialogueInterval = 1
    
    RoundConfig = [
        None,
        [1]*1+[0]*2,
        [1]*3+[0]*4,
        [1]*4+[0]*5,
    ]
    DrawConfig = [None, 2, 4]

    PlayerHealth = 6
    MaxItems = 8