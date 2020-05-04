// Function call when click "SOLVE" button 
function submitForm() {

    // Retrieve number for each row in mainboard
    function retrieveRowData(id) {
        row = document.querySelectorAll(id);
        row_data = '';
        row.forEach(square => {
            square = square.value.toString();
            square = square ? square : 0; // Insert 0 for empty square
            row_data += square;
        });
        return row_data;
    }

    array = [] // Complete list for row in string
    for (i = 1; i < 10; i++) { // id from r1 to r9
        each_row = retrieveRowData(`#r${i}`)
        array.push(each_row)
    }

    // Create input tag and append array(user input) 
    let node = document.createElement("input");
    node.setAttribute("type", "text");
    node.setAttribute("name", "raw_data")
    node.setAttribute("id", "raw_data")

    // Append into #sudoku-main form
    board = document.querySelector('.sudoku-main');
    board.appendChild(node);

    // Insert array(user input) into #raw_data that create earlier
    document.querySelector('#raw_data').value = array;

    // Submit form #mainboard
    let mainboard = document.querySelector('#mainboard');
    mainboard.submit();
}

// Show error message if problem unsolved
error = document.querySelector(".error");
error_msg = error.innerHTML;
if (error_msg) {
    error.style.display = "block";
}

// Get the data that return by django backend in #raw_data_list
raw_data_list = document.querySelector('#raw_data_list').innerHTML;
if (raw_data_list) {
    // The raw_data_list is type of Python list format, and convert to raw string while select by JavaScript
    // So, unused string "[", "]", "'" and space need to be removed
    raw_data_list = raw_data_list.replace("[", "");
    raw_data_list = raw_data_list.replace("]", "");
    raw_data_list = raw_data_list.replace(/'/g, "");
    raw_data_list = raw_data_list.replace(/ /g, "");
    // Convert the remaining raw string to array
    raw_data_list = raw_data_list.split(",");

    // loop through array and insert each number to its corresponding square
    let rowInStringIndex = 1;
    raw_data_list.forEach(rowInString => {
        let squareIndex = 0;
        rowInList = rowInString.split(""); // Make each of rowInString into separate item in array
        rowInList.forEach(numInString => {
            squareNode = document.querySelectorAll(`#r${rowInStringIndex}`)[squareIndex]; // From r1 to r9, each square in the row
            squareNode.setAttribute("value", numInString);
            squareIndex += 1;
        });
        rowInStringIndex += 1;
    });

    // Disable "SOLVE" button after answer display on board
    buttonSolve = document.querySelector(".btn-solve");
    buttonSolve.disabled = true;
    buttonSolve.style.color = '#666666';
    buttonSolve.style.backgroundColor = '#cccccc';
    buttonSolve.style.border = '2px solid #999999';
}

// Function call when click "RESET" button 
function resetForm() {
    if (raw_data_list) {
        // Replace each square with empty string
        for (rowIndex = 1; rowIndex <= 9; rowIndex ++) {
            rowNode = document.querySelectorAll(`#r${rowIndex}`);
            rowNode.forEach(squareNode => {
                squareNode.setAttribute("value", "");
            });
        }
    } else { // Reset before "SOLVE" button been pressed
        document.querySelector("#mainboard").reset();
    }
        
    // Enable "SOLVE" button after reset button been pressed
    buttonSolve = document.querySelector(".btn-solve");
    buttonSolve.disabled = false;
    buttonSolve.style.color = 'darkblue';
    buttonSolve.style.backgroundColor = 'cornflowerblue';
    buttonSolve.style.border = '2px solid darkblue';
}
