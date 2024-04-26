# 自然语言转图查询语言的增强微调
## 选题分析
### Graph Query Language语言选择
Graph Query language 2000年后才被发明，因此没有像SQL一样经历50年发展，早已经完成了ISO标准化。常见的竞品包括但不限于 Gremlin, Sparql, AQL, nGQL, GraphQL, cypher/opencypher等， 以上这些语言各有其侧重点与优势。

就在2024年4月，iso-GQL标准正式发布，但是还没有厂家能够完全支持。 opencypher被认为是iso-GQL的蓝本，目前市占率最大的neo4j, 阿里开源的Tugraph等都以cypher其作为输入语言, 同时两家都表示将尽快完成iso-GQL标准支持。出于应用广泛度与开发者的技术力量的角度考虑， 本研究将以cypher作为NL2GQL语言选择。所有代码将以在当前Neo4j community版与Tugraph开源版成功运行返回正确为基准。

### Text2Cypher 现状
已经有一些前人研究如
[SpCQL: A Semantic Parsing Dataset for Converting Natural Language into Cypher(2022)](https://ir.webis.de/anthology/2022.cikm_conference-2022.406/)
构建并开源了多达10,000条中文描述与Cypher Query的数据对， 但是受限数据质量不高与当时技术限制，最后验证准确率仅有2%。

[𝑅3-NL2GQL: A Hybrid Models Approach for for Accuracy Enhancing and Hallucinations Mitigation(2023)](https://arxiv.org/abs/2311.01862)
采用多种手段增强数据，包含cypher语言分析，训练中引入Schema，Reasoning，尤为值得学习实践。

[Aligning Large Language Models to a Domain-specific Graph Database(2024)](https://arxiv.org/abs/2402.16567)
自己构建了 FinGQL and MediGQL领域数据集，给出采集数据的来源但没有给出数据集，根据文章所述，经过微调后的模型Schema理解能力大提升，超越当时的商业化大模型。

现在Neo4j的资深工程师 [Tomaz Bratanic](https://bratanic-tomaz.medium.com/) 在寻求更多数据，基于GPT-4模型提升Text2Cypher能力的实践。

同时Huggingface上有人在尝试基于大模型微调Text2Cypher,但没有文档与数据来源的说明。

商业化大模型对cypher语法有训练， 但输入Schema后提问获得Query得到准确率并不高, 有很大的进步空间。

举例：
```
Write cypher code based on following Schema and Question
Schema:

(:Person {label: 'Person',id: string, role: string, description: string})-[:HAS_EDUCATION {}]->(:Education {label:'Education', id: string, degree: string, university: string, graduationDate: string, score: string, url: string})

Question: How many java developers attend more than one universities? Return code only!

```


**百度文心**
```cypher
MATCH (p:Person)-[:HAS_EDUCATION]->(e:Education)
WHERE p.role = 'Developer' AND e.degree CONTAINS 'Java'
WITH p, COLLECT(DISTINCT e.university) AS universities
WHERE size(universities) > 1
RETURN count(p)

```


**gpt-3.5-turbo:**
```cypher
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: \"Java\"})
WITH p, count(DISTINCT p)-[:HAS_EDUCATION]->(e:Education)
 as numUniversities
WHERE numUniversities > 1
RETURN count(p) as numJavaDevelopersMultipleUniversities
```

**gpt-4-turbo**
```cypher
MATCH (p:Person {role: \"Java Developer\"})-[:HAS_EDUCATION]->(e:Education)
WITH p, COUNT(DISTINCT e.university) AS universitiesCount
WHERE universitiesCount > 1
RETURN COUNT(p) AS JavaDevelopersWithMultipleUniversities
```

百度文心没有理会Schema， GPT采用了但对schema的理解都出现了误判， 而且各不相同。

究其原因可能是已有研究的数据集缺乏， 没有结合Schema进行训练，或者需要更多手段辅助训练。 现有大模型Text2Cypher输出难以直接应用， 同时也缺乏可靠的评测标准。

另一方面作为一种声明式查询语言， cypher的语法结构与SQL有诸多相似之处，而Text2SQL已有可观的数据集、增强工具与评测标准，将可以为Text2Cypher的数据集收集与评测构建带来启发。能否找到办法有效利用Text2SQL丰富资源，克服cypher的资源匮乏，是本次研究一大重点与难点。


# 研究任务
## 核心任务：收集数据，微调InternLM2 20b模型， 使其更好的完成Text2Cypher任务，

1. 丰富数据集，人工收集之外，也尝试通过其他LLM增强生成， 已有的Text2SQL研究成果迁移生成；
2. 建立对代码验证的Pipeline, 确保代码能够在neo4j，Tugraph有效运行；
3. 初步对问题的难度进行量化，拟定评测标准，建立评测办法；
4. 划分数据集，开始微调训练；
5. 验证，总结，提高。

## 可能的拓展：对错误语句的reasoning, debug分析
## 可能的拓展: 基于自然语言调用建模的下游图任务， 比如依赖分析， 路径分析等
## 可能的拓展: 接入Agent工作流， 并增加GuardRails确保其查询的数据安全性
