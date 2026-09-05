import base64
import html
import json
import ssl
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import streamlit as st
import certifi


st.set_page_config(
    page_title="Language Trainer",
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

FRENCH_WORD_SETS = {
    "A1": [
        {"english": "bonjour", "russian": "привет"},
        {"english": "livre", "russian": "книга"},
        {"english": "maison", "russian": "дом"},
        {"english": "eau", "russian": "вода"},
        {"english": "école", "russian": "школа"},
        {"english": "famille", "russian": "семья"},
        {"english": "ami", "russian": "друг"},
        {"english": "manger", "russian": "есть"},
        {"english": "boire", "russian": "пить"},
        {"english": "parler", "russian": "говорить"},
        {"english": "lire", "russian": "читать"},
        {"english": "écrire", "russian": "писать"},
        {"english": "petit", "russian": "маленький"},
        {"english": "grand", "russian": "большой"},
        {"english": "heureux", "russian": "счастливый"},
    ],
    "A2": [
        {"english": "voyager", "russian": "путешествовать"},
        {"english": "acheter", "russian": "покупать"},
        {"english": "choisir", "russian": "выбирать"},
        {"english": "commencer", "russian": "начинать"},
        {"english": "comprendre", "russian": "понимать"},
        {"english": "demander", "russian": "спрашивать"},
        {"english": "répondre", "russian": "отвечать"},
        {"english": "oublier", "russian": "забывать"},
        {"english": "rencontrer", "russian": "встречать"},
        {"english": "souvent", "russian": "часто"},
        {"english": "bientôt", "russian": "скоро"},
        {"english": "besoin", "russian": "необходимость"},
        {"english": "facile", "russian": "лёгкий"},
        {"english": "difficile", "russian": "трудный"},
        {"english": "travail", "russian": "работа"},
    ],
    "B1": [
        {"english": "améliorer", "russian": "улучшать"},
        {"english": "réussir", "russian": "добиваться успеха"},
        {"english": "conseil", "russian": "совет"},
        {"english": "expérience", "russian": "опыт"},
        {"english": "environnement", "russian": "окружающая среда"},
        {"english": "habitude", "russian": "привычка"},
        {"english": "pourtant", "russian": "однако"},
        {"english": "probablement", "russian": "вероятно"},
        {"english": "éviter", "russian": "избегать"},
        {"english": "proposer", "russian": "предлагать"},
        {"english": "décider", "russian": "решать"},
        {"english": "expliquer", "russian": "объяснять"},
        {"english": "comparer", "russian": "сравнивать"},
        {"english": "connaissance", "russian": "знание"},
        {"english": "occasion", "russian": "возможность"},
    ],
    "B2": [
        {"english": "avantage", "russian": "преимущество"},
        {"english": "conséquence", "russian": "последствие"},
        {"english": "preuve", "russian": "доказательство"},
        {"english": "fiable", "russian": "надёжный"},
        {"english": "exiger", "russian": "требовать"},
        {"english": "empêcher", "russian": "предотвращать"},
        {"english": "maintenir", "russian": "поддерживать"},
        {"english": "approfondir", "russian": "углублять"},
        {"english": "néanmoins", "russian": "тем не менее"},
        {"english": "perspective", "russian": "точка зрения"},
        {"english": "contribuer", "russian": "вносить вклад"},
        {"english": "convaincre", "russian": "убеждать"},
        {"english": "essentiel", "russian": "необходимый"},
        {"english": "significatif", "russian": "значительный"},
        {"english": "solution", "russian": "решение проблемы"},
    ],
}

SPANISH_WORD_SETS = {
    "A1": [
        {"english": "hola", "russian": "привет"},
        {"english": "libro", "russian": "книга"},
        {"english": "casa", "russian": "дом"},
        {"english": "agua", "russian": "вода"},
        {"english": "escuela", "russian": "школа"},
        {"english": "familia", "russian": "семья"},
        {"english": "amigo", "russian": "друг"},
        {"english": "comer", "russian": "есть"},
        {"english": "beber", "russian": "пить"},
        {"english": "hablar", "russian": "говорить"},
        {"english": "leer", "russian": "читать"},
        {"english": "escribir", "russian": "писать"},
        {"english": "pequeño", "russian": "маленький"},
        {"english": "grande", "russian": "большой"},
        {"english": "feliz", "russian": "счастливый"},
    ],
    "A2": [
        {"english": "viajar", "russian": "путешествовать"},
        {"english": "comprar", "russian": "покупать"},
        {"english": "elegir", "russian": "выбирать"},
        {"english": "empezar", "russian": "начинать"},
        {"english": "entender", "russian": "понимать"},
        {"english": "preguntar", "russian": "спрашивать"},
        {"english": "responder", "russian": "отвечать"},
        {"english": "olvidar", "russian": "забывать"},
        {"english": "conocer", "russian": "знакомиться"},
        {"english": "a menudo", "russian": "часто"},
        {"english": "pronto", "russian": "скоро"},
        {"english": "necesitar", "russian": "нуждаться"},
        {"english": "fácil", "russian": "лёгкий"},
        {"english": "difícil", "russian": "трудный"},
        {"english": "trabajo", "russian": "работа"},
    ],
    "B1": [
        {"english": "mejorar", "russian": "улучшать"},
        {"english": "lograr", "russian": "добиваться"},
        {"english": "consejo", "russian": "совет"},
        {"english": "experiencia", "russian": "опыт"},
        {"english": "medio ambiente", "russian": "окружающая среда"},
        {"english": "costumbre", "russian": "привычка"},
        {"english": "sin embargo", "russian": "однако"},
        {"english": "probablemente", "russian": "вероятно"},
        {"english": "evitar", "russian": "избегать"},
        {"english": "sugerir", "russian": "предлагать"},
        {"english": "decidir", "russian": "решать"},
        {"english": "explicar", "russian": "объяснять"},
        {"english": "comparar", "russian": "сравнивать"},
        {"english": "conocimiento", "russian": "знание"},
        {"english": "oportunidad", "russian": "возможность"},
    ],
    "B2": [
        {"english": "ventaja", "russian": "преимущество"},
        {"english": "consecuencia", "russian": "последствие"},
        {"english": "evidencia", "russian": "доказательство"},
        {"english": "fiable", "russian": "надёжный"},
        {"english": "requerir", "russian": "требовать"},
        {"english": "prevenir", "russian": "предотвращать"},
        {"english": "mantener", "russian": "поддерживать"},
        {"english": "profundizar", "russian": "углублять"},
        {"english": "no obstante", "russian": "тем не менее"},
        {"english": "perspectiva", "russian": "точка зрения"},
        {"english": "contribuir", "russian": "вносить вклад"},
        {"english": "convencer", "russian": "убеждать"},
        {"english": "esencial", "russian": "необходимый"},
        {"english": "significativo", "russian": "значительный"},
        {"english": "solución", "russian": "решение проблемы"},
    ],
}

LANGUAGE_WORD_SETS = {
    "Английский": WORD_SETS,
    "Французский": FRENCH_WORD_SETS,
    "Испанский": SPANISH_WORD_SETS,
}

LANGUAGE_FORMS = {
    "Английский": "английском",
    "Французский": "французском",
    "Испанский": "испанском",
}

LANGUAGE_EXAMPLES = {
    "Английский": "book",
    "Французский": "livre",
    "Испанский": "libro",
}

LANGUAGE_VOICES = {
    "Английский": "en-US",
    "Французский": "fr-FR",
    "Испанский": "es-ES",
}

LANGUAGE_CODES = {
    "Английский": "en",
    "Французский": "fr",
    "Испанский": "es",
}

CUSTOM_WORDS_FILE = Path(__file__).with_name("custom_words.json")
LOGO_FILE = Path(__file__).with_name("language_trainer_logo.png")


def load_custom_words():
    if not CUSTOM_WORDS_FILE.exists():
        return []
    try:
        data = json.loads(CUSTOM_WORDS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            words = []
            for item in data:
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("english"), str)
                    and isinstance(item.get("russian"), str)
                ):
                    language = item.get("language", "Английский")
                    if language not in LANGUAGE_WORD_SETS:
                        language = "Английский"
                    words.append(
                        {
                            "language": language,
                            "english": item["english"],
                            "russian": item["russian"],
                        }
                    )
            return words
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
    st.session_state.results = []
    for key in list(st.session_state):
        if key.startswith("answer_"):
            del st.session_state[key]


