const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const configDiv = document.getElementById("config");
const fileNameSpan = document.getElementById("file-name");
const extractBtn = document.getElementById("extract-btn");
const progressDiv = document.getElementById("progress");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const resultsDiv = document.getElementById("results");
const resultTitle = document.getElementById("result-title");
const slidesGrid = document.getElementById("slides-grid");
const downloadBtn = document.getElementById("download-btn");

let selectedFile = null;

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
        handleFile(fileInput.files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    fileNameSpan.textContent = file.name;
    configDiv.classList.remove("hidden");
    resultsDiv.classList.add("hidden");
}

extractBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    extractBtn.disabled = true;
    extractBtn.textContent = "Processando...";
    progressDiv.classList.remove("hidden");
    resultsDiv.classList.add("hidden");
    progressFill.style.width = "10%";
    progressText.textContent = "Enviando vídeo...";

    const formData = new FormData();
    formData.append("video", selectedFile);
    formData.append("interval", document.getElementById("interval").value);

    try {
        progressFill.style.width = "40%";
        progressText.textContent = "Extraindo slides...";

        const response = await fetch("/extract", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erro ao processar");
        }

        progressFill.style.width = "80%";
        progressText.textContent = "Gerando download...";

        setTimeout(() => {
            progressFill.style.width = "100%";
            progressText.textContent = "Pronto!";

            resultTitle.textContent = `${data.slide_count} slides extraídos`;
            slidesGrid.innerHTML = "";

            data.slides.forEach((slide) => {
                const img = document.createElement("img");
                img.src = `/slide/${data.job_id}/${slide}`;
                img.alt = slide;
                img.loading = "lazy";
                slidesGrid.appendChild(img);
            });

            downloadBtn.href = `/download/${data.job_id}`;
            resultsDiv.classList.remove("hidden");

            extractBtn.disabled = false;
            extractBtn.textContent = "Extrair Slides";
        }, 500);

    } catch (err) {
        progressText.textContent = `Erro: ${err.message}`;
        progressFill.style.width = "0%";
        extractBtn.disabled = false;
        extractBtn.textContent = "Extrair Slides";
    }
});
