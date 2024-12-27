from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')

def summarize_data(df):
    column_metadata = {}

    for column in df.columns:
        column_metadata[column] = {
            "data_type": str(df[column].dtype),
            "unique_values": df[column].dropna().unique().tolist()
        }

    summary = {
        "columns": list(df.columns),
        "metadata": column_metadata,
    }
    return summary

def generate_embeddings(df_summary):
    embeddings = {
        "columns": {},
        "unique_values": {}
    }

    for col in df_summary["columns"]:
        embeddings["columns"][col] = model.encode(col, convert_to_tensor=True)

    # Encode unique values
    for col, meta in df_summary["metadata"].items():
        embeddings["unique_values"][col] = {
            value: model.encode(str(value), convert_to_tensor=True)
            for value in meta["unique_values"]
        }

    return embeddings

def handle_query(query, df_summary, embeddings):
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Match columns
    column_scores = {
        col: cosine_similarity(
            [query_embedding],
            [embeddings["columns"][col]]
        )[0][0] for col in embeddings["columns"]
    }

    relevant_columns = [
        col for col, score in sorted(column_scores.items(), key=lambda x: x[1], reverse=True) if score > 0.5
    ]

    relevant_unique_values = {}
    for col in relevant_columns:
        value_scores = {
            value: cosine_similarity(
                [query_embedding],
                [embedding]
            )[0][0] for value, embedding in embeddings["unique_values"][col].items()
        }

        relevant_unique_values[col] = [
            value for value, score in sorted(value_scores.items(), key=lambda x: x[1], reverse=True) if score > 0.5
        ]

    return {
        "relevant_columns": relevant_columns,
        "relevant_unique_values": relevant_unique_values
    }
