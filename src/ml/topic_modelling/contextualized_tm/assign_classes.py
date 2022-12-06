from contextualized_topic_models.models.kitty_classifier import Kitty
import json


def main() -> None:
    kt = Kitty.load("kitty.pkl")

    with open('assigned_labels.json', 'r+') as file:
        classes = json.load(file)
        kt.assigned_classes = {int(k): v for k, v in classes.items()}

    kt.save('kitty.pkl')


if __name__ == '__main__':
    main()