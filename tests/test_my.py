import pytest
from conftest import load

M = load(5)


def W(i, kind, zone, emv, **flags):
    return {"id": i, "kind": kind, "zone": zone, "emv": emv, **flags}


@pytest.mark.parametrize(
    "args, expected",
    [
        # Власний випадок 1: рівність mitigate_cost == emv не спрацьовує (суворе порівняння),
        # тому застосовується Т6 (прийняття активне)
        (
            (
                [
                    W(
                        "MY-01",
                        "threat",
                        "висока",
                        10000,
                        avoidable=False,
                        mitigate_cost=10000,
                    )
                ],
            ),
            [{"id": "MY-01", "strategy": "прийняття активне", "rule": "T6"}],
        ),
        # Власний випадок 2: можливість controllable має найвищий пріоритет (O1)
        (
            (
                [
                    W(
                        "MY-02",
                        "opportunity",
                        "висока",
                        15000,
                        controllable=True,
                        shareable=True,
                    )
                ],
            ),
            [{"id": "MY-02", "strategy": "використання", "rule": "O1"}],
        ),
        # Власний випадок 3: можливість без прапорців controllable/shareable з низької зони дає O4 (прийняття)
        (
            (
                [
                    W(
                        "MY-03",
                        "opportunity",
                        "низька",
                        5000,
                        controllable=False,
                        shareable=False,
                    )
                ],
            ),
            [{"id": "MY-03", "strategy": "прийняття", "rule": "O4"}],
        ),
    ],
)
def test_my_cases(args, expected):
    assert M.choose_strategies(*args) == expected