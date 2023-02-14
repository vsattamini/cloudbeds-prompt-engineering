import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
            frequency_penalty=0.05,
            max_tokens=1500,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Write a good prompt for an artificial intelligence system that creates images from text (DALL-E 2). The image is the cover for an article about {}.

Here are three typical prompts:

1. "A vast sky with various glowing strings of memories shaping an enormous aurora borealis like glowing foliage, white, orange, extremely beautiful, beautiful universe twist, beautiful nightfall, cinematic lighting, beautiful field, high definition, high quality, hyper detail."

2. "Kneeling cat knight, portrait, finely detailed armor, intricate design, silver, silk, cinematic lighting, 4k."

3. "Ultra sharp award winning underwater nature photography of a woman riding a glistening gradient sea horse, backlit, depth of field, ocean floor, lush vegetation, particles, solar rays, coral, golden fishes, under water fashion photography, woman riding a seahorse, ultra sharp award winning photography."

You can use different words or concepts. Write just one prompt.""".format(
        animal.capitalize()
    )
