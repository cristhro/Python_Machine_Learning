from flask import Flask, jsonify, request, render_template, make_response
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template(
        'index.html'
    )

@app.route('/buscar', methods = ["POST"])
def buscar():
    buscado = request.form['buscado']
    resultado = realizar_busqueda_2(buscado)
    return jsonify({
        'resultado': resultado
    })
def realizar_busqueda_2(buscado):

    bodyQuery2 = {
        "query": {
            "match": {
                "Title": {
                    "query": buscado,
                    "fuzziness": "AUTO",
                    "operator": "and"
                }
            }
        },
        "highlight": {
            "fields": {
                "Title": {},
                "Plot": {"fragment_size": 300, "number_of_fragments": 3}
            },
            # Permite el hightlight sobre campos que no se han hecho query
            # como Plot en este ejemplo
            "require_field_match": False
        }
    }
    res = es.search(index="prueba-index", body= bodyQuery2)
    print("Got %d Hits:" % res['hits']['total'])
    # Uso el [0] porque solo hay 1 hit, si hubiese mas, pues habria mas campos
    # de la lista, habria que usar el for de arriba para sacar el highlight de
    # cada uno de la lista
    # print res['hits']['hits'][0]['highlight']

    resultado = []
    for hit in res['hits']['hits']:
        resultado.append(hit['highlight'])

    return resultado
def realizar_busqueda(buscado):
    bodyQuery = {
        "query": {
            "match": {
                "Director": {
                    "query": buscado,
                    "fuzziness": "AUTO",
                    "operator": "and"
                }
            }
        },
        "highlight": {
            "fields": {
                "Title": {},
                "Plot": {}
            }
        }
    }
    res = es.search(index="prueba-index", body= bodyQuery)
    print("Got %d Hits:" % res['hits']['total'])

    resultado = []
    for hit in res['hits']['hits']:
        resultado.append("%(Title)s" % hit["_source"])

    return resultado
if __name__ == '__main__':
    app.run(debug=True)
