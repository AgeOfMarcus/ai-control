from subprocess import check_output, CalledProcessError
try:
    from flask import Flask, request
except ImportError:
    print('Please install flask using pip install flask')
    exit(1)


sh = lambda cmd: check_output(cmd.split(" ")).decode()

app = Flask(__name__)

@app.route("/")
async def app_get():
    return 'use /run for running cmds'

@app.route("/run", methods=['POST'])
def app_post():
    cmd = request.json['cmd']
    try:
        return sh(cmd)
    except CalledProcessError as e:
        return e.output.decode()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)