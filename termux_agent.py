from subprocess import Popen, PIPE, CalledProcessError
try:
    from flask import Flask, request
except ImportError:
    print('Please install flask using pip install flask[async]')
    exit(1)


sh = lambda cmd: Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].decode()

app = Flask(__name__)

@app.route("/")
async def app_get():
    return 'use /run for running cmds'

@app.route("/run", methods=['POST'])
def app_post():
    cmd = request.json['cmd']
    try:
        return {'output': sh(cmd)}
    except CalledProcessError as e:
        return {'error': e.output.decode()}

@app.route('/shutdown')
def shutdown_server():
    print('Server shutting down...')
    fn = request.environ.get('werkzeug.server.shutdown')
    try:
        fn() # idk if it needs to be called
    except:
        pass
    return 'ok'

def main(host='127.0.0.1', port=8080):
    app.run(host=host, port=port)

if __name__ == '__main__':
    main()