def find_saved_translation(text, language, source_code, target_code):
    all_words = []
    for level_words in LANGUAGE_WORD_SETS[language].values():
        all_words.extend(level_words)
    all_words.extend(
        item
        for item in st.session_state.custom_words
        if item.get("language", "Английский") == language
    )

    normalized = text.strip().casefold()
    if source_code == "ru":
        for item in all_words:
            if item["russian"].strip().casefold() == normalized:
                return item["english"]
    else:
        for item in all_words:
            if item["english"].strip().casefold() == normalized:
                return item["russian"]
    return None


@st.cache_data(ttl=86400, show_spinner=False)
def request_translation(text, source_code, target_code):
    query = urlencode(
        {
            "q": text,
            "langpair": f"{source_code}|{target_code}",
        }
    )
    request = Request(
        f"https://api.mymemory.translated.net/get?{query}",
        headers={"User-Agent": "Language-Trainer/1.0"},
    )
    secure_context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, timeout=10, context=secure_context) as response:
        payload = json.loads(response.read().decode("utf-8"))
    translated = payload.get("responseData", {}).get("translatedText", "")
    translated = html.unescape(str(translated)).strip()
    if not translated:
        raise ValueError("Сервис не вернул перевод.")
    return translated


def translate_word(text, language, source_code, target_code):
    saved_translation = find_saved_translation(
        text,
        language,
        source_code,
        target_code,
    )
    if saved_translation:
        return saved_translation
    return request_translation(text, source_code, target_code)


