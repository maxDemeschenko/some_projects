import json
from datetime import datetime
import flask
from flask import Flask
from sudoku_solver2 import create_sudoku_table, unfilled_sudoku_table

app = Flask(__name__)

current_user_table = None
current_user_unfilled_table, current_result = unfilled_sudoku_table()
current_user_working_table = current_user_unfilled_table.copy()


def table_for_display(table):
    table_output = table.copy()
    for i, row in enumerate(table_output):
        for j, item in enumerate(row):
            if item == 0:
                table_output[i][j] = ""
    return table_output


@app.route('/')
def hello_world():  # put application's code here
    global current_user_table
    current_user_table = create_sudoku_table()
    return flask.render_template('sudoku.html', initial_table=current_user_table)


@app.route('/unfilled')
def unfilled_field():
    global current_user_unfilled_table
    # current_user_unfilled_table = unfilled_sudoku_table()
    return flask.render_template('sudoku.html',
                                 initial_table=table_for_display(current_user_working_table))


@app.route('/check_server')
def check_server():
    return current_result


@app.route('/get_cells_with_number/<int:clicked_number>')
def get_cells_with_number(clicked_number):
    global current_user_working_table
    indexes = []
    for i in range(9):
        for j in range(9):
            if current_user_working_table[i][j] == clicked_number:
                indexes.append(i * 9 + j + 1)
    return flask.Response(json.dumps(indexes), content_type='application/json', status=200)


@app.route('/fill_cell', methods=['post'])
def fill_cell():
    json_from_request = flask.request.json
    cell_id = json_from_request['cell_id'] - 1
    i = cell_id // 9
    j = cell_id % 9
    number = json_from_request['number']
    if int(number) != current_result[i][j]:
        return flask.abort(422)
    current_user_working_table[i][j] = number
    return flask.Response(status=200)


@app.route('/new_game')
def new_game():
    timer = datetime.now()
    global current_user_unfilled_table, current_result, current_user_working_table
    current_user_unfilled_table, current_result = unfilled_sudoku_table()
    current_user_working_table = current_user_unfilled_table.copy()
    print(datetime.now() - timer)
    return flask.redirect('/unfilled')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
