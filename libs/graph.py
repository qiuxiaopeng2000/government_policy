from py2neo import Graph
import pandas as pd

graph = Graph('http://localhost:7474/', username='neo4j', password='sb1234567890SB')

CSV_1 = pd.read_csv('E:\\Desktop\\新建文件夹\\country.csv', error_bad_lines=False, encoding='utf-8')
