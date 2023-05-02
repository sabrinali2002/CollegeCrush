import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import test

"""
Returns a new dataframe that contains only personality related words
"""
def getTFIDF(df, name, word):
    try:
        return df.loc[df['University Name'] == name.title()].loc[:,word].values[0]
    except:
        return 0

def getDataframe(college_data_path):
    # dataframe of whole dataset
    df = pd.read_csv(college_data_path)
    # Loop through each college's tf-idf matrix and extract only the personality-related terms
    new_data = []
    for i in range(len(df)):
        college_data = df.iloc[i, 2:]  # Get the tf-idf scores for this college
        college_personality_data = college_data[
            personality_terms
        ]  # Extract only the personality-related terms
        new_data.append(college_personality_data)

    # Create a new dataframe with the extracted data
    new_df = pd.DataFrame(new_data, columns=personality_terms)

    return new_df


"""
Input: 
    A list of personality related words
    A personality word only dataframe

Output:
    labels: an array of each colleges clusters. e.g. [1,2,3] means college at index 0 belongs to cluster 1.
    college represented by index 1 belongs to cluster2 ...

    Sorted_clusters: A dictionary whose keys are integers from 0 to 39 enumerating the clusters.
and values are lists of colleges that belong to each cluster
"""


def cluster(personality_terms, college_data_path, new_df):
    df = pd.read_csv(college_data_path)
    # Determine the number of clusters
    num_clusters = 40

    # Create KMeans model with the desired number of clusters
    kmeans_model = KMeans(n_clusters=num_clusters)

    # Cluster the colleges
    kmeans_model.fit(new_df)

    # Evaluate the quality of the clusters using the silhouette score
    labels = kmeans_model.labels_

    college_names = df.iloc[:, 1]

    clusters = {}
    for i in range(len(labels)):
        if labels[i] in clusters:
            clusters[labels[i]].append(college_names[i])
        else:
            clusters[labels[i]] = [college_names[i]]

    sorted_clusters = {k: clusters[k] for k in sorted(clusters.keys())}

    return labels, sorted_clusters

"""
Takes in a Dataframe and labels which is a global variable set inside cluster function, and outputs the silhouette score 
which can be used for displaying something like "Your similarity with these colleges are [score] %
"""


def s_score(df, labels):
    score = silhouette_score(new_df, labels)
    score = (score + 1.0) / 2 * 100
    return score


"""
Input: 

    df: The old, unprocessed dataframe
    new_df: dataframe that has only personality related words
    Clusters: the dictionary output by cluster function
    User_input: a list of personality related words input by user

Output:
    Cluster_number: an Integer that indicates which cluster has the highest similarity with user input
    cluster_sim_score: an float that represents the average cosine similarity between user input and its
    most similar clusters of colleges

"""
def cosine_similarity1(df, new_df, clusters, user_input):
    personality_words = new_df.columns
    vectorizer = TfidfVectorizer()
    vectorizer.fit(personality_words)
    user_tfidf = vectorizer.transform(user_input)
    # calculate the cosine similarity between user input and each college

    similarity_scores = cosine_similarity(user_tfidf, new_df.values)
    return similarity_scores

def find_cluster(df, new_df, clusters, user_input):
    college_names = df.iloc[:, 1]
    similarity_scores = cosine_similarity1(df, new_df, clusters, user_input)

    cluster_number = -1
    cluster_max_sim_score = -1
    for cluster_i, colleges in clusters.items():
        score = 0
        for college in colleges:
            college_index = df.loc[college_names == college]["index"].values[0]
            score += similarity_scores[0][college_index]
        size = len(colleges)
        avg_score = score / float(size)
        if avg_score > cluster_max_sim_score:
            cluster_max_sim_score = avg_score
            cluster_number = cluster_i

    return cluster_number, cluster_max_sim_score


def get_result(input):
    most_sim_cluster, sim_score = find_cluster(
        pd.read_csv(path), new_df, clusters, input
    )
    return clusters[most_sim_cluster], sim_score


# just some tests
personality_terms = test.get_words()
# user_input = ['sad']
path = "X1_with_labels.csv"
df = pd.read_csv(path)
new_df = getDataframe(path)
labels, clusters = cluster(personality_terms, path, new_df)
s_score = s_score(new_df, labels)
