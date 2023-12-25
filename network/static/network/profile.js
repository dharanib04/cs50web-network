document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", (event) => {
    const element = event.target;

    if (element.className == "editPost") {
      event.preventDefault();
      const content = element.parentElement.nextElementSibling.textContent;
      element.parentElement.nextElementSibling.style.display = "none";
      const newElement = document.createElement("textarea");
      const submitButton = document.createElement("button");
      submitButton.className = "btn btn-primary sm";
      const linebreak = document.createElement("br");
      element.parentElement.appendChild(newElement);
      element.parentElement.appendChild(linebreak);
      element.parentElement.appendChild(submitButton);
      submitButton.textContent = "Save";
      newElement.value = content;
      newElement.focus();
      submitButton.addEventListener("click", (event) => {
        saveButtonClick(event, newElement, element, linebreak);
      });
      element.style.display = "none";
    }
  });

  function saveButtonClick(event, newElement, element, linebreak) {
    event.preventDefault();
    element.parentElement.nextElementSibling.style.display = "block";
    element.parentElement.nextElementSibling.textContent = newElement.value;
    element.style.display = "block";
    newElement.remove();
    event.target.remove();
    linebreak.remove();

    fetch("/editpost", {
      method: "PUT",
      body: JSON.stringify({
        id: element.dataset.id,
        content: newElement.value,
      }),
    });
  }
});
