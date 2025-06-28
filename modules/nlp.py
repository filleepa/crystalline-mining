from bertopic import BERTopic
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def PCA_embeddings(embeddings):
    """Takes in embeddings and reduces dimentionality, selecting enough components to explain 90% of the variance."""
    pca = PCA(n_components=0.9, random_state=42)
    embeddings_pca = pca.fit_transform(embeddings)
    print(f"PCA reduced from {embeddings.shape} to {embeddings_pca.shape}")
    print(f"Number of components chosen:", pca.n_components_)
    
    return embeddings_pca

def tsne_embeddings(embeddings_pca):
    """Takes in reduced PCA embeddings and further reduces dimentionality to 2."""
    tsne = TSNE(
        n_components=2,
        perplexity=10,
        learning_rate=200,
        n_iter=1000,
        random_state=42
    )
    embeddings_tsne_2d = tsne.fit_transform(embeddings_pca)
    print(f"TSNE reduced dimentionality from {embeddings_pca.shape} to {embeddings_tsne_2d.shape}")
    
    return embeddings_tsne_2d


