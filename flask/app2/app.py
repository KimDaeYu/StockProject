from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app, version='1.0', title='API title',
          description='A simple API',
          )

ns = api.namespace('custom', description='operations')

app.config.SWAGGER_UI_DOC_EXPANSION = 'full'

@ns.route('/<string:text>')
@ns.response(200, 'Found')
@ns.response(404, 'Not found')
@ns.response(500, 'Internal Error')
@ns.param('text', 'String value')
class Algorithm(Resource):
    @ns.doc('get')
    def get(self, text):
        return {"text": "hello,world"}

    @ns.doc('delete')
    def delete(self, id):
        return '', 204

    @ns.doc('put')
    def put(self, id):
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)