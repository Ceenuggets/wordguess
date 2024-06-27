import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import re
import random

external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/word_guess.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

guess_letters = set()
num = 0
guessed_word = ""


class WordGuess:
    def __init__(self, *words):
        self.words = words
        self.correct_letters_count = 0
        self.chosen_word = set()
        self.guessed_word = ""
        self.guessed_letters = set()

    def random_word(self):
        random_word = random.choice(self.words)
        self.guessed_word = re.sub(r".", "-", random_word)
        self.supply_word(random_word.lower())

        return random_word

    def supply_word(self, random_word):
        pass
        # print("====================")
        # print(len(self.guessed_word))
        # print(len(random_word))
        # print(len(self.chosen_word))


def compare_words(current_word, letter):
    global guessed_word
    for i in range(len(current_word)):
        if current_word[i] == letter.lower():
            new_word = list(guessed_word)
            new_word[i] = letter.lower()
            guessed_word = "".join(new_word)
    return guessed_word


sample = WordGuess("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
                   "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
                   "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
                   "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
                    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
                    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
                    "Republic of the Congo", "Congo DRC", "Costa Rica", "Ivory Coast",
                    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
                    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
                    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
                    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
                    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
                    "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
                    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
                    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
                    "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
                    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
                    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
                    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
                    "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau",
                    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
                    "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
                    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
                    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
                    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
                    "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
                    "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand",
                    "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
                    "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
                    "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela",
                    "Vietnam", "Yemen", "Zambia", "Zimbabwe")

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("Word Guess")
                ], className='d-flex justify-content-center text-align-center', id="title"),
                html.Div([
                    html.Div([
                        html.Span(id="expected_word"),
                        html.Hr(style={"width": "100% !important",  }),
                        html.Span(id="min_expected_guess"),
                        html.Span(id="guessed_letters"),
                        html.Span(id="num_of_attempts"),

                    ], id="info_div"),
                    html.Hr(),
                    html.Label("Guess a word:", style={'fontSize': '18px'}),
                    dcc.Input(
                        id="user_input",
                        type="text",
                        # placeholder="Guess a word",
                        style={'margin': '10px'},
                        maxLength=1,
                        pattern=".{1,1}",
                        inputMode="text",
                        autoCapitalize="none" 
                    ),
                ])
            ], id="input_div")
        ], xs=12, sm=12, md=8, lg=8, xl=6,
            className="mx-auto"
        ),
    ], justify="center", className='g-0'),
    dcc.Store(id='stored_data'),
    dcc.Store(id='store-content', data=None),
], fluid=True)


app.clientside_callback(
    """
    function(value) {
        var inputElem = document.getElementById('user_input');
        if (inputElem) {
            inputElem.focus();
            inputElem.select();
        }
        return value;
    }
    """,
    Output('store-content', 'data'),
    Input('user_input', 'value')
)

@app.callback(
    Output("expected_word", "children"),
    Output("min_expected_guess", "children"),
    Output('stored_data', 'data'),
    Input("user_input", "value"),
    State("expected_word", "children"),
)
def update_output_div(user_input, current_word):
    global guessed_word
    chosen_word = set()
    if not current_word:
        new_word = sample.random_word()
        chosen_word.update(new_word)
        stored_data = {'current_word': new_word}
        masked_newword = re.sub(r".", "-", new_word)
        guessed_word = masked_newword
        # print(new_word)
        return masked_newword, html.P(["Minimum expected guesses: ", html.Span(len(chosen_word), className="min-attempts shared-span-style")]), stored_data
    else:
        return dash.no_update


@app.callback(
    Output("expected_word", "children",  allow_duplicate=True),
    Output("guessed_letters", "children"),
    Output("num_of_attempts", "children"),
    Input("user_input", "value"),
    State('stored_data', 'data'),
    prevent_initial_call=True,
)
def process_user_input(user_input, stored_data):
    global num
    global guessed_word
    pattern = re.compile(r"^[a-zA-Z\s.]+$")
    if pattern.match(user_input):
        num += 1
        if stored_data:
            current_word = stored_data['current_word'].lower()
            guess_letters.update(user_input.lower())
            guess_outcome = compare_words(current_word, user_input.lower())

            if guess_outcome.lower() == current_word.lower():
                num = 0
                guess_letters.clear()
                # print("Hurray, You have answer")
                return stored_data['current_word'], html.P(["Already guessed: ", html.Span(",".join(guess_letters), className="guessed_letters shared-span-style")]), html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style") ])
                
            else:
                return guess_outcome, html.P(["Already guessed: ", html.Span(",".join(guess_letters), className="guessed_letters shared-span-style")]), html.P(["Attempts: ", html.Span(str(num),className="attempts shared-span-style") ])

            # return guessed_word, f"Already guessed letters: {",".join(guess_letters)}", f"Number of attempts: {num}"

        else:
            return dash.no_update
    return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True, port=8066)
