import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import re

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-davinci-003"

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        subject = request.form["model-selection"]
        initial = request.form["subject"]
        response = openai.Completion.create(
            model=MODEL,
            prompt=generate_prompt(initial, subject),
            temperature=0.8,
            frequency_penalty=0.05,
            max_tokens=1500,
        )
        if subject == 'Image Generation':
            res = createImageFromPrompt(response.choices[0].text, subject=subject)
        elif subject == 'Playlist Creator':
            res = createImageFromPrompt(response.choices[0].text, subject=subject, initial=initial)
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

    return render_template("index.html", result=result,image=image, data=[{'name':'Image Generation'}, {'name':'Historical Text'}, {'name':'Scientific Articles'}, {'name':'Playlist Creator'}])


@app.route("/rpg", methods=("GET", "POST"))
def rpg():
    if request.method == "POST":
        subject = request.form["model-selection"]
        initial = request.form["subject"]
        response = openai.Completion.create(
            model=MODEL,
            prompt=generate_prompt(initial, subject),
            temperature=0.8,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=1024
        )
        if subject == 'Character Image Generator' or subject == 'Playlist Creator':
            res = createImageFromPrompt(response.choices[0].text, subject)
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

    return render_template("index.html", result=result,image=image, data=[{'name':'Character Image Generator'}])


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

    if subject == 'Character Image Generator':
        return """Write a good prompt for an artificial intelligence system that creates images from text (DALL-E 2). The image is of a tabletop RPG Character, whose name and story are as follows: {}.

Here are three typical prompts:

1. "Photoreastic fantasy elf, sun rays shining from above, wooded fairland, cinematic, detailed , fantastical"

2. "Kneeling cat knight, portrait, finely detailed armor, intricate design, silver, silk, cinematic lighting, 4k."

3. "Ultra sharp award winning underwater nature photography of a woman riding a glistening gradient sea horse, backlit, depth of field, ocean floor, lush vegetation, particles, solar rays, coral, golden fishes."

You can use different words or concepts. Write just one prompt.
""".format(
        initial.capitalize()
    )

    if subject == 'Playlist Creator':
        return  """
    You are an expert song recommender. Based on the song {} create a playlist with 10 songs that are similar to the given song.
    Do not choose songs that have the same names or artists. Be creative, think outside the box. Do not write explanations or other words. Reply with only the playlist name,
    a description and the 10 songs:

""".format(
        initial.capitalize()
    )








def number_splitter(input):
    amount_list =[]
    product_list = []
    temp_amount_list =[]
    temp_product_list = []
    for character in input:
        if character.isnumeric():
            if len(temp_product_list) != 0:
                if temp_product_list[0] != '':
                    product_list.append("".join(temp_product_list))
                    print(product_list)
                    temp_product_list = []
            temp_amount_list.append(character)
        elif character.isalpha():
            if len(temp_amount_list) != 0:
                if temp_amount_list[0] != '':
                    amount_list.append("".join(temp_amount_list))
                    temp_amount_list = []
            temp_product_list.append(character)
    if len(temp_product_list) != 0:
            product_list.append("".join(temp_product_list))
    if len(temp_amount_list) != 0:
            amount_list.append("".join(temp_amount_list))

    return dict(zip(product_list, amount_list))

def createImageFromPrompt(prompt, subject, initial=None):
    if subject == 'Playlist Creator':
        final = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""Please provide a prompt to use in an image generation model such as DALL-E 2, to generate the cover
            for a playlist based on the song {initial}, which contains the description and songs listed here: {prompt}.
            The prompt should maximize the vibe of the image:
           """,
            temperature=1,
            frequency_penalty=0.05,
            max_tokens=1500,
        )
        response = openai.Image.create(prompt=final.choices[0].text, n=1, size="512x512")
        return response['data']
    else:
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        return response['data']
