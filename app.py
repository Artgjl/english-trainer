import json
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="English Trainer",
    page_icon="🎓",
    layout="centered",
)

WORD_SETS = {
    "A1": [
        {"english": "apple", "russian": "яблоко"},
        {"english": "book", "russian": "книга"},
        {"english": "cat", "russian": "кошка"},
        {"english": "city", "russian": "город"},
        {"english": "day", "russian": "день"},
        {"english": "door", "russian": "дверь"},
        {"english": "family", "russian": "семья"},
        {"english": "food", "russian": "еда"},
        {"english": "friend", "russian": "друг"},
        {"english": "house", "russian": "дом"},
        {"english": "morning", "russian": "утро"},
        {"english": "mother", "russian": "мама"},
        {"english": "school", "russian": "школа"},
        {"english": "student", "russian": "ученик"},
        {"english": "water", "russian": "вода"},
        {"english": "happy", "russian": "счастливый"},
        {"english": "small", "russian": "маленький"},
        {"english": "beautiful", "russian": "красивый"},
        {"english": "cold", "russian": "холодный"},
        {"english": "young", "russian": "молодой"},
        {"english": "come", "russian": "приходить"},
        {"english": "drink", "russian": "пить"},
        {"english": "eat", "russian": "есть"},
        {"english": "help", "russian": "помогать"},
        {"english": "learn", "russian": "учить"},
        {"english": "listen", "russian": "слушать"},
        {"english": "read", "russian": "читать"},
        {"english": "speak", "russian": "говорить"},
        {"english": "walk", "russian": "гулять"},
        {"english": "write", "russian": "писать"},
    ],
    "A2": [
        {"english": "abroad", "russian": "за границей"},
        {"english": "accident", "russian": "несчастный случай"},
        {"english": "adventure", "russian": "приключение"},
        {"english": "airport", "russian": "аэропорт"},
        {"english": "appointment", "russian": "назначенная встреча"},
        {"english": "arrive", "russian": "прибывать"},
        {"english": "borrow", "russian": "брать взаймы"},
        {"english": "careful", "russian": "осторожный"},
        {"english": "celebrate", "russian": "праздновать"},
        {"english": "comfortable", "russian": "удобный"},
        {"english": "conversation", "russian": "разговор"},
        {"english": "delicious", "russian": "вкусный"},
        {"english": "different", "russian": "разный"},
        {"english": "difficult", "russian": "трудный"},
        {"english": "direction", "russian": "направление"},
        {"english": "enough", "russian": "достаточно"},
        {"english": "explain", "russian": "объяснять"},
        {"english": "famous", "russian": "известный"},
        {"english": "forget", "russian": "забывать"},
        {"english": "future", "russian": "будущее"},
        {"english": "important", "russian": "важный"},
        {"english": "invite", "russian": "приглашать"},
        {"english": "journey", "russian": "путешествие"},
        {"english": "message", "russian": "сообщение"},
        {"english": "possible", "russian": "возможный"},
        {"english": "remember", "russian": "помнить"},
        {"english": "surprised", "russian": "удивлённый"},
        {"english": "together", "russian": "вместе"},
        {"english": "weather", "russian": "погода"},
        {"english": "without", "russian": "без"},
    ],
    "B1": [
        {"english": "achieve", "russian": "достигать"},
        {"english": "advice", "russian": "совет"},
        {"english": "afford", "russian": "позволить себе"},
        {"english": "avoid", "russian": "избегать"},
        {"english": "behavior", "russian": "поведение"},
        {"english": "challenge", "russian": "испытание"},
        {"english": "choice", "russian": "выбор"},
        {"english": "compare", "russian": "сравнивать"},
        {"english": "complain", "russian": "жаловаться"},
        {"english": "decision", "russian": "решение"},
        {"english": "describe", "russian": "описывать"},
        {"english": "develop", "russian": "развивать"},
        {"english": "environment", "russian": "окружающая среда"},
        {"english": "experience", "russian": "опыт"},
        {"english": "improve", "russian": "улучшать"},
        {"english": "include", "russian": "включать"},
        {"english": "increase", "russian": "увеличивать"},
        {"english": "instead", "russian": "вместо"},
        {"english": "knowledge", "russian": "знание"},
        {"english": "opinion", "russian": "мнение"},
        {"english": "opportunity", "russian": "возможность"},
        {"english": "organize", "russian": "организовывать"},
        {"english": "prepare", "russian": "готовиться"},
        {"english": "probably", "russian": "вероятно"},
        {"english": "promise", "russian": "обещать"},
        {"english": "relationship", "russian": "отношения"},
        {"english": "responsible", "russian": "ответственный"},
        {"english": "suggest", "russian": "предлагать"},
        {"english": "succeed", "russian": "добиваться успеха"},
        {"english": "valuable", "russian": "ценный"},
    ],
    "B2": [
        {"english": "accurate", "russian": "точный"},
        {"english": "acknowledge", "russian": "признавать"},
        {"english": "advantage", "russian": "преимущество"},
        {"english": "approach", "russian": "подход"},
        {"english": "assumption", "russian": "предположение"},
        {"english": "aware", "russian": "осведомлённый"},
        {"english": "benefit", "russian": "польза"},
        {"english": "circumstance", "russian": "обстоятельство"},
        {"english": "complex", "russian": "сложный"},
        {"english": "consequence", "russian": "последствие"},
        {"english": "contribute", "russian": "вносить вклад"},
        {"english": "convince", "russian": "убеждать"},
        {"english": "demonstrate", "russian": "демонстрировать"},
        {"english": "efficient", "russian": "эффективный"},
        {"english": "emphasize", "russian": "подчёркивать"},
        {"english": "essential", "russian": "необходимый"},
        {"english": "evidence", "russian": "доказательство"},
        {"english": "flexible", "russian": "гибкий"},
        {"english": "furthermore", "russian": "кроме того"},
        {"english": "impact", "russian": "влияние"},
        {"english": "maintain", "russian": "поддерживать"},
        {"english": "nevertheless", "russian": "тем не менее"},
        {"english": "perspective", "russian": "точка зрения"},
        {"english": "prevent", "russian": "предотвращать"},
        {"english": "reliable", "russian": "надёжный"},
        {"english": "require", "russian": "требовать"},
        {"english": "significant", "russian": "значительный"},
        {"english": "solution", "russian": "решение проблемы"},
        {"english": "tend", "russian": "иметь склонность"},
        {"english": "whereas", "russian": "тогда как"},
    ],
}

