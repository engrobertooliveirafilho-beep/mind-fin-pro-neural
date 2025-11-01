export function speak(text){
  const u = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(u);
}