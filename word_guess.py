import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import re
import random
import pandas as pd
import os

external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/word_guess.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'word_guess.csv')
countries = pd.read_csv(csv_path, encoding="latin-1")
# countries = pd.read_csv("word_guess.csv", encoding="latin-1")
print(countries["Country"])
random_output = ""
masked_random_output= ""
num = 0
guessed_letters = set()
match_found = False


def random_pick(*words):
    global num
    global guessed_letters
    global match_found
    random_word = random.choice(*words)
    rnd_mask = re.sub(r".", "-", random_word)
    num = 0
    match_found = False
    guessed_letters.clear()
    return random_word, rnd_mask


def word_screen(input_char):
    global masked_random_output
    for i in range(len(random_output)):
        if random_output[i].lower() == input_char.lower():
            new_word = list(masked_random_output)
            new_word[i] = input_char.lower()
            masked_random_output = "".join(new_word)
            print("".join(new_word))
    return masked_random_output

# countries["Country"]
sample =  countries["Country"].values
# "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
# "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
# "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
# "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
# "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
# "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
# "Republic of the Congo", "Congo DRC", "Costa Rica", "Ivory Coast",
# "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
# "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
# "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
# "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
# "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
# "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
# "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
# "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
# "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
# "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
# "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
# "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
# "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau",
# "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
# "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
# "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
# "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
# "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
# "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
# "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand",
# "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
# "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
# "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela",
# "Vietnam", "Yemen", "Zambia", "Zimbabwe"





app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("Word Guess")
                ], className='d-flex justify-content-center text-align-center', id="title"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label("Country:",
                                       style={'fontSize': '18px', 'marginRight': '5px', 'fontWeight': 'bold'}),
                            html.Span(id="expected_word"),
                        ]),
                        html.Hr(style={"width": "100% !important", }),
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

                    ),
                ])
            ], id="input_div")
        ], xs=12, sm=12, md=8, lg=8, xl=6,
            className="mx-auto"
        ),
    ], justify="center", className='g-0'),
    dcc.Store(id='input_interacted', data=False),
    dcc.Store(id='store-content', data=None),
], fluid=True)




@app.callback(
    Output('input_interacted', 'data'),
    Input('user_input', 'value'),
    State('input_interacted', 'data')
)
def track_input_interaction(value, interacted):
    if not interacted and value:
        return True
    return interacted


@app.callback(
    Output('expected_word', 'children'),
    Output("min_expected_guess", "children"),
    Output("guessed_letters", "children"),
    Output("num_of_attempts", "children"),
    Output("expected_word", "style"),
    [Input('user_input', 'value'),
     Input('input_interacted', 'data')]
)
def update_output(value, interacted):
    global random_output
    global masked_random_output
    global num
    global match_found
    pattern = re.compile(r"^[a-zA-Z\s.]+$")
    if interacted:
        if match_found:
            random_output, masked_random_output = random_pick(sample)
            return masked_random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]),html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),{'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}
        if pattern.match(value):
            num += 1
            guessed_letters.update(value.lower())
            guess_outcome = word_screen(value)
            if guess_outcome.lower() == random_output.lower():
                match_found = True
                # print("Yes, you've got the answer!")
                print(num)
                print(guessed_letters)
                return random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]),html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),{'backgroundColor': 'green', 'color': 'white', 'boxShadow': '5px 10px 5px rgba(0, 0, 0, 0.4)', 'border': '2px solid white'}
            else:
                return guess_outcome, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]), html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),{'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}
        else:
            return masked_random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]), html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]), {'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}
    else:
        random_output, masked_random_output = random_pick(sample)
        # masked_random_output = re.sub(r".", "-", random_output)
        return masked_random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]), html.P(["Already guessed: ", html.Span("-", className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]), {'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}


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

if __name__ == '__main__':
    app.run_server(debug=True)