CUSTOM_WORDS_FILE = Path(__file__).with_name("custom_words.json")


def load_custom_words():
    if not CUSTOM_WORDS_FILE.exists():
        return []
    try:
        data = json.loads(CUSTOM_WORDS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [
                item
                for item in data
                if isinstance(item, dict)
                and isinstance(item.get("english"), str)
                and isinstance(item.get("russian"), str)
            ]
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save_custom_words(words):
    CUSTOM_WORDS_FILE.write_text(
        json.dumps(words, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def reset_training():
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.correct = False
    for key in list(st.session_state):
        if key.startswith("answer_"):
            del st.session_state[key]


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #071229, #282267 55%, #164e63);
        color: white;
    }
    .block-container {max-width: 760px; padding-top: 2.5rem;}
    .word-card {
        background: linear-gradient(145deg, rgba(255,255,255,.16), rgba(255,255,255,.07));
        border: 1px solid rgba(255,255,255,.25);
        border-radius: 28px;
        padding: 48px 24px;
        text-align: center;
        box-shadow: 0 22px 60px rgba(0,0,0,.3);
        margin: 22px 0;
    }
    .level {color: #c4b5fd; font-size: 17px; letter-spacing: .08em;}
    .russian-word {font-size: 48px; font-weight: 800; margin-top: 10px;}
    .score {text-align: center; color: #ddd6fe; font-size: 20px; margin: 12px 0;}
    h1, .subtitle {text-align: center;}
    .stButton button {border-radius: 14px; font-weight: 700; min-height: 48px;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "index" not in st.session_state:
    reset_training()
if "custom_words" not in st.session_state:
    st.session_state.custom_words = load_custom_words()

st.title("🎓 English Trainer")
st.markdown(
    '<p class="subtitle">Тренируй готовые уровни или создай свой словарь</p>',
    unsafe_allow_html=True,
)

section = st.sidebar.radio("Раздел", ["Тренировка", "Мои слова"])

if section == "Мои слова":
    st.subheader("Добавить слово")
    with st.form("add_word", clear_on_submit=True):
        russian = st.text_input("Слово на русском", max_chars=60)
        english = st.text_input("Перевод на английском", max_chars=60)
        submitted = st.form_submit_button("Добавить", use_container_width=True)

    if submitted:
        russian_clean = russian.strip()
        english_clean = english.strip().lower()
        if not russian_clean or not english_clean:
            st.warning("Заполните оба поля.")
        elif any(
            item["english"].lower() == english_clean
            and item["russian"].lower() == russian_clean.lower()
            for item in st.session_state.custom_words
        ):
            st.info("Такое слово уже есть в вашем словаре.")
        else:
            st.session_state.custom_words.append(
                {"english": english_clean, "russian": russian_clean}
            )
            try:
                save_custom_words(st.session_state.custom_words)
                st.success("Слово добавлено и сохранено.")
            except OSError:
                st.error("Не удалось сохранить файл со словами.")

    st.subheader(f"Ваш словарь: {len(st.session_state.custom_words)} слов")
    if st.session_state.custom_words:
        for number, item in enumerate(st.session_state.custom_words, start=1):
            st.write(f'{number}. {item["russian"]} — {item["english"]}')
    else:
        st.info("Пока здесь нет слов. Добавьте первое слово выше.")
    st.stop()

level = st.selectbox(
    "Выберите набор слов",
    ["A1", "A2", "B1", "B2", "Мои слова"],
)

if st.session_state.get("last_level") != level:
    st.session_state.last_level = level
    reset_training()

words = (
    st.session_state.custom_words
    if level == "Мои слова"
    else WORD_SETS[level]
)

if not words:
    st.info("Сначала добавьте слова в разделе «Мои слова».")
    st.stop()

if st.session_state.index >= len(words):
    percent = round(st.session_state.score / len(words) * 100)
    st.success(
        f"Тренировка завершена! Результат: "
        f"{st.session_state.score} из {len(words)} — {percent}%."
    )
    st.balloons()
    if st.button("Пройти ещё раз", use_container_width=True):
        reset_training()
        st.rerun()
    st.stop()

word = words[st.session_state.index]
answer_key = f"answer_{level}_{st.session_state.index}"

st.markdown(
    f'<div class="score">Очки: {st.session_state.score} · '
    f'Слово {st.session_state.index + 1} из {len(words)}</div>',
    unsafe_allow_html=True,
)
st.progress(st.session_state.index / len(words))
st.markdown(
    f"""
    <div class="word-card">
        <div class="level">НАБОР {level}</div>
        <div class="russian-word">{word["russian"]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

answer = st.text_input(
    "Введите перевод на английском:",
    key=answer_key,
    disabled=st.session_state.answered,
    placeholder="Например: book",
)

if not st.session_state.answered:
    if st.button("Проверить", use_container_width=True):
        cleaned_answer = answer.strip().lower()
        if not cleaned_answer:
            st.warning("Сначала введите ответ.")
        else:
            st.session_state.answered = True
            st.session_state.correct = cleaned_answer == word["english"].lower()
            if st.session_state.correct:
                st.session_state.score += 1
            st.rerun()

if st.session_state.answered:
    if st.session_state.correct:
        st.success("Правильно! Отличная работа.")
    else:
        st.error(f'Неверно. Правильный ответ: {word["english"]}')

    if st.button("Следующее слово →", use_container_width=True):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.correct = False
        st.rerun()
