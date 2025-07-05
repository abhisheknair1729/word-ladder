import { wordPairs } from "./wordPairs.js";
import { validWords } from "./validWords.js";


let source = "";
let target = "";
let solution = "";
let difficulty = 0;
let ladder = [];

/** Utility: Random 4-letter word from valid list */
/** The pairs are sorted by difficulty. Therefore, we have a 
 * threshold to ensure that super difficult words are not picked.
 */
function pickRandomPair() {
  if (wordPairs.length === 0) return null;

  const difficulty_threshold = 10000
  // assert(wordPairs.length > difficulty_threshold, "wordPairs length exceeds maximum limit");
  const idx = Math.floor(Math.random() * difficulty_threshold);
  
  return wordPairs[idx];
}

/** Utility: Check if two words differ by one letter */
function isOneLetterDifferent(word1, word2) {
  if (word1.length !== word2.length) return false;
  let diff = 0;
  for (let i = 0; i < word1.length; i++) {
    if (word1[i] !== word2[i]) diff++;
  }
  return diff <= 1;
}

/* Generate HTML for displaying a word */
function createWordDisplayHTML(word) {

  let htmlContent = "";
  for (let i = 0; i < word.length; i++) {
    const letter = word[i].toUpperCase();
    htmlContent += `<p class=bordered-text>${letter}</p>`;
    htmlContent += `<div class=horizontalgap></div>`;
  }
  htmlContent += "<br>";
  // htmlContent += "</tr></table>";
  return htmlContent;
}

function createSpecialWordDisplayHTML(word) {

  let htmlContent = "";
  for (let i = 0; i < word.length; i++) {
    const letter = word[i].toUpperCase();
    htmlContent += `<p class=bordered-text-spl>${letter}</p>`;
    htmlContent += `<div class=horizontalgap></div>`;
  }
  htmlContent += "<br>";
  // htmlContent += "</tr></table>";
  return htmlContent;
}

/* Generate HTML for displaying the solution */
function createSolutionHTML(solution) {
  if (!solution) return "No solution available.";
  const steps = solution;
  let htmlContent = "";
  steps.forEach((step, index) => {
    htmlContent += `<span">${step.toUpperCase()}</span>`;
    if (index < steps.length - 1) {
      htmlContent += " → ";
    }
  });
  return htmlContent;
}

/** Show an empty ladder */
function showEmptyLadder() {  
  const list = document.getElementById("ladderword");
  const htmlContent = createWordDisplayHTML("    ");
  list.innerHTML = htmlContent;
}

/** Initialize game */
function initializeGame() {
  
  let pair = pickRandomPair();
  if(pair){
    source = pair.word1;
    target = pair.word2;
    solution = pair.solution;
    difficulty = pair.difficultyscore;
  } else {
    source = "cold";
    target = "warm";
    solution = "cold->cord->card->ward->warm";
    difficulty = 1;
  }

  document.getElementById("sourceword").innerHTML = createSpecialWordDisplayHTML(source);
  document.getElementById("targetword").innerHTML = createSpecialWordDisplayHTML(target);

  ladder = [source];
  showEmptyLadder();
  document.getElementById("message").textContent = "";
}

/** Submit a guess */
function submitWord() {
  const input = document.getElementById("wordInput");
  const word = input.value.trim().toLowerCase();
  const message = document.getElementById("message");
  message.textContent = "";

  if (word.length !== 4 || !validWords.includes(word)) {
    message.textContent = "❌ Not a valid 4-letter word.";
    return;
  }

  const prevWord = ladder[ladder.length - 1];
  if (!isOneLetterDifferent(prevWord, word)) {
    message.textContent = "❌ Must differ by only one letter.";
    return;
  }

  var isDone = word == target;

  ladder.push(word);
  updateLadder(isDone);

  if (isDone) {
    message.textContent = "🎉 You win! You've reached the target word!";
    input.disabled = true;
  }

  input.value = "";
}

function resetLadder() {
  ladder = [source];
  showEmptyLadder();
  document.getElementById("message").textContent = "";
}

/** Update the displayed ladder list */
function updateLadder(isDone) {
  const list = document.getElementById("ladderword");
  list.innerHTML = "";
  for( let i = 1; i < ladder.length; i++) {
    const word = ladder[i];
    list.innerHTML += createWordDisplayHTML(word);
  }

  if(!isDone) {
    list.innerHTML += createWordDisplayHTML("    "); //create space for the next word
  }

}

function displaySolution() {
  const message = document.getElementById("message");
  if (solution) {
    message.innerHTML = `${createSolutionHTML(solution)}`;
  }else {
    //should never happen
    message.textContent = "No solution available.";
  }
}

var wordSubmited = document.getElementById("wordInput");
wordSubmited.addEventListener("keyup", function(event) {

  if (event.key === "Enter") {
    event.preventDefault();
    submitWord();
  }

});

window.initializeGame = initializeGame;
window.submitWord = submitWord;
window.resetLadder = resetLadder;
window.displaySolution = displaySolution;

