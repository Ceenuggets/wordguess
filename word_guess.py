import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import re
import random
from word_guess_data import countries


external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/word_guess.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])


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


sample = list(countries.keys())





app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("Word Guess")
                ], className='d-flex justify-content-center text-align-center', id="title"),
                html.Div([
                    html.Div([
                        html.Label("Country:", 
                                   style={'fontSize': '18px', 'marginRight': '5px', 'fontWeight': 'bold', 'display': 'inline-block'}),
                        html.Div([
                            html.Span(id="expected_word"),
                            html.Span(id="capital"),
                        ], id="result"),
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
    Output("result", "style"),
    Output("capital", "children"),
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
            return masked_random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]),html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),{'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}, ""
        if pattern.match(value):
            num += 1
            guessed_letters.update(value.lower())
            guess_outcome = word_screen(value)
            if guess_outcome.lower() == random_output.lower():
                match_found = True
                # print("Yes, you've got the answer!")
                print(num)
                print(guessed_letters)
                print(countries[random_output])
                return random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]),html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),{'backgroundColor': 'green', 'color': 'white', 'boxShadow': '5px 10px 5px rgba(0, 0, 0, 0.4)', 'border': '2px solid white'}, countries[random_output]
            else:
                return guess_outcome, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]), html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]),{'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}, ""
        else:
            return masked_random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]), html.P(["Already guessed: ", html.Span(",".join(guessed_letters), className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]), {'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}, ""
    else:
        random_output, masked_random_output = random_pick(sample)
        # masked_random_output = re.sub(r".", "-", random_output)
        return masked_random_output, html.P(["Minimum expected guesses: ", html.Span(len(set(random_output)), className="min-attempts shared-span-style")]), html.P(["Already guessed: ", html.Span("-", className="guessed_letters shared-span-style")]),html.P(["Attempts: ", html.Span(str(num), className="attempts shared-span-style")]), {'backgroundColor': '#f0f0f0', 'color': 'black', 'boxShadow': 'box-shadow: 5px 10px 5px rgba(0, 0, 0, 0.2)'}, ""


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