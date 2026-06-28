const game = {
  answer: [],
  attempts: 9,
  maxAttempts: 9,
  numberCount: 3,
  isOver: false,
};


const input1 = document.getElementById("number1");
const input2 = document.getElementById("number2");
const input3 = document.getElementById("number3");

const attemptsSpan = document.getElementById("attempts");
const resultsBox = document.getElementById("results");
const resultDisplay = document.querySelector(".result-display");
const gameResultImg = document.getElementById("game-result-img");
const submitBtn = document.querySelector(".submit-button");


function updateUI() {
  attemptsSpan.textContent = game.attempts;
}



function generateAnswer() {
  const pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
  const result = [];

  for (let i = 0; i < game.numberCount; i++) {
    const idx = Math.floor(Math.random() * pool.length);
    result.push(pool[idx]);
    pool.splice(idx, 1);
  }
  return result;
}


function clearInputs() {
  input1.value = "";
  input2.value = "";
  input3.value = "";
  input1.focus();
}



function initGame() {
  game.attempts =game.maxAttempts;
  game.isOver = false;
  game.answer = generateAnswer();

  resultsBox.innerHTML = "";
  gameResultImg.src = "";
  submitBtn.disabled = false;

  clearInputs();
  updateUI();

  console.log("정답:", game.answer.join(""));
}


function compare(guess) {
  let strikes = 0;
  let balls = 0;

  for (let i = 0; i < game.numberCount; i++) {
    if (guess[i] === game.answer[i]) {
      strikes += 1;
    } else if (game.answer.includes(guess[i])) {
      balls += 1;
    }
  }
  return { strikes, balls };
}


// 결과창에줄 추가
function appendResult(guess, strikes, balls) {
  const row = document.createElement("div");
  row.className = "check-result";

  const left = document.createElement("div");
  left.className = "left";
  left.textContent = guess.join(" ");

  const colon = document.createElement("div");
  colon.textContent = ":";

  const right = document.createElement("div");
  right.className = "right";

  if (strikes === 0 && balls === 0) {

    right.innerHTML = `<span class="num-result out">O</span>`;
  } else {
    right.innerHTML =
      `${strikes} <span class="num-result strike">S</span> ` +
      `${balls} <span class="num-result ball">B</span>`;
  }

  row.appendChild(left);
  row.appendChild(colon);
  row.appendChild(right);
  resultsBox.appendChild(row);

  resultDisplay.scrollTop = resultDisplay.scrollHeight;
}


// 게임 결과
function endGame(isWin) {
  game.isOver = true;
  gameResultImg.src = isWin ? "success.png" : "fail.png";
  submitBtn.disabled = true;
}


// 확인하기 버튼 함수
function check_numbers() {
  if (game.isOver) return;

  const v1 = input1.value;
  const v2 = input2.value;
  const v3 = input3.value;

  // 입력되지 않은 칸이 있으면 확인하지 않고 input만 비움
  if (v1 === "" || v2 === "" || v3 === "") {
    clearInputs();
    return;
  }


  const guess = [parseInt(v1), parseInt(v2), parseInt(v3)];
  const { strikes, balls } = compare(guess);

  appendResult(guess, strikes, balls);


  game.attempts -= 1;
  updateUI();
  clearInputs();

  // 3) 게임 종료 체크
  if (strikes === game.numberCount) {
    endGame(true);
  } else if (game.attempts <= 0) {
    endGame(false);
  }
}



initGame();