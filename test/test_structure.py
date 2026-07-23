from main import ask_question
def test_structure():

    result = []

    try:
        questions = [
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

        for num, question in enumerate(questions, 1):

            response = ask_question(question)

            has_intro = len(response.split('\n\n')[0]) > 15 if '\n\n' in response else False
            has_body = len(response) > 70
            has_source = "http" in response or "источник" in response.lower() or "Ссылка" in response

            is_good = has_intro and has_body and has_source

            result.append(is_good)

    except Exception as e:
        print(f'Ошибка: {e}')
        result.append(False)

    passed = sum(result)
    print(f'Тест на сохранение структуры ответа прошли {passed}/10 вопросов')


