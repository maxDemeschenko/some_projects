for (let i = 1; i <= 81; i++)
{
    let obj = document.getElementById(i.toString());
    obj.addEventListener("click", () => OnClick(i));
}

let last_selected_id;

document.addEventListener('keypress', (e) => key_pressed(e))

document.getElementById('new-game-button').addEventListener('click', () => {
    fetch('http://127.0.0.1:5000/new_game')
        .then(response => {
            window.location.href = response.url;
        });
})

function key_pressed(e) {
    if (e.code < 1 || e.code > 9)
        return;
    let obj = document.getElementById(last_selected_id);
    if (obj.innerText)
        return;
    obj.innerText = e.key;
    fetch('http://127.0.0.1:5000/fill_cell', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({
            'cell_id': last_selected_id,
            'number': Number(e.key)
        })
    }).then(response => {
        if (!response.ok) {
            obj.innerText = '';
            alert('Last number is mistaken');
        }
    });
    if (CheckEndOfGame())
        alert('YOU WIN');
    OnClick(last_selected_id);
}

function CheckEndOfGame() {
    for (let i = 1; i <= 81; i++) {
        if (!document.getElementById(i.toString()).innerText)
            return false;
    }
    return true;
}

function OnClick(obj_id) {
    last_selected_id = obj_id;
    ClearBackgroundColors();
    let obj = document.getElementById(obj_id.toString());
    obj.style.backgroundColor = '#fafa8e';
    let number = obj.innerText
    if (number === '')
        return;
    fetch(`http://127.0.0.1:5000/get_cells_with_number/${number}`)
        .then(response => {
            let json_from_response = response.json();
            json_from_response.then(value => value.filter(index => index !== obj_id)
                .forEach(index => {
                    let same_number_object = document.getElementById(index);
                    same_number_object.style.backgroundColor = '#d5ffae';
            }));
        })
}

function ClearBackgroundColors() {
    for (let i = 1; i <= 81; i++)
    {
        let obj = document.getElementById(i.toString());
        obj.style.backgroundColor = 'white';
    }
}