from Controller.Controller import Controller


class Main:

    @staticmethod
    def main():
        try:
            ctrl = Controller()
            ctrl.controller()
        except KeyboardInterrupt:
            exit(0)


if __name__ == '__main__':
    Main.main()
