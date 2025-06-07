import json
from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATA_FILE = 'flashcards.json'

def load_flashcards():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_flashcards(cards):
    with open(DATA_FILE, 'w') as f:
        json.dump(cards, f)

flashcards = load_flashcards()

def get_current_index():
    return session.get('current_index', 0)

@app.route("/", methods=["GET", "POST"])
def home():
    if not flashcards:
        return render_template("flashcard.html", question="No flashcards. Add a new one!", answer="", show_answer=False, no_cards=True)
    idx = get_current_index()
    card = flashcards[idx]
    show_answer = session.get('show_answer', False)
    return render_template(
        "flashcard.html",
        question=card["question"],
        answer=card["answer"],
        show_answer=show_answer,
        no_cards=False
    )

@app.route("/flip", methods=["POST"])
def flip():
    session['show_answer'] = True
    return redirect(url_for('home'))

@app.route("/skip", methods=["POST"])
def skip_card():
    if flashcards:
        idx = random.randint(0, len(flashcards)-1)
        session['current_index'] = idx
        session['show_answer'] = False
    return redirect(url_for('home'))

@app.route("/add", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        if question and answer:
            flashcards.append({"question": question, "answer": answer})
            save_flashcards(flashcards)
            session['current_index'] = len(flashcards) - 1
            session['show_answer'] = False
            return redirect(url_for('home'))
    return render_template("add_card.html")

@app.route("/delete", methods=["POST"])
def delete_card():
    if flashcards:
        idx = get_current_index()
        flashcards.pop(idx)
        save_flashcards(flashcards)
        session['current_index'] = 0
        session['show_answer'] = False
    return redirect(url_for('home'))

@app.route("/list")
def list_questions():
    questions = [card["question"] for card in flashcards]
    return render_template("list_questions.html", questions=questions)


if __name__ == '__main__':
    app.run(debug=True)
