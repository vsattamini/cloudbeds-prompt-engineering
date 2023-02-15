import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        subject = request.form["model-selection"]
        initial = request.form["subject"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(initial, subject),
            temperature=0.8,
            frequency_penalty=0.05,
            max_tokens=1500,
        )
        if subject == 'Image Generation':
            res = createImageFromPrompt(response.choices[0].text)
        else:
            res=[{'url':'static/open-ai-logo-3.png'}]

        return redirect(url_for("index", result=response.choices[0].text, image=res[0]['url']))
    result = request.args.get("result")
    image = request.args.get("image")


    # if request.method == "POST":
    #     images = []
    #     res = createImageFromPrompt(result)
    #     if len(res) > 0:
    #         for img in res:
    #             images.append(img['url'])
    #     return redirect(url_for("index", image=res[0]['url']))
    # images = request.args.get("image")

    return render_template("index.html", result=result,image=image, data=[{'name':'Image Generation'}, {'name':'Historical Text'}, {'name':'Scientific Articles'}])


def generate_prompt(initial, subject):

    if subject == 'Image Generation':
        return """Write a good prompt for an artificial intelligence system that creates images from text (DALL-E 2). The image is the cover for an article about {}.

Here are three typical prompts:

1. "A vast sky with various glowing strings of memories shaping an enormous aurora borealis like glowing foliage, white, orange, extremely beautiful, beautiful universe twist, beautiful nightfall, cinematic lighting, beautiful field, high definition, high quality, hyper detail."

2. "Kneeling cat knight, portrait, finely detailed armor, intricate design, silver, silk, cinematic lighting, 4k."

3. "Ultra sharp award winning underwater nature photography of a woman riding a glistening gradient sea horse, backlit, depth of field, ocean floor, lush vegetation, particles, solar rays, coral, golden fishes, under water fashion photography, woman riding a seahorse, ultra sharp award winning photography."

You can use different words or concepts. Write just one prompt.

""".format(
        initial.capitalize()
    )

    if subject == 'Historical Text':
        intermediate_descriptors = openai.Completion.create(
            model="text-davinci-003",
            prompt="""
            Complete the following list with 5 adjectives describing the civilization that is incomplete. There are 4 examples to base yourself on:

            1. Brazil - Festive, Jolly, Large, diverse, sporty
            2. Greece - Cultured, democratic, fragmented, ancient, philosophical
            3. Assyria - Violent, domineering, warmongering, efficient, strong
            4. Aztec - Sacrificing, violent, native, brave, domineering
            {}:
            """.format(initial.capitalize()),
            temperature=1.5,
            frequency_penalty=0.05,
            max_tokens=1500,
        )
        intermediate_format = openai.Completion.create(
            model="text-davinci-003",
            prompt="""
            What was the dominant form of narrative in the following culture in five or less words, with an added adjective:{}
            """.format(initial.capitalize()),
            temperature=0.1,
            frequency_penalty=0.05,
            max_tokens=1500,
        )

        what_about = openai.Completion.create(
            model="text-davinci-003",
            prompt="""
            Generate an unusual and unexpected historical topic that could serve as the basis for a fake historical text. The topic should be quirky, offbeat, and unlikely, but also interesting and engaging. The text should capture the reader's attention and imagination with its vivid imagery, compelling narrative, and intriguing details. Some examples might include competitive yoga, the banana revolution, or the wheel conspiracy.
            """,
            temperature=1,
            frequency_penalty=0.05,
            max_tokens=1500,
        )


        return f"Write a piece of {intermediate_format} in the style of the people of {initial}. The piece should reflect values of a {intermediate_descriptors} society. The piece should be about {what_about}."


    if subject == 'Scientific Articles':
        final = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""Please provide only 3 groundbreaking ideas for scientific articles on {initial}
            that disrupt traditional ways of thinking and draw on multiple disciplines.
            The emphasis should be on creative and bold article titles that catalyze
            conversation rather than a deep dive into the research, breaking new ground
            and leading to better and more interesting research. Please remember to only generate 3 ideas""",
            temperature=1,
            frequency_penalty=0.05,
            max_tokens=1500,
        )
        return final.choices[0].text

def createImageFromPrompt(prompt):
    response = openai.Image.create(prompt=prompt, n=3, size="512x512")
    return response['data']
