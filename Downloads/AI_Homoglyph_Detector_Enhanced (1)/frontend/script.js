async function checkDomain() {
  const domain = document.getElementById("domainInput").value;
  const response = await fetch("http://localhost:5000/check", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ domain: domain })
  });
  const data = await response.json();
  const result = document.getElementById("result");
  if (data.phishing) {
    result.textContent = `⚠️ Phishing detected! Looks like "${domain}" mimics "${data.matched}"`;
    result.style.color = "red";
  } else {
    result.textContent = `✅ Safe! No visual similarity found.`;
    result.style.color = "green";
  }
}

async function generateHomoglyphs() {
  const domain = document.getElementById("domainInput").value;
  const response = await fetch("http://localhost:5000/generate", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ domain: domain })
  });
  const data = await response.json();
  const result = document.getElementById("result");
  if (data.variants.length > 0) {
    result.innerHTML = "Generated Homoglyphs:<br>" + data.variants.join("<br>");
    result.style.color = "blue";
  } else {
    result.textContent = "No homoglyph variants generated.";
    result.style.color = "gray";
  }
}