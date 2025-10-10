// Menu burger responsive
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
menuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Scroll fluide et activation du lien de menu
const links = document.querySelectorAll('.nav-link');
links.forEach(link => {
  link.addEventListener('click', function(e) {
    const href = this.getAttribute('href');
    if (href.startsWith('#')) {
      e.preventDefault();
      const targetId = href.replace('#', '');
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop - 60,
          behavior: 'smooth'
        });
        navLinks.classList.remove('open'); // Ferme le menu sur mobile
      }
    }
    // Sinon, laisse le comportement par défaut pour les liens externes
  });
});

// Activation dynamique du lien de menu selon la section visible
window.addEventListener('scroll', () => {
  const scrollPos = window.scrollY + 80;
  links.forEach(link => {
    const targetId = link.getAttribute('href').replace('#', '');
    const section = document.getElementById(targetId);
    if (section && section.offsetTop <= scrollPos && section.offsetTop + section.offsetHeight > scrollPos) {
      links.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    }
  });
});

// Animation d'apparition des sections au scroll
const sections = document.querySelectorAll('.section');
function revealSections() {
  const trigger = window.innerHeight * 0.92;
  sections.forEach(section => {
    const sectionTop = section.getBoundingClientRect().top;
    if (sectionTop < trigger) {
      section.classList.add('visible');
    }
  });
}
window.addEventListener('scroll', revealSections);
window.addEventListener('load', revealSections);

// Gestion des commentaires (localStorage)
const form = document.getElementById('form-commentaire');
const input = document.getElementById('input-commentaire');
const liste = document.getElementById('liste-commentaires');

function afficherCommentaires() {
  const commentaires = JSON.parse(localStorage.getItem('commentaires') || '[]');
  liste.innerHTML = commentaires.map(c => `<li>${c}</li>`).join('');
}

afficherCommentaires();

form.addEventListener('submit', function(e) {
  e.preventDefault();
  const val = input.value.trim();
  if (val) {
    const commentaires = JSON.parse(localStorage.getItem('commentaires') || '[]');
    commentaires.push(val);
    localStorage.setItem('commentaires', JSON.stringify(commentaires));
    input.value = '';
    afficherCommentaires();
  }
});

// Gestion des miniatures vidéo
document.addEventListener("DOMContentLoaded", () => {
    const videoThumbnails = document.querySelectorAll(".video-thumbnail");

    videoThumbnails.forEach((thumbnail) => {
        const videoId = thumbnail.getAttribute("data-video-id");

        thumbnail.addEventListener("click", () => {
            const iframe = document.createElement("iframe");
            iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
            iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
            iframe.allowFullscreen = true;
            iframe.width = "100%";
            iframe.height = "200px";

            // Remplace la miniature par l'iframe
            thumbnail.parentNode.replaceChild(iframe, thumbnail);
        });
    });
});