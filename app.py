from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def precedence(op):
    if op in ['+', '-']:
        return 1
    if op in ['*', '/']:
        return 2
    if op == '^':
        return 3
    return 0

def infix_to_postfix_steps(infix):
    stack = []
    output = ""
    steps = []

    for ch in infix:
        if ch.isalnum():
            output += ch
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(ch):
                output += stack.pop()
            stack.append(ch)

        steps.append({"symbol": ch, "stack": stack.copy(), "output": output})

    while stack:
        output += stack.pop()
        steps.append({"symbol": "", "stack": stack.copy(), "output": output})

    return output, steps

@app.route("/infixtopostfix/suchint", methods=["GET", "POST"])
def index():
    postfix = ""
    steps = []

    if request.method == "POST":
        infix = request.form.get("infix", "")
        postfix, steps = infix_to_postfix_steps(infix)

    return render_template("index.html", postfix=postfix, steps=steps)

if __name__ == "__main__":
    app.run(debug=True)
