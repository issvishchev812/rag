from test.test_structure import test_structure
from test.test_safety import test_safety
from test.test_red_team import test_red_team
from test.test_rag import test_rag


def test_all():

    test_structure()

    test_safety()

    test_red_team()

    test_rag()



if __name__ == "__main__":
    test_all()