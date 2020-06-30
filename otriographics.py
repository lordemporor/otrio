class window():
    def __init__(self):
        pass  #Enter in code when working on


    def request_player_action(self):
        #Replace with code when working on
        raw_action_input = input("Where would you like to go? ")
        return raw_action_input[0], raw_action_input[1]


    def terminal(self):
        #TEMP CODE!
        # Asking player
        players = []
        accepted_player_type_entries = ["random", "ai", "human"]
        for player_type in accepted_player_type_entries:
            continue_asking_for_players = True
        while continue_asking_for_players:
            if len(players) == 0:
                print("No players currently")
            elif len(players) == 1:
                print("Only one player currently")
            else:
                print("There are currently " + str(len(players)) + " players currently")

            raw_player_type_input = ""
            entry_not_accepted = False
            while not (str.lower(raw_player_type_input) in accepted_player_type_entries):
                raw_player_type_input =