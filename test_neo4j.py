from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"   # same password you set in Neo4j Desktop

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("CREATE (m:Movie {name:'Inception'}) RETURN m")
    for record in result:
        print(record)

print("Neo4j connected successfully!")
driver.close()