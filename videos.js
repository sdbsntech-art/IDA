document.addEventListener("DOMContentLoaded", () => {
    const videos = [
        {
            title: "Introduction à HTML",
            description: "Apprenez les bases du HTML avec Grafikart.",
            url: "https://www.youtube.com/embed/VIDEO_ID_HTML"
        },
        {
            title: "Introduction à CSS",
            description: "Découvrez comment styliser vos pages web avec CSS.",
            url: "https://www.youtube.com/embed/VIDEO_ID_CSS"
        },
        {
            title: "Introduction à JavaScript",
            description: "Maîtrisez les bases de JavaScript pour rendre vos sites interactifs.",
            url: "https://www.youtube.com/embed/VIDEO_ID_JS"
        }
        // Ajoutez d'autres vidéos ici
    ];

    const videoContainer = document.getElementById("video-container");

    videos.forEach((video) => {
        const videoCard = document.createElement("div");
        videoCard.classList.add("video-card");

        videoCard.innerHTML = `
            <iframe src="${video.url}" title="${video.title}" allowfullscreen></iframe>
            <h3>${video.title}</h3>
            <p>${video.description}</p>
        `;

        videoContainer.appendChild(videoCard);
    });
});