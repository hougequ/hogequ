import random
import sys

starting_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A"]

def save_balance(balance):
    with open("balance.txt", "w") as file:
        file.write(str(balance))

def load_balance():
    try:
        with open("balance.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 1000

player_balance = load_balance()

cards_art = {
    "back": """
 _______
|░░░░░░░|
|░░░░░░░|
|░░░░░░░|
|░░░░░░░|
|_______|
""",
    "2": """
 _______
|2      |
|       |
|   ♠   |
|       |
|_______|
""",
    "3": """
 _______
|3      |
|   ♠   |
|   ♠   |
|   ♠   |
|_______|
""",
    "4": """
 _______
|4      |
|♠     ♠|
|       |
|♠     ♠|
|_______|
""",
    "5": """
 _______
|5      |
|♠     ♠|
|   ♠   |
|♠     ♠|
|_______|
""",
    "6": """
 _______
|6      |
|♠     ♠|
|♠     ♠|
|♠     ♠|
|_______|
""",
    "7": """
 _______
|7      |
|♠     ♠|
| ♠   ♠ |
|  ♠ ♠  |
|_______|
""",
    "8": """
 _______
|8      |
|♠     ♠|
|♠     ♠|
|♠     ♠|
|_______|
""",
    "9": """
 _______
|9      |
|♠  ♠  ♠|
|   ♠   |
|♠  ♠  ♠|
|_______|
""",
    "10": """
 _______
|10     |
|♠  ♠  ♠|
|   ♠   |
|♠  ♠  ♠|
|_______|
""",
    "J": """
 _______
|J      |
|   ♠   |
|   ♠   |
|♠  ♠  ♠|
|_______|
""",
    "Q": """
 _______
|Q      |
|   ♠   |
| ♠   ♠ |
|   ♠   |
|_______|
""",
    "K": """
 _______
|K      |
|♠     ♠|
|♠  ♠  ♠|
|♠     ♠|
|_______|
""",
    "A": """
 _______
|A      |
|   ♠   |
| ♠   ♠ |
|   ♠   |
|_______|
"""
}

def calculate_score(cards):
    score = sum([11 if card == "A" else 10 if card in ["K", "Q", "J"] else card for card in cards])
    if "A" in cards and score > 21:
        cards.remove("A")
        cards.append(1)
    return score

def display_cards(player_cards, computer_cards, hide_first=True):
    print("\nTwoje karty:", end=" ")
    for card in player_cards:
        if str(card) in cards_art:
            print(cards_art[str(card)], end=" ")
        else:
            print(cards_art["back"], end=" ")

    print("    Karty komputerowe:", end=" ")
    if hide_first:
        print(cards_art["back"], end=" ")
        for card in computer_cards[1:]:
            if str(card) in cards_art:
                print(cards_art[str(card)], end=" ")
            else:
                print(cards_art["back"], end=" ")
    else:
        for card in computer_cards:
            if str(card) in cards_art:
                print(cards_art[str(card)], end=" ")
            else:
                print(cards_art["back"], end=" ")

    print("\n")

def deal_card():
    # Zwraca losową kartę z talii.
    return random.choice(starting_deck)

def play_game():
    global player_balance

    if player_balance <= 0:
        print("Nie masz wystarczających środków, aby zagrać.")

        play_again = input("Czy chcesz zagrać ponownie? Wpisz 'tak' lub 'nie': ")
        if play_again.lower() == 'tak':
            player_balance = 1000  # Ustawienie salda otwarcia na 1000 USD
        else:
            end_game()
            sys.exit()

    while True:
        try:
            bet = int(input(f"Twoje aktualne saldo: {player_balance}. Wpisz swoją ofertę: "))
            if 1 <= bet <= player_balance:
                break
            else:
                print("Nieprawidłowy zakład. Wprowadź wartość od 1 do", player_balance)
        except ValueError:
            print("Nieprawidłowe dane wejściowe. Wprowadź liczbę całkowitą.")

    player_balance -= bet

    user_cards = []
    computer_cards = []

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    game_over = False

    while not game_over:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)

        display_cards(user_cards, computer_cards)

        if user_score == 0 or computer_score == 0 or user_score > 21:
            game_over = True
        else:
            user_should_continue = input("Chcesz wziąć kolejną kartę? Wpisz 'y' lub 'n': ")
            if user_should_continue.lower() == 'y':
                user_cards.append(deal_card())
            else:
                game_over = True

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    display_cards(user_cards, computer_cards, hide_first=False)

    print(f"Twoje konto: {user_score}")
    print(f"Konto komputera: {computer_score}")

    determine_winner(user_score, computer_score, bet)

def determine_winner(user_score, computer_score, bet):
    global player_balance

    if user_score > 21 or (computer_score <= 21 and computer_score >= user_score):
        print(f"Przegrałeś {bet} dolarów.")
    elif user_score == computer_score:
        print("Rysować. Zwrócimy Twój zakład.")
        player_balance += bet
    else:
        print(f"Wygrałeś {bet} dolarów!")
        player_balance += 2 * bet

    print(f"Twoje aktualne saldo: {player_balance}")
    save_balance(player_balance)

def end_game():
    print("Koniec gry. Do widzenia!")

def start_menu():
    while True:
        print("\n=== MENU ===")
        print("1. Zagraj w blackjacka")
        print("2. Zasady blackjacka")
        print("3. Zakończ grę")

        choice = input("Wybierz opcję (1/2/3): ")

        if choice == '1':
            play_game()
        elif choice == '2':
            print_rules()
        elif choice == '3':
            end_game()
            sys.exit()
        else:
            print("Zły wybór. Wpisz 1, 2 lub 3.")

def print_rules():
    print("\n=== ZASADY BLACKJACKA ===")
    print("Blackjack (lub 21) to gra karciana, w której celem jest uzyskanie kombinacji kart, których suma punktów będzie jak najbardziej zbliżona do 21, ale nie przekroczy tego progu.")
    print("Powodzenia w grze!")

if __name__ == "__main__":
    start_menu()