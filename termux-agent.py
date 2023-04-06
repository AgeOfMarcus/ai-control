from subprocess import check_output, CalledProcessError
try:
    from fastapi import FastAPI, Request
except ImportError:
    print('Please install fastapi using pip install fastapi')
    exit(1)
try:
    import uvicorn
except ImportError:
    print('Please install uvicorn using pip install uvicorn')
    exit(1)

sh = lambda cmd: check_output(cmd.split(" ")).decode()

app = FastAPI()

@app.get("/")
async def app_get():
    return 'use /run for running cmds'

@app.post("/run")
async def app_post(request: Request):
    data = request.json()
    cmd = data['cmd']
    try:
        return sh(cmd)
    except CalledProcessError as e:
        return e.output.decode()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)