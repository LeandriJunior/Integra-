import sys
import BO.robo.robo


def main(parameter=None):
    BO.robo.robo.Robo(parametro=parameter).processar()


if __name__ == '__main__':
    try:
        arg = sys.argv[1] if len(sys.argv) > 1 else None
        main(parameter=arg)
    except EnvironmentError as e:
        print(e)
        sys.exit(-1)
