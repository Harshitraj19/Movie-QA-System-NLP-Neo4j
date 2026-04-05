#Overview
This project implements a Movie Question Answering (QA) System that leverages Natural Language Processing (NLP) techniques and Graph Databases to answer queries based on a large movie dataset. It processes over 200,000 movie records from TMDB and builds a knowledge graph using Neo4j, a graph database. The system enables users to ask questions such as "Who directed Inception?" or "What are the top-rated action movies?", and retrieve answers in real time using Cypher, Neo4j’s query language.

#Features
Data Collection and Preparation: Collected over 200,000 movie records from the TMDB API, cleaned, and processed using Python.
Triples Extraction with NLP: Utilized spaCy and Stanford CoreNLP to extract subject-predicate-object triples (e.g., "Director - Christopher Nolan").
Entity-Relation Mapping: Mapped extracted triples to entities like movies, directors, genres, etc., and relationships like "directed by".
Knowledge Graph Construction: Built a knowledge graph in Neo4j to store entities and their relationships. Utilized Neo4j Admin Bulk Import for efficient large-scale data import (~2.2M nodes, ~7.8M relationships).
Natural Language Query Parsing: A Flask-based web interface allows users to ask queries in natural language. The system parses the input query for execution.
Cypher Query Generation and Execution: Converted parsed queries into Cypher queries, executed on the Neo4j graph to return results such as directors, genres, or top-rated movies.

#Technologies Used
 -Programming Languages:
  Python: Data processing, NLP tasks (with spaCy and Stanford CoreNLP), and interaction with Neo4j.
  JavaScript: Web interface built using Flask for real-time user interaction.

 -Libraries and Frameworks:
  Flask: Framework for the web application that interacts with the QA system.
  spaCy and Stanford CoreNLP: NLP libraries for extracting triples from movie overviews.
  pandas: Used for cleaning and structuring the movie data.

  -Databases:
  Neo4j: Graph database used to represent movie data and relationships as nodes and edges.
  MongoDB: Used for storing raw movie data before processing into Neo4j.

  -Tools:
  Cypher: Query language used to query the graph database.
  Neo4j Admin Bulk Import: Tool for efficiently importing large datasets into Neo4j.
  Stanza: Python NLP library for extracting semantic triples.
