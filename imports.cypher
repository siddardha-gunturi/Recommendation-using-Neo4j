LOAD CSV WITH HEADERS FROM "file:///movies.csv" AS line
 MERGE (m:Movie{ id:line.movieId, title:line.title}) 
 FOREACH (gName in split(line.genres, '|') | 
    MERGE (g:Genre {name:gName}) 
    MERGE (m)-[:IS_GENRE]->(g)
)


LOAD CSV WITH HEADERS FROM "file:///ratings.csv" AS line
 MATCH (m:Movie {id:line.movieId})
 MERGE (u:User {id:line.userId})
 MERGE (u)-[:RATED { rating: toFloat(line.rating)}]->(m);


LOAD CSV WITH HEADERS FROM "file:///tags.csv" AS line
 MATCH (m:Movie {id:line.movieId})
 MATCH (u:User {id:line.userId})
 CREATE (u)-[:TAGGED { tag: line.tag}]->(m);

LOAD CSV WITH HEADERS FROM "file:///links.csv" AS line
MATCH (m:Movie {id:line.movieId})
SET m.tmdbId=line.tmdbId;


LOAD CSV WITH HEADERS FROM "file:///directors.csv" AS line
MATCH (m:Movie{ tmdbId:line.movieId})
MERGE (p:Person{name:line.person_name})
MERGE (p)-[:DIRECTED]->(m);


LOAD CSV WITH HEADERS FROM "file:///roles.csv" AS line
MATCH (m:Movie{ tmdbId:line.movieId})
MERGE (p:Person{name:line.person_name})
CREATE (p)-[r:ACTED_IN] ->(m)
SET  r.role= line.role;


