"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $(".board");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  console.log(response)
  gameId = response.data.game_id;
  let board = response.data.board;
  console.log('started new game')

  displayBoard(board);
}

/** Display board */



function displayBoard(board) {
  $table.empty();
  for (let row of board) {
    let $tr = $("<tr>");
    for (let letter of row) {
      $tr.append(`<td>${letter}</td>`);
    }
    $table.append($tr);
  }
}


/** Send word submissions to back end  */


async function handleFormSubmit(evt) {
  evt.preventDefault();

  const word = $wordInput.val().toUpperCase();
  if (!word) return;

  await submitWordToAPI(word);

  $wordInput.val("").focus();
}

$form.on("submit", handleFormSubmit);


async function submitWordToAPI(word) {
  const response = await axios({
    url: "/api/score-word",
    method: "POST",
    data: { word, gameId }
  });


  const {result} = response.data

  if (result === "not-word"){
    showMessage(`Not a Valid word!: ${word}`, 'ERR')
  }
  else if (result === "not-on-board"){
    showMessage(`word is not on board!: ${word}`, 'ERR')
  }
  else {
    showWord(word);
    showMessage(`Added: ${word}`, 'nice!')
  }

}


/** Add word to played word list in DOM */

function showWord(word) {
  $($playedWords).append($("<li>", { text: word }));
}


/** Show status message. */

function showMessage(msg, cssClass) {
  $message
    .text(msg)
    .removeClass()
    .addClass(`msg ${cssClass}`);
}



/** Event Handlers */




start();