def add_custom_word(language, russian, foreign):
    russian_clean = russian.strip()
    foreign_clean = foreign.strip().lower()
    if any(
        item.get("language", "Английский") == language
        and item["english"].casefold() == foreign_clean.casefold()
        and item["russian"].casefold() == russian_clean.casefold()
        for item in st.session_state.custom_words
    ):
        return False

    st.session_state.custom_words.append(
        {
            "language": language,
            "english": foreign_clean,
            "russian": russian_clean,
        }
    )
    save_custom_words(st.session_state.custom_words)
    return True


def show_pronunciation_button(text, language):
    spoken_text = base64.b64encode(text.encode("utf-8")).decode("ascii")
    voice_code = json.dumps(LANGUAGE_VOICES[language])
    st.iframe(
        f"""
        <button onclick="speakWord()">🔊 Прослушать произношение</button>
        <script>
        function speakWord() {{
            window.speechSynthesis.cancel();
            const bytes = Uint8Array.from(atob("{spoken_text}"), c => c.charCodeAt(0));
            const word = new TextDecoder().decode(bytes);
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = {voice_code};
            utterance.rate = 0.82;
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        <style>
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        button {{
            width: 100%;
            min-height: 48px;
            border: 1px solid rgba(255,255,255,.24);
            border-radius: 14px;
            background: linear-gradient(135deg, #6d5dfc, #2563eb);
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
        }}
        button:hover {{ filter: brightness(1.1); }}
        button:active {{ transform: scale(.99); }}
        </style>
        """,
        height=56,
    )


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
if "results" not in st.session_state:
    st.session_state.results = []

if LOGO_FILE.exists():
    logo_left, logo_center, logo_right = st.columns([1, 1, 1])
    with logo_center:
        st.image(str(LOGO_FILE), width=180)

st.title("Language Trainer")
st.markdown(
    '<p class="subtitle">Изучай языки по уровням или создай свой словарь</p>',
    unsafe_allow_html=True,
)

language = st.sidebar.selectbox(
    "Изучаемый язык",
    list(LANGUAGE_WORD_SETS),
)
section = st.sidebar.radio("Раздел", ["Тренировка", "Мои слова"])

if section == "Мои слова":
    st.subheader(f"Автоматический перевод · {language}")
    foreign_code = LANGUAGE_CODES[language]
    russian_to_foreign = f"Русский → {language}"
    foreign_to_russian = f"{language} → Русский"
    direction = st.radio(
        "Направление перевода",
        [russian_to_foreign, foreign_to_russian],
        horizontal=True,
    )
    source_code, target_code = (
        ("ru", foreign_code)
        if direction == russian_to_foreign
        else (foreign_code, "ru")
    )

    with st.form("translate_word"):
        source_word = st.text_input(
            "Введите слово или короткую фразу",
            max_chars=100,
            placeholder=(
                "Например: книга"
                if direction == russian_to_foreign
                else f"Например: {LANGUAGE_EXAMPLES[language]}"
            ),
        )
        translate_submitted = st.form_submit_button(
            "Перевести",
            use_container_width=True,
        )

    if translate_submitted:
        source_clean = source_word.strip()
        if not source_clean:
            st.warning("Сначала введите слово.")
        else:
            try:
                with st.spinner("Перевожу…"):
                    translated = translate_word(
                        source_clean,
                        language,
                        source_code,
                        target_code,
                    )
                st.session_state.pending_translation = {
                    "language": language,
                    "direction": direction,
                    "source": source_clean,
                    "translated": translated,
                }
            except Exception:
                st.session_state.pop("pending_translation", None)
                st.error(
                    "Не удалось получить перевод. Проверьте интернет "
                    "и попробуйте ещё раз."
                )

    pending = st.session_state.get("pending_translation")
    if pending and (
        pending["language"] != language or pending["direction"] != direction
    ):
        st.session_state.pop("pending_translation", None)
        pending = None

    if pending:
        st.success(f'Перевод: **{pending["translated"]}**')
        if direction == russian_to_foreign:
            russian_word = pending["source"]
            foreign_word = pending["translated"]
        else:
            russian_word = pending["translated"]
            foreign_word = pending["source"]

        if st.button("Добавить в мой словарь", use_container_width=True):
            try:
                if add_custom_word(
                    language,
                    russian_word,
                    foreign_word,
                ):
                    st.success("Слово добавлено и сохранено.")
                    st.session_state.pop("pending_translation", None)
                else:
                    st.info("Такое слово уже есть в вашем словаре.")
            except OSError:
                st.error("Не удалось сохранить файл со словами.")

    st.caption(
        "Для незнакомых приложению слов используется онлайн-сервис перевода."
    )

    custom_words = [
        item
        for item in st.session_state.custom_words
        if item.get("language", "Английский") == language
    ]
    st.subheader(f"Ваш словарь: {len(custom_words)} слов")
    if custom_words:
        for number, item in enumerate(custom_words, start=1):
            st.write(f'{number}. {item["russian"]} — {item["english"]}')
    else:
        st.info("Пока здесь нет слов. Добавьте первое слово выше.")
    st.stop()

