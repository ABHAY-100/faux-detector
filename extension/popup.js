document.addEventListener("DOMContentLoaded", function () {
  const score = document.getElementById("score");
  const output = document.getElementById("output");

  chrome.runtime.sendMessage({ action: "getResult" }, (response) => {
    if (response) {
      score.textContent = response.best_prediction;
      output.textContent = response.classification;

      const body = document.querySelector("body");
      if (response.classification.includes("Fake")) {
        body.style.backgroundImage = "url('bg_false.png')";
      } else {
        body.style.backgroundImage = "url('bg_true.png')";
      }
    }
  });
});
