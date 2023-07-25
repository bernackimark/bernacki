class UI:
    @staticmethod
    def get_user_bet() -> int:
        return int(input('What is your bet? '))

    @staticmethod
    def display_balance(balance: float) -> None:
        print(f'Your balance is {balance}')

    @staticmethod
    def display_reels(reels) -> None:
        for r in reels:
            print(r.visible_rows())

    @staticmethod
    def display_spun_matrix(matrix: list[list]) -> None:
        for r in matrix:
            print(r)

    @staticmethod
    def display(text) -> None:
        print(text)
