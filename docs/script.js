// Data structure to define the questions and flow of the guideline process.
const questions = {
  start: {
      question: "Are students interested in network engineering?",
      yes: "tcp",
      no: "exper_dns"
  },
  tcp: {
      question: "Do students need foundational network programming?",
      yes: "module1",
      no: "switch",
      default: "int_dns"
  },
  switch: {
      question: "Do students have knowledge and experience with switches?",
      yes: "module2"
  },
  exper_dns: {
      question: "Do students have knowledge and experience related to DNS?",
      yes: "module3",
      no: "exper_web",
      default: "exper_web"
  },
  exper_web: {
      question: "Do students have knowledge and experience related to web?",
      yes: "module4"
  },
  int_dns: {
      question: "Are students interested in understanding DNS?",
      yes: "module3",
      default: "int_web"
  },
  int_web: {
      question: "Are students interested in Web development?",
      yes: "module4"
  },
  mininet: {
      question: "Do students have experience with network simulation tools?",
      yes: "module5",
      no: "finished"
  },
  // Define modules with numbers and details.
  module0: { num: 0, detail: "Guide for Setup Captive Portal Project" },
  module1: { num: 1, detail: "Module 1: TCP Server/Client" },
  module2: { num: 2, detail: "Module 2: Switch Implementation" },
  module3: { num: 3, detail: "Module 3: DNS Server Implementation" },
  module4: { num: 4, detail: "Module 4: Web Server Frontend and Backend Implementation" },
  module5: { num: 5, detail: "Module 5: Mininet Implementation" }
};

// Helper queues for managing the question flow and the modules for recommendation.
const queues = [];
const recommendedModules = [0];

// Handler for displaying the final recommendations.
function showGuideline() {
  const container = document.getElementById('questionContainer');
  const links = recommendedModules.map(num => `<a href="./Module${num}.md" download="Module${num}.md">${questions[`module${num}`].detail}</a>`);
  if (links.length !== 0) {
      container.innerHTML = `<p>Recommended Modules:<br>${links.join('<br>')}</p>`;
      const downloadAllButton = document.createElement('button');
      downloadAllButton.textContent = 'Download All';
      downloadAllButton.onclick = function() { downloadAll(links); };
      container.appendChild(downloadAllButton);
  } else {
      container.innerHTML = '<p>Unfortunately, this tutorial is not for you at the moment</p>';
  }
}

// Define downloadAll function to concatenate and download content from all provided links
async function downloadAll(links) {
  let combinedContent = '';  // Initialize a string to store combined content

  // Use Promise.all to handle all fetch requests in parallel
  const filesContent = await Promise.all(recommendedModules.map(num => 
      fetch(`./Module${num}.md`).then(response => response.text())  // Fetch text content from each URL
  ));

  // Concatenate all file contents
  combinedContent = filesContent.join('\n');  // Use newline as a separator

  // Create a Blob object for the combined content
  const blob = new Blob([combinedContent], { type: 'text/plain' });

  // Create a link for downloading
  const downloadLink = document.createElement('a');
  downloadLink.href = URL.createObjectURL(blob);
  downloadLink.download = 'Captive Protal Guidelines.md';  // Set the download file name
  document.body.appendChild(downloadLink);
  downloadLink.click();  // Trigger the download
  document.body.removeChild(downloadLink);  // Clean up the link from the page
}

// Show question or result based on the student's pathway through the questions.
function showQuestion(node) {
  if (node === 'finished') {
      return showGuideline();
  }

  // If the node points to a terminal module node or is undefined, manage module addition.
  if (node === 'undefined' || questions[node].num) {
      if (node !== 'undefined') {
          recommendedModules.push(questions[node].num);
      }
      // Proceed to the next question in the queue or end.
      if (queues.length > 0) {
          showQuestion(queues.shift());
      } else {
          showGuideline();
      }
      return;
  }

  // Render the current question.
  const container = document.getElementById('questionContainer');
  container.innerHTML = '';
  const questionText = questions[node].question;
  const questionElement = document.createElement('div');
  questionElement.className = 'question';
  questionElement.innerHTML = `<p>${questionText}</p>
      <button onclick="showQuestion('${questions[node].yes}')">Yes</button>
      <button onclick="showQuestion('${questions[node].no}')">No</button>`;

  container.appendChild(questionElement);
  // Queue the default path if it exists.
  if (questions[node].default) queues.push(questions[node].default);
}

// Initialize the questioning process.
document.addEventListener('DOMContentLoaded', () => {
  showQuestion('start');
});
