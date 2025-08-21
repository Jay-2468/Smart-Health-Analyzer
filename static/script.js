document.addEventListener("DOMContentLoaded", () => {
  const themeToggleBtn = document.getElementById("theme-toggle");
  const analyzeBtn = document.getElementById("analyze-btn");
  const exportPdfBtn = document.getElementById("export-pdf-btn");
  const symptomsInput = document.getElementById("symptoms");
  const resultsSection = document.getElementById("results-section");
  const resultsContent = document.getElementById("results-content");
  const loader = document.getElementById("loader");

  let latestAnalysisData = null;

  // Theme Toggler 
  const currentTheme = localStorage.getItem("theme");
  if (currentTheme) {
    document.documentElement.setAttribute("data-theme", currentTheme);
    if (currentTheme === "dark") themeToggleBtn.textContent = "☀️";
  }

  themeToggleBtn.addEventListener("click", () => {
    let theme = document.documentElement.getAttribute("data-theme");
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "light");
      localStorage.setItem("theme", "light");
      themeToggleBtn.textContent = "🌙";
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      localStorage.setItem("theme", "dark");
      themeToggleBtn.textContent = "☀️";
    }
  });

  // Analyze Symptoms 
  analyzeBtn.addEventListener("click", async () => {
    if (!symptomsInput.value.trim()) {
      alert("Please describe your symptoms.");
      return;
    }

    resultsSection.classList.remove("hidden");
    loader.classList.remove("hidden");
    resultsContent.innerHTML = "";
    exportPdfBtn.classList.add("hidden");
    latestAnalysisData = null;

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptomsInput.value }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error);

      latestAnalysisData = data;
      displayResults(data);
      exportPdfBtn.classList.remove("hidden");
    } catch (error) {
      resultsContent.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
    } finally {
      loader.classList.add("hidden");
    }
  });

  function displayResults(data) {
    let html = "";
    if (data.summary?.length) {
      html += `<h3>Identified Symptoms</h3><ul>${data.summary
        .map((item) => `<li>${item}</li>`)
        .join("")}</ul>`;
    }
    if (data.considerations?.length) {
      html += `<h3>Potential Considerations</h3><ul>${data.considerations
        .map((item) => `<li>${item}</li>`)
        .join("")}</ul>`;
    }
    if (data.recommendations?.length) {
      html += `<h3>Recommended Actions</h3><ul>${data.recommendations
        .map((item) => `<li>${item}</li>`)
        .join("")}</ul>`;
    }
    resultsContent.innerHTML = html;
  }

  // --- Export to PDF ---
  exportPdfBtn.addEventListener("click", async () => {
    if (!latestAnalysisData) return;

    try {
      const response = await fetch("/export_pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(latestAnalysisData),
      });

      if (!response.ok) throw new Error("PDF generation failed.");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "HealthReport.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert(`Error exporting PDF: ${error.message}`);
    }
  });
});
