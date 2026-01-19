from game_state import (
    create_initial_state,
    move_player,
    pickup_item,
    use_item,
    interact_with_environment,
    save_game,
    load_game,
    reset_game_state
)

if __name__ == "__main__":
    print("=== DEMO START ===")

    state = create_initial_state()
    print("Initial Player:", state.player)

    # Move + pickup potion
    move_player(state, 2, 2)
    pickup_item(state, "p1")

    # Use potion after reducing health
    state.player.health = 50
    use_item(state, "p1")
    print("After using potion, Player:", state.player)

    # Interact with door
    interact_with_environment(state, "d1")

    # Save game
    save_game(state, "saves/save1.json")

    # Load game
    loaded = load_game("saves/save1.json")
    print("Loaded Player:", loaded.player)
    print("Loaded Door State:", loaded.env_objects["d1"].state)

    # Reset game
    state = reset_game_state()
    print("After Reset Player:", state.player)

    print("=== DEMO END ===")