level = st.selectbox(
    "Выберите набор слов",
    ["A1", "A2", "B1", "B2", "Мои слова"],
)

training_key = f"{language}:{level}"
if st.session_state.get("last_training") != training_key:
    st.session_state.last_training = training_key
    reset_training()

custom_words = [
    item
    for item in st.session_state.custom_words
    if item.get("language", "Английский") == language
]
words = (
    custom_words
    if level == "Мои слова"
    else LANGUAGE_WORD_SETS[language][level]
)

if not words:
    st.info("Сначала добавьте слова в разделе «Мои слова».")
    st.stop()

if st.session_state.index >= len(words):
    percent = round(st.session_state.score / len(words) * 100)
    mistakes = [item for item in st.session_state.results if not item["correct"]]
    if percent >= 90:
        result_message = "Отличный результат!"
    elif percent >= 70:
        result_message = "Хороший результат — осталось немного повторить."
    elif percent >= 50:
        result_message = "Неплохо! Повтори слова с ошибками."
    else:
        result_message = "Продолжай тренироваться — результат обязательно улучшится."

    st.subheader("🏆 Результат тренировки")
    score_column, percent_column, mistakes_column = st.columns(3)
    score_column.metric("Правильно", f"{st.session_state.score}/{len(words)}")
    percent_column.metric("Результат", f"{percent}%")
    mistakes_column.metric("Ошибки", len(mistakes))
    st.success(result_message)

    if mistakes:
        st.subheader("Слова для повторения")
        for item in mistakes:
            user_answer = item["user_answer"] or "нет ответа"
            st.write(
                f'• **{item["russian"]}** — {item["answer"]} '
                f'_(ваш ответ: {user_answer})_'
            )
    else:
        st.info("Все ответы правильные — ошибок нет!")

    st.balloons()
    if st.button("Пройти ещё раз", use_container_width=True):
        reset_training()
        st.rerun()
    st.stop()

word = words[st.session_state.index]
answer_key = f"answer_{language}_{level}_{st.session_state.index}"
display_word = html.escape(word["russian"])

st.markdown(
    f'<div class="score">Очки: {st.session_state.score} · '
    f'Слово {st.session_state.index + 1} из {len(words)}</div>',
    unsafe_allow_html=True,
)
st.progress(st.session_state.index / len(words))
st.markdown(
    f"""
    <div class="word-card">
        <div class="level">{language.upper()} · УРОВЕНЬ {level}</div>
        <div class="russian-word">{display_word}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

answer = st.text_input(
    f"Введите перевод на {LANGUAGE_FORMS[language]}:",
    key=answer_key,
    disabled=st.session_state.answered,
    placeholder=f"Например: {LANGUAGE_EXAMPLES[language]}",
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
            st.session_state.results.append(
                {
                    "russian": word["russian"],
                    "answer": word["english"],
                    "user_answer": cleaned_answer,
                    "correct": st.session_state.correct,
                }
            )
            st.rerun()

if st.session_state.answered:
    if st.session_state.correct:
        st.success("Правильно! Отличная работа.")
    else:
        st.error(f'Неверно. Правильный ответ: {word["english"]}')

    show_pronunciation_button(word["english"], language)

    if st.button("Следующее слово →", use_container_width=True):
        st.session_state.index += 1
        st.session_state.answered = False
        st.session_state.correct = False
        st.rerun()
