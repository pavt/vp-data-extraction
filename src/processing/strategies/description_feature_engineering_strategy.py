import nltk
import pandas as pd
from collections import Counter
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# 🔹 Asegurar que los recursos de NLTK están disponibles
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
     

# Cargar stopwords en inglés
stop_words = set(stopwords.words('english'))

# Inicializar el Stemmer y Lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

class DescriptionFeatureEngineeringStrategy:
    """
    Estrategia para extraer características de la columna `description`
    con tokenización, stemming, lematización y eliminación de stopwords.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        print("🛠️ [Capa 6] Extrayendo características de la descripción...")

        bigram_col, trigram_col = [], []

        for index, row in df.iterrows():
            if pd.notna(row["description"]):
                try:
                    # 🔹 Tokenización y preprocesamiento en una sola línea
                    words = [word.lower() for word in word_tokenize(row["description"]) if word.isalnum() and word.lower() not in stop_words]

                    # 🔹 Aplicar stemming y lematización
                    stemmed_tokens = [stemmer.stem(word) for word in words]  # Stemming
                    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in stemmed_tokens]  # Lematización

                    # 🔹 Generar bigramas y trigramas
                    bigrams = list(ngrams(lemmatized_tokens, 2))
                    trigrams = list(ngrams(lemmatized_tokens, 3))

                    # 🔹 Obtener los más comunes
                    most_common_bigram = Counter(bigrams).most_common(1)
                    most_common_trigram = Counter(trigrams).most_common(1)

                    bigram_col.append(" ".join(most_common_bigram[0][0]) if most_common_bigram else "")
                    trigram_col.append(" ".join(most_common_trigram[0][0]) if most_common_trigram else "")

                except Exception as e:
                    print(f"⚠️ Error procesando descripción en índice {index}: {e}")
                    bigram_col.append("")
                    trigram_col.append("")
            else:
                bigram_col.append("")
                trigram_col.append("")

        # Agregar las columnas al DataFrame
        df["desc_bigram_most_common"] = bigram_col
        df["desc_trigram_most_common"] = trigram_col

        print("✅ Características de la descripción extraídas correctamente.")
        return df
