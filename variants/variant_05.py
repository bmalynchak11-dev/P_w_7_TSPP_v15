"""Варіант 15. Задача 5: Вибір стратегії реагування за правилами."""


def choose_strategies(risks: list) -> list:
    if not risks:
        raise ValueError("Реєстр порожній")

    valid_kinds = {"threat", "opportunity"}
    valid_zones = {"низька", "середня", "висока", "критична"}

    result = []

    for r in risks:
        rid = r.get("id")
        kind = r.get("kind")
        zone = r.get("zone")
        emv = r.get("emv")

        # Перевірка коректності полів
        if kind not in valid_kinds:
            raise ValueError(f"Ризик {rid}: невідомий вид «{kind}»")

        if zone not in valid_zones:
            raise ValueError(f"Ризик {rid}: невідома зона «{zone}»")

        if isinstance(emv, bool) or not isinstance(emv, (int, float)) or emv < 0:
            raise ValueError(
                f"Ризик {rid}: очікувана вартість має бути невід'ємним числом"
            )

        scope = r.get("scope")
        avoidable = bool(r.get("avoidable", False))
        controllable = bool(r.get("controllable", False))
        shareable = bool(r.get("shareable", False))
        transfer_cost = r.get("transfer_cost")
        mitigate_cost = r.get("mitigate_cost")

        if kind == "threat":
            # Правила для загроз T1 - T6
            if scope == "org":
                strat, rule = "ескалація", "T1"
            elif zone == "критична" and avoidable:
                strat, rule = "уникнення", "T2"
            elif (
                zone != "низька"
                and transfer_cost is not None
                and transfer_cost < emv
            ):
                strat, rule = "передача", "T3"
            elif (
                zone != "низька"
                and mitigate_cost is not None
                and mitigate_cost < emv
            ):
                strat, rule = "зниження", "T4"
            elif zone == "низька":
                strat, rule = "прийняття пасивне", "T5"
            else:
                strat, rule = "прийняття активне", "T6"
        else:
            # Правила для можливостей O1 - O4
            if controllable:
                strat, rule = "використання", "O1"
            elif shareable:
                strat, rule = "поділ", "O2"
            elif zone in ("висока", "критична"):
                strat, rule = "посилення", "O3"
            else:
                strat, rule = "прийняття", "O4"

        result.append({"id": rid, "strategy": strat, "rule": rule})

    return result