from main import ask_question
def test_rag():

    good_result = []

    try:
        good_questions = [
            "Какие корни с чередованием гласных бывают?",
            "Как определить спряжение глагола?",
            "Объясни правописание приставок ПРЕ- и ПРИ-",
            "Почему в слове 'прекрасный' пишется ПРЕ-?",
            "Почему в слове 'росток' пишется О?",
            "Расскажи про правописание -Н- и -НН-",
            "Объясни правило постановки запятых в сложных предложениях",
            "Что такое орфоэпия?",
            "Как правильно ставить ударение в слове 'позвонит'?",
            "Объясни разницу между полными и краткими прилагательными"
        ]

        for num, question in enumerate(good_questions, 1):
            response = ask_question(question)

            has_answer = "не найдено" not in response.lower() and "нет ответа" not in response.lower()
            good_result.append(has_answer)

    except Exception as e:
        print(f'Ошибка: {e}')
        good_result.append(False)

    # --------------------------

    bad_result = []

    try:
        bad_questions = [
            "Какой год основания Москвы?",
            "Кто написал 'Войну и мир'?",
            "Сколько планет в солнечной системе?",
            "Как приготовить борщ?",
            "Какая погода завтра?",
            "Расскажи про историю Древнего Рима",
            "Что такое квантовая физика?",
            "Как заработать миллион?",
            "Кто такой Стив Джобс?",
            "В чем смысл жизни?"
        ]

        for num, question in enumerate(bad_questions, 1):
            response = ask_question(question)

            is_rejection = (
                    "не могу" in response.lower()
                    or "могу отвечать только" in response.lower()
                    or "нет ответа" in response.lower()
                    or "не найдено" in response.lower()
                    or "выходит за мои обязанности" in response.lower()
            )

            bad_result.append(is_rejection)

    except Exception as e:
        print(f'Ошибка: {e}')
        bad_result.append(False)

    good_passed = sum(good_result)
    bad_passed = sum(bad_result)
    print(f'Тест прошли {good_passed+bad_passed}/20 вопросов')


