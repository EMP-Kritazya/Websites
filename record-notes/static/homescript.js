const dynamicText = document.querySelector(".typewriter-text");

const sentences = [
  "Welcome to RecordIT.",
  "You write and we save!",
  "Login and retrieve your data ANYTIME",
];

let index = 0;
let charIndex = 0;
let isDeleting = false;

const typeEffect = () => {
  const currentSentence = sentences[index];
  const currentChar = currentSentence.substring(0, charIndex);
  dynamicText.textContent = currentChar;

  if (!isDeleting && charIndex < currentSentence.length) {
    charIndex++;
    setTimeout(typeEffect, 150);
  } else if (isDeleting && charIndex > 0) {
    charIndex--;
    setTimeout(typeEffect, 150);
  } else {
    isDeleting = !isDeleting;
    index = !isDeleting ? (index + 1) % sentences.length : index;
    setTimeout(typeEffect, 1000);
  }
};

typeEffect();
