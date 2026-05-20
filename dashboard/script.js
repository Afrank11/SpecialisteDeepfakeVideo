const formulaire = document.getElementById("formulaire-video");
const resultat = document.getElementById("resultat");

formulaire.addEventListener("submit", async function (event) {
    event.preventDefault();

    const fichierVideo = document.getElementById("video").files[0];

    if (!fichierVideo) {
        resultat.innerHTML = "<p>Veuillez selectionner une video.</p>";
        return;
    }

    const donnees = new FormData();
    donnees.append("video", fichierVideo);

    resultat.innerHTML = "<p>Analyse en cours...</p>";

    try {
        const reponse = await fetch("http://127.0.0.1:8000/analyser-video", {
            method: "POST",
            body: donnees
        });

        const data = await reponse.json();

        resultat.innerHTML = `
            <h2>Resultat de l'analyse</h2>
            <p><strong>Score yeux :</strong> ${data.score_yeux}%</p>
            <p><strong>Score levres :</strong> ${data.score_levres}%</p>
            <p><strong>Score final :</strong> ${data.score_final}%</p>
            <p><strong>Niveau :</strong> ${data.niveau}</p>
        `;
    } catch (erreur) {
        resultat.innerHTML = "<p>Erreur pendant l'analyse.</p>";
    }
});