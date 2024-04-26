# Data collection and preparation

## data format proposal

```
{"input_text":"Schema:\n(:Person {label: 'Person',id: string, role: string, description: string})-[:HAS_SKILL {}]->(:Skill {label:'Skill', id: string,name: string,level: string})\n(:Person {label: 'Person',id: string, role: string, description: string})-[:HAS_EDUCATION {}]->(:Education {label:'Education', id: string, degree: string, university: string, graduationDate: string, score: string, url: string})\nQuestion: How many java developers attend more than one universities?",

"output_text":"MATCH (p:Person)-[:HAS_SKILL]->(s:Skill), (p)-[:HAS_EDUCATION]->(e1:Education), (p)-[:HAS_EDUCATION]->(e2:Education) WHERE toLower(s.name) CONTAINS 'java' AND e1.university <> e2.university RETURN COUNT(DISTINCT p)
"}
